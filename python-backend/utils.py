"""Utility functions for the iOS Test Generator API"""
from typing import Optional, List, Dict, Any

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from config import config
from requests_and_responses import AppContext

# Initialize RAG vector store (lazy loading)
_vectorstore: Optional[Chroma] = None


def build_context_section(app_context: Optional[AppContext]) -> str:
    """Build the context section for the prompt from AppContext"""
    if not app_context:
        return ""

    sections: List[str] = []

    if app_context.app_name:
        sections.append(f"App Name: {app_context.app_name}")

    if app_context.screens:
        sections.append(f"Available Screens: {', '.join(app_context.screens)}")

    if app_context.ui_elements:
        elements_str = "\n".join(
            [f"  {screen}: {', '.join(elements)}" for screen, elements in app_context.ui_elements.items()]
        )
        sections.append(f"UI Elements:\n{elements_str}")

    if app_context.accessibility_ids:
        sections.append(f"Accessibility IDs: {', '.join(app_context.accessibility_ids)}")

    if app_context.custom_types:
        sections.append(f"Custom Types: {', '.join(app_context.custom_types)}")

    if app_context.source_code_snippets:
        # Keep raw Swift snippet without markdown fences (models sometimes echo fences back)
        sections.append(f"Relevant Code:\n{app_context.source_code_snippets}")

    return "App Context:\n" + "\n\n".join(sections) if sections else ""


def build_class_name_section(class_name: Optional[str]) -> str:
    """Build the class name section for the prompt"""
    return f"Test Class Name: {class_name}" if class_name else (
        "Generate an appropriate test class name based on the test description."
    )


def validate_xcuitest_contract(swift_code: str) -> Dict[str, bool]:
    """Validate that the generated XCUITest code meets required standards"""
    return {
        "has_xcuiapplication": "XCUIApplication()" in swift_code,
        "has_app_launch": "app.launch()" in swift_code,
        "has_wait_for_existence": "waitForExistence(timeout:" in swift_code or "XCTNSPredicateExpectation" in swift_code,
        "has_assertions": any(x in swift_code for x in ["XCTAssertTrue", "XCTAssertEqual", "XCTAssertFalse", "XCTAssertNotNil"]),
        "has_setup_teardown": "setUpWithError" in swift_code and "tearDownWithError" in swift_code,
    }


def strip_code_fences(swift_code: str) -> str:
    """Remove markdown code fences from generated code"""
    s = swift_code.strip()
    if s.startswith("```swift"):
        s = s[len("```swift"):].strip()
    if s.startswith("```"):
        s = s[len("```"):].strip()
    if s.endswith("```"):
        s = s[:-3].strip()
    return s


def extract_class_name(swift_code: str, fallback: str) -> str:
    """Extract the test class name from generated Swift code"""
    # Handles "final class X: XCTestCase" and "class X: XCTestCase"
    for line in swift_code.splitlines():
        if "class " in line and ": XCTestCase" in line:
            try:
                after = line.split("class ", 1)[1]
                name = after.split(":", 1)[0].strip()
                if name:
                    return name
            except Exception:
                pass
    return fallback


def get_vectorstore() -> Chroma:
    """Lazy-load the RAG vector store"""
    global _vectorstore
    if _vectorstore is None:
        embeddings = HuggingFaceEmbeddings(model_name=config.RAG_EMBED_MODEL)
        _vectorstore = Chroma(
            collection_name=config.RAG_COLLECTION,
            embedding_function=embeddings,
            persist_directory=config.RAG_PERSIST_DIR,
        )
    return _vectorstore


def query_rag(test_description: str, k: int = None) -> Dict[str, Any]:
    """
    Query the RAG system for relevant context based on the test description.
    Returns accessibility IDs, code snippets, and screen information.
    """
    if k is None:
        k = config.RAG_TOP_K

    try:
        vs = get_vectorstore()
        docs = vs.similarity_search(test_description, k=k)

        # Extract relevant information from retrieved documents
        accessibility_ids = set()
        screens = set()
        code_snippets = []

        for doc in docs:
            meta = doc.metadata

            # Collect accessibility IDs
            if "accessibility_ids" in meta:
                ids = meta["accessibility_ids"]
                if ids:
                    accessibility_ids.update(ids.split("|"))

            # Collect screen names
            if "screen" in meta and meta["screen"]:
                screens.add(meta["screen"])

            # Collect code snippets (prioritize SwiftUI views and accessibility maps)
            kind = meta.get("kind", "")
            if kind in ["swiftui_view", "accessibility_map", "screen_card"]:
                code_snippets.append({
                    "kind": kind,
                    "path": meta.get("path", ""),
                    "screen": meta.get("screen", ""),
                    "content": doc.page_content[:500]  # Limit snippet length
                })

        return {
            "accessibility_ids": sorted(list(accessibility_ids)),
            "screens": sorted(list(screens)),
            "code_snippets": code_snippets[:5],  # Top 5 most relevant
            "total_docs_retrieved": len(docs)
        }
    except Exception as e:
        # If RAG fails, return empty context (graceful degradation)
        return {
            "accessibility_ids": [],
            "screens": [],
            "code_snippets": [],
            "total_docs_retrieved": 0,
            "error": str(e)
        }
