# main.py
from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import config
from agents import TestGenerator
from utils import query_rag
from requests_and_responses import (
    AppContext,
    TestGenerationRequest,
    TestGenerationResponse,
    RAGTestGenerationRequest
)

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Test Generator
test_generator = TestGenerator()


# -------------------------
# API Routes
# -------------------------


@app.get("/")
async def root():
    return {"service": config.API_TITLE, "status": "running", "version": config.API_VERSION}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "llm_configured": bool(config.ANTHROPIC_API_KEY),
        "model": config.ANTHROPIC_MODEL,
    }


@app.post("/generate-test", response_model=TestGenerationResponse)
async def generate_test(request: TestGenerationRequest):
    """Generate a test using the TestGenerator class"""
    try:
        return test_generator.run(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating test: {str(e)}")


@app.post("/generate-test-with-rag", response_model=TestGenerationResponse)
async def generate_test_with_rag(request: RAGTestGenerationRequest):
    """
    Generate a test using RAG to automatically retrieve context from the codebase.
    User provides a free-form natural language description, and RAG finds relevant
    screens, accessibility IDs, and code snippets.
    """
    try:
        test_type = request.test_type.lower().strip()
        if test_type not in {"unit", "ui"}:
            raise HTTPException(status_code=400, detail="test_type must be 'unit' or 'ui'")

        # Query RAG for context
        rag_context = query_rag(request.test_description, k=request.rag_top_k)

        # Build AppContext from RAG results
        code_snippets_text = "\n\n".join([
            f"// {snippet['kind']} from {snippet['path']}\n{snippet['content']}"
            for snippet in rag_context["code_snippets"]
        ])

        app_context = AppContext(
            app_name="SampleApp",  # Could be parameterized
            screens=rag_context["screens"],
            accessibility_ids=rag_context["accessibility_ids"],
            source_code_snippets=code_snippets_text if code_snippets_text else None
        )

        # Use the existing generate_test logic with RAG-enhanced context
        wrapped_request = TestGenerationRequest(
            test_description=request.test_description,
            test_type=test_type,
            app_context=app_context,
            class_name=request.class_name,
            include_comments=request.include_comments
        )

        response = await generate_test(wrapped_request)

        # Add RAG metadata to response
        response.metadata["rag_enabled"] = True
        response.metadata["rag_context"] = {
            "accessibility_ids_found": len(rag_context.get("accessibility_ids", [])),
            "screens_found": len(rag_context.get("screens", [])),
            "code_snippets_used": len(rag_context.get("code_snippets", [])),
            "total_docs_retrieved": rag_context.get("total_docs_retrieved", 0),
        }
        if "error" in rag_context:
            response.metadata["rag_error"] = rag_context["error"]

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating test with RAG: {str(e)}")


@app.post("/generate-tests-batch")
async def generate_tests_batch(requests: List[TestGenerationRequest]):
    results = []
    errors = []

    for idx, req in enumerate(requests):
        try:
            results.append(await generate_test(req))
        except Exception as e:
            errors.append(
                {"index": idx, "error": str(e), "description": (req.test_description or "")[:100]}
            )

    return {"generated": len(results), "failed": len(errors), "results": results, "errors": errors}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.HOST, port=config.PORT)
