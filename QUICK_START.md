# iOS Test Automator - Quick Start Guide

## What You Have

A complete **RAG-enhanced iOS test automation pipeline** that:
- Takes natural language test descriptions
- Automatically retrieves relevant context from your codebase
- Generates Swift XCUITest code using Claude
- Executes tests in iOS Simulator
- Records video of test execution

## Quick Start (3 Steps)

### 1. Start the Backend Server

```bash
cd python-backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Check Readiness

```bash
./check_pipeline_ready.sh
```

If all checks pass:
```
✅ ALL CHECKS PASSED
Ready to run the full pipeline!
```

### 3. Run the Full Pipeline

```bash
./test_full_pipeline_with_rag.sh
```

Watch the Simulator window! You'll see:
- App launches
- Login screen appears
- Email and password fields filled
- Login button tapped
- Navigation to Items screen

## What Happens

```
Input: Natural Language
   ↓
"I want to test the login flow. Enter email test@example.com
and password password123, tap login, verify Items tab appears"
   ↓
RAG Retrieval (automatic)
   ↓
Found: emailTextField, passwordTextField, loginButton, itemsTab
Found: LoginView, ItemsView screens
Found: AuthService code snippets
   ↓
LLM Generation (Claude Sonnet 4.5)
   ↓
Generated: Complete XCUITest Swift code
   ↓
Build & Execute
   ↓
Output: Video + Test Results
```

## Output Files

After running, you get:

1. **LLMGeneratedTest.swift** - Generated test code
2. **test_output.log** - Complete test logs
3. **test_recording.mp4** - Video of execution

## Key Features

### 1. RAG-Enhanced Context (No Manual Work!)

**Before RAG:**
```json
{
  "test_description": "Test login",
  "app_context": {
    "accessibility_ids": ["emailTextField", "passwordTextField", "loginButton"]
  }
}
```
❌ You had to know and specify all IDs manually

**With RAG:**
```json
{
  "test_description": "Test login flow with email and password"
}
```
✅ RAG automatically finds all relevant IDs, screens, and code!

### 2. Natural Language Input

Just describe what you want to test:
- "Test login with valid credentials"
- "Verify logout functionality"
- "Test item list scrolling"
- "Check error message for invalid email"

### 3. Automatic Context Retrieval

RAG searches your codebase and finds:
- **Accessibility IDs**: All relevant element identifiers
- **Screens**: View controllers and SwiftUI views
- **Code Patterns**: How elements are structured
- **Navigation**: Flow between screens

### 4. High-Quality Test Generation

Generated tests include:
- Proper XCUITest structure
- Wait conditions (`waitForExistence`)
- Assertions for verification
- Error handling
- Visual delays (sleep) for debugging
- Comments explaining each step

## Customizing Tests

### Edit Test Description

In [test_full_pipeline_with_rag.sh](test_full_pipeline_with_rag.sh), modify the `TEST_REQUEST`:

```bash
TEST_REQUEST='{
  "test_description": "YOUR TEST HERE",
  "test_type": "ui",
  "class_name": "YourTestName"
}'
```

### Example Test Descriptions

**Valid Login:**
```
"Test successful login: enter test@example.com and password123,
tap login, verify Items screen appears"
```

**Invalid Login:**
```
"Test login with wrong password: enter test@example.com and
wrongpassword, tap login, verify error message appears"
```

**Logout:**
```
"Test logout: tap logout button, verify return to login screen"
```

**Item Interaction:**
```
"Test item list: scroll through items, tap first item,
verify detail screen shows"
```

## API Endpoints

### 1. RAG-Enhanced Generation (Recommended)

```bash
curl -X POST 'http://localhost:8000/generate-test-with-rag' \
  -H 'Content-Type: application/json' \
  -d '{
    "test_description": "test login flow with email and password",
    "test_type": "ui"
  }'
```

**Benefits:**
- Automatic context retrieval
- Just natural language needed
- Finds all relevant code

### 2. Manual Context Generation

```bash
curl -X POST 'http://localhost:8000/generate-test' \
  -H 'Content-Type: application/json' \
  -d '{
    "test_description": "test login",
    "test_type": "ui",
    "app_context": {
      "accessibility_ids": ["emailTextField", "passwordTextField"]
    }
  }'
```

**When to use:**
- You know exact element IDs
- Testing specific edge cases
- RAG index not available

## Project Structure

```
iOS-test-automator/
├── python-backend/           # FastAPI backend
│   ├── main.py              # API endpoints + RAG integration
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # ANTHROPIC_API_KEY
│
├── python-rag/              # RAG system
│   ├── ios_rag_mvp.py       # RAG indexing and querying
│   └── rag_store/           # ChromaDB vector store
│
├── ios-app/                 # iOS application
│   └── src/SampleApp/
│       ├── SampleApp/       # App source code
│       └── SampleAppUITests/
│           └── LLMGeneratedTest.swift  # Generated tests
│
├── test_full_pipeline_with_rag.sh  # Full pipeline runner
├── check_pipeline_ready.sh         # Readiness check
├── FULL_PIPELINE_GUIDE.md         # Detailed guide
├── RAG_INTEGRATION.md             # RAG documentation
└── QUICK_START.md                 # This file
```

## Troubleshooting

### Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'langchain_anthropic'`

**Solution:**
```bash
cd python-backend
pip install -r requirements.txt
```

### No API Key

**Error:** `ANTHROPIC_API_KEY not set`

**Solution:**
```bash
# Create .env file in python-backend/
echo "ANTHROPIC_API_KEY=your-key-here" > python-backend/.env
```

### RAG Returns Empty Context

**Error:** RAG finds 0 accessibility IDs

