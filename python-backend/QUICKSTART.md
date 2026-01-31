# Quick Start - PoC Test Generator

## Setup (5 minutes)

```bash
# 1. Navigate to python-backend
cd python-backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up API key
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here

# 5. Run server
python main.py
```

Server runs at: `http://localhost:8000`

## Test the API

### Using curl:

```bash
curl -X POST "http://localhost:8000/generate-test" \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

### Using the example file:

```bash
curl -X POST "http://localhost:8000/generate-test" \
  -H "Content-Type: application/json" \
  -d '{
    "test_description": "Test login with empty fields shows error and stays on login screen",
    "test_type": "ui",
    "app_context": {
      "accessibility_ids": ["login_email", "login_password", "login_button", "error_label", "login_screen"]
    }
  }'
```

### Check contract validation:

The response includes `contract_validation` in metadata:

```json
{
  "swift_code": "import XCTest...",
  "test_type": "ui",
  "class_name": "LoginTests",
  "metadata": {
    "contract_validation": {
      "has_xcuiapplication": true,
      "has_app_launch": true,
      "has_wait_for_existence": true,
      "has_assertions": true,
      "has_setup_teardown": true
    }
  }
}
```

## Enforced Contract (PoC)

Every generated XCUITest MUST have:

✅ `XCUIApplication()` - App instance
✅ `app.launch()` - Launch the app
✅ `waitForExistence(timeout:)` - Explicit waits
✅ Assertions (`XCTAssertTrue`, `XCTAssertEqual`, etc.)
✅ `setUpWithError` and `tearDownWithError` methods

The API validates and reports which requirements are met.

## Interactive Documentation

Visit: `http://localhost:8000/docs`

Try the API directly in your browser with Swagger UI!
