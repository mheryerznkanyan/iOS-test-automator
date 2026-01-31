# iOS Test Generator Backend

LLM-powered test generation service using FastAPI and LangChain with Claude AI.

## Features

- Generate XCTest unit tests from natural language
- Generate XCUITest UI tests from natural language
- Support for app context (UI elements, accessibility IDs, screens)
- Batch test generation
- RESTful API with OpenAPI documentation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

3. Run the server:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### `POST /generate-test`

Generate a single test from natural language description.

**Request Body:**
```json
{
  "test_description": "Test that user can login with valid credentials",
  "test_type": "ui",
  "app_context": {
    "app_name": "MyApp",
    "screens": ["LoginScreen", "HomeScreen"],
    "ui_elements": {
      "LoginScreen": ["emailField", "passwordField", "loginButton"]
    },
    "accessibility_ids": ["email_input", "password_input", "login_btn"]
  },
  "class_name": "LoginTests",
  "include_comments": true
}
```

**Response:**
```json
{
  "swift_code": "import XCTest\n\nfinal class LoginTests: XCTestCase { ... }",
  "test_type": "ui",
  "class_name": "LoginTests",
  "metadata": {
    "model": "claude-sonnet-4-5-20250929",
    "has_context": true
  }
}
```

### `POST /generate-tests-batch`

Generate multiple tests in one request.

### `GET /health`

Health check endpoint.

## Usage Examples

### Basic UI Test
```bash
curl -X POST "http://localhost:8000/generate-test" \
  -H "Content-Type: application/json" \
  -d '{
    "test_description": "Test login flow with valid credentials",
    "test_type": "ui"
  }'
```

### With App Context
```bash
curl -X POST "http://localhost:8000/generate-test" \
  -H "Content-Type: application/json" \
  -d '{
    "test_description": "Verify that tapping the login button with empty fields shows an error",
    "test_type": "ui",
    "app_context": {
      "ui_elements": {
        "LoginScreen": ["emailTextField", "passwordTextField", "loginButton", "errorLabel"]
      },
      "accessibility_ids": ["login_email", "login_password", "login_submit", "login_error"]
    }
  }'
```

### Unit Test
```bash
curl -X POST "http://localhost:8000/generate-test" \
  -H "Content-Type: application/json" \
  -d '{
    "test_description": "Test that UserValidator correctly validates email format",
    "test_type": "unit",
    "app_context": {
      "source_code_snippets": "struct UserValidator {\n  func isValidEmail(_ email: String) -> Bool\n}"
    }
  }'
```

## Architecture

```
┌─────────────────┐
│  Swift CLI      │
│  (testautomator)│
└────────┬────────┘
         │ HTTP Request
         │ (test description + context)
         ▼
┌─────────────────┐
│  FastAPI Server │
│  (this service) │
└────────┬────────┘
         │ LangChain
         │ + Prompts
         ▼
┌─────────────────┐
│  Claude API     │
│  (Anthropic)    │
└────────┬────────┘
         │ Generated
         │ Swift Code
         ▼
┌─────────────────┐
│  Response       │
│  (XCTest/       │
│   XCUITest)     │
└─────────────────┘
```

## How It Solves the App Context Problem

The service accepts an `app_context` object that can include:

1. **UI Elements**: List of buttons, fields, labels by screen
2. **Accessibility IDs**: Known identifiers for XCUITest queries
3. **Screens**: Available view controllers/screens
4. **Source Code**: Relevant Swift code snippets for unit tests
5. **Custom Types**: Custom UI components or models

This context is injected into the LLM prompt, allowing Claude to generate tests that:
- Use correct element identifiers
- Reference actual screens and UI components
- Generate appropriate Swift code for your specific app

## Tips for Better Results

1. **Provide specific accessibility IDs** - The LLM will use them in queries
2. **Include screen names** - Helps with navigation tests
3. **Add source code snippets** - For unit tests of specific classes
4. **Be descriptive** - Better test descriptions = better generated code
5. **Use lower temperature** - Already set to 0.3 for consistent code generation

## Development

Run with auto-reload:
```bash
uvicorn main:app --reload
```

Run tests (when added):
```bash
pytest
```