**Solution:** Rebuild the RAG index:
```bash
cd python-rag
python ios_rag_mvp.py ingest \
  --app-dir ../ios-app/src/SampleApp/SampleApp \
  --persist ./rag_store \
  --collection sample_app
```

### Simulator Not Found

**Error:** `Device 'iPhone 17' not found`

**Solution:**
```bash
# List available devices
xcrun simctl list devices | grep iPhone

# Update DEVICE variable in script to match available device
```

### Build Fails

**Solution:**
```bash
# Open in Xcode to see detailed errors
open ios-app/src/SampleApp/SampleApp.xcodeproj

# Clean build
cd ios-app/src/SampleApp
xcodebuild clean -project SampleApp.xcodeproj -scheme SampleApp
```

## Advanced Usage

### Update RAG Index

When you modify your iOS app code:

```bash
cd python-rag
python ios_rag_mvp.py ingest \
  --app-dir ../ios-app/src/SampleApp/SampleApp \
  --persist ./rag_store \
  --collection sample_app
```

### Use Different App

To test a different iOS app:

```bash
# 1. Build RAG index for your app
cd python-rag
python ios_rag_mvp.py ingest \
  --app-dir /path/to/your/app \
  --persist ./rag_store_myapp \
  --collection myapp

# 2. Update backend environment
export RAG_PERSIST_DIR="./rag_store_myapp"
export RAG_COLLECTION="myapp"

# 3. Update script paths
# Edit test_full_pipeline_with_rag.sh
# Change PROJECT_DIR to your app's path
```

### Retrieve More Context

Increase RAG retrieval for complex tests:

```json
{
  "test_description": "complex multi-screen flow",
  "test_type": "ui",
  "rag_top_k": 20
}
```

## Performance Tips

### Fast Iteration

For quick test iterations:

```bash
# Just test generation (no execution)
curl -X POST 'http://localhost:8000/generate-test-with-rag' \
  -H 'Content-Type: application/json' \
  -d '{"test_description": "your test"}' | jq .
```

### Parallel Testing

Run multiple test generations in parallel:

```bash
# Generate different tests simultaneously
curl -X POST ... &
curl -X POST ... &
wait
```

### Cache RAG Results

The RAG vector store is loaded once and cached, making subsequent queries fast.

## What's Next?

### 1. Try Different Scenarios

Edit the test description and run different flows:
- Login variations (valid, invalid, empty fields)
- Navigation flows
- Form submissions
- List interactions

### 2. Inspect Generated Code

Learn from the generated tests:
```bash
cat ios-app/src/SampleApp/SampleAppUITests/LLMGeneratedTest.swift
```

### 3. Improve RAG Index

Add more files or update when code changes:
```bash
cd python-rag
python ios_rag_mvp.py ingest ...
```

### 4. Integrate into CI/CD

Automate test generation and execution:
```yaml
# .github/workflows/test.yml
- name: Generate and run tests
  run: ./test_full_pipeline_with_rag.sh
```

## Resources

- **Full Guide**: [FULL_PIPELINE_GUIDE.md](FULL_PIPELINE_GUIDE.md)
- **RAG Details**: [RAG_INTEGRATION.md](RAG_INTEGRATION.md)
- **Backend Code**: [python-backend/main.py](python-backend/main.py)
- **RAG Implementation**: [python-rag/ios_rag_mvp.py](python-rag/ios_rag_mvp.py)

## Architecture Summary

```
┌─────────────────────────────────────────────────────┐
│                 Natural Language                    │
│        "Test login with email and password"         │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              RAG Vector Search                      │
│    (ChromaDB + sentence-transformers)               │
│  Searches: Swift files, SwiftUI views, UIKit VCs    │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│           Retrieved Context (Automatic)             │
│  • Accessibility IDs: [emailTextField, ...]         │
│  • Screens: [LoginView, ItemsView]                  │
│  • Code snippets: LoginView.swift, AuthService.swift│
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│         LLM Generation (Claude Sonnet 4.5)          │
│     Prompt = System + Description + RAG Context     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│           Generated Swift XCUITest                  │
│  • Proper XCUIApplication setup                     │
│  • Element queries with accessibility IDs           │
│  • Wait conditions (waitForExistence)               │
│  • Assertions and verifications                     │
│  • Visual delays (sleep) for debugging              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Xcode Build & Execute                  │
│  1. Save to LLMGeneratedTest.swift                  │
│  2. xcodebuild build-for-testing                    │
│  3. Boot iOS Simulator                              │
│  4. Start video recording                           │
│  5. xcodebuild test                                 │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                   Results                           │
│  • test_output.log (PASSED/FAILED)                  │
│  • test_recording.mp4 (video)                       │
│  • LLMGeneratedTest.swift (code)                    │
└─────────────────────────────────────────────────────┘
```

## Success Criteria

After running the pipeline, you should have:

- ✅ Backend responding with RAG context
- ✅ 5+ accessibility IDs retrieved automatically
- ✅ 2+ screens identified
- ✅ Swift test code generated (100+ lines)
- ✅ Contract validation passed (XCUIApplication, app.launch, etc.)
- ✅ Build successful
- ✅ Test executed in simulator
- ✅ Video recording saved
- ✅ Test result (PASSED/FAILED) shown

## Support

Issues? Check:
1. [FULL_PIPELINE_GUIDE.md](FULL_PIPELINE_GUIDE.md) - Detailed troubleshooting
2. [RAG_INTEGRATION.md](RAG_INTEGRATION.md) - RAG-specific issues
3. Backend logs - Check terminal running `python main.py`
4. Xcode - Open project for detailed build errors

---

**Ready to get started?**

```bash
# 1. Check you're ready
./check_pipeline_ready.sh

# 2. Run the pipeline
./test_full_pipeline_with_rag.sh

# 3. Watch the Simulator and enjoy! 🎉
```
