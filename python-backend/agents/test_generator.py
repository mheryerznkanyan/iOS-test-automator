"""Test Generator class with LangChain integration"""
from typing import Dict, Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

from config import config
from prompts import XCTEST_SYSTEM_PROMPT, XCUITEST_SYSTEM_PROMPT
from requests_and_responses import TestGenerationRequest, TestGenerationResponse
from utils import (
    build_context_section,
    build_class_name_section,
    validate_xcuitest_contract,
    strip_code_fences,
    extract_class_name
)


class TestGenerator:
    """Test generator using LangChain and Claude"""

    def __init__(self):
        """Initialize the test generator with LangChain Anthropic chat model"""
        self.llm = ChatAnthropic(
            model=config.ANTHROPIC_MODEL,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.LLM_MAX_TOKENS,
            api_key=config.ANTHROPIC_API_KEY,
        )

    def run(self, request: TestGenerationRequest) -> TestGenerationResponse:
        """
        Generate a test based on the request.

        Args:
            request: TestGenerationRequest containing test description and context

        Returns:
            TestGenerationResponse with generated Swift code
        """
        test_type = request.test_type.lower().strip()
        if test_type not in {"unit", "ui"}:
            raise ValueError("test_type must be 'unit' or 'ui'")

        # Select appropriate prompt based on test type
        system_prompt = XCTEST_SYSTEM_PROMPT if test_type == "unit" else XCUITEST_SYSTEM_PROMPT
        default_class_name = "GeneratedUnitTests" if test_type == "unit" else "GeneratedUITests"

        # Build the prompt sections
        context_section = build_context_section(request.app_context)
        class_name_section = build_class_name_section(request.class_name)

        # Construct the user message
        user_message = f"""Generate a Swift {('XCTest unit test' if test_type == 'unit' else 'XCUITest UI test')} for the following:

Test Description: {request.test_description}

{context_section}

{class_name_section}

Include comments: {request.include_comments}

Output ONLY Swift code.
"""

        # Invoke the LLM with LangChain
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]

        ai_msg = self.llm.invoke(messages)
        swift_code = strip_code_fences(ai_msg.content)

        # Extract class name from generated code
        final_class_name = extract_class_name(swift_code, request.class_name or default_class_name)

        # Validate UI tests
        validation_results: Dict[str, Any] = {}
        if test_type == "ui":
            checks = validate_xcuitest_contract(swift_code)
            validation_results = {
                **checks,
                "all_passed": all(checks.values()),
                "failed_checks": [k for k, v in checks.items() if not v],
            }

        return TestGenerationResponse(
            swift_code=swift_code,
            test_type=test_type,
            class_name=final_class_name,
            metadata={
                "provider": "langchain_anthropic",
                "model": config.ANTHROPIC_MODEL,
                "has_context": bool(request.app_context),
                "context_provided": bool(context_section),
                "contract_validation": validation_results if test_type == "ui" else None,
            },
        )
