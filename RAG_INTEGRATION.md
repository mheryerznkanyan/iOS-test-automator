# RAG Integration for iOS Test Automation

## Overview

Successfully integrated RAG (Retrieval-Augmented Generation) with the iOS test automation system. Users can now describe tests in natural language and the system automatically retrieves relevant context from the codebase.

## What's Been Built

### 1. RAG Index
- **Location**: `python-rag/rag_store/`
- **Indexed**: 12 Swift files from SampleApp
- **Documents**: 35 total documents containing:
  - SwiftUI Views and UIKit ViewControllers
  - Accessibility identifiers
  - Buttons and interactive elements
  - Navigation patterns
  - Screen summaries

### 2. RAG Integration in Backend
- **File**: `python-backend/main.py`
- **New Endpoint**: `/generate-test-with-rag`
- **Features**:
  - Automatic context retrieval from codebase
  - Natural language test descriptions
  - Finds relevant screens, accessibility IDs, and code snippets
  - Graceful degradation if RAG fails

### 3. Test Infrastructure Fixed
- Fixed "Executed 0 tests" issue by adding `LLMGeneratedTest.swift` to Xcode project
- Tests now run successfully in simulator
- Video recording captures test execution

## How to Use

### Start the Backend Server

```bash
cd python-backend
python main.py
```

The server will start on `http://localhost:8000`

### Generate a Test with RAG

**Simple Example**:
```bash
curl -X POST 'http://localhost:8000/generate-test-with-rag' \
  -H 'Content-Type: application/json' \
  --data '{
    "test_description": "test login flow with email and password"
  }'
```

**Full Example**:
```bash
curl -X POST 'http://localhost:8000/generate-test-with-rag' \
  -H 'Content-Type: application/json' \
  --data '{
    "test_description": "I want to test the login flow. User should enter email test@example.com and password password123, tap login button, and see the items screen after successful login",
    "test_type": "ui",
    "class_name": "RAGGeneratedLoginTest"
  }'
```

## How It Works

1. **User provides natural language description**: "test login flow with email and password"

2. **RAG queries vector database**:
   - Searches for relevant code based on the description
   - Finds LoginView, LoginViewModel, AuthService
   - Extracts accessibility IDs: `emailTextField`, `passwordTextField`, `loginButton`

3. **Context building**:
   - Screens: [`LoginView`]
   - Accessibility IDs: [`appLogo`, `appTitle`, `demoCredentials`, `emailError`, `emailTextField`, `loginButton`, `loginError`, `passwordError`, `passwordTextField`]
   - Code snippets: LoginView structure, AuthService logic

4. **Test generation**:
   - LLM receives enriched context
   - Generates accurate XCUITest code with correct element IDs
   - Includes sleep delays for visual debugging

## Comparison: Before vs After RAG

### Before (Manual Context)
```json
{
  "test_description": "Test login",
  "app_context": {
    "accessibility_ids": ["emailTextField", "passwordTextField", "loginButton"]
  }
}
```
**Problem**: User had to manually specify all accessibility IDs

### After (RAG-Enhanced)
```json
{
  "test_description": "test login flow"
}
```
**Benefit**: System automatically finds all relevant IDs and context!

## API Endpoints

### 1. `/generate-test` (Original)
- Requires manual context specification
- Good for when you know exact element IDs

### 2. `/generate-test-with-rag` (New)
- Automatic context retrieval
- Natural language descriptions
- Recommended for most use cases

### 3. `/health`
Check if server is running:
```bash
curl http://localhost:8000/health
```

## Files Modified

1. **`python-backend/main.py`**:
   - Added RAG configuration
   - Added `get_vectorstore()` function
   - Added `query_rag()` function
   - Added `/generate-test-with-rag` endpoint

2. **`python-backend/requirements.txt`**:
   - Added `langchain-community==0.3.27`
   - Added `chromadb==0.5.23`
   - Added `sentence-transformers==3.0.1`
   - Updated `langchain-core` to 0.3.76 for compatibility

3. **`ios-app/src/SampleApp/SampleApp.xcodeproj/project.pbxproj`**:
   - Added `LLMGeneratedTest.swift` to build phases
   - Fixed test discovery issue

## Next Steps

### 1. Update RAG Index
Whenever you modify the SampleApp code:
```bash
cd python-rag
python ios_rag_mvp.py ingest \
  --app-dir ../ios-app/src/SampleApp/SampleApp \
  --persist ./rag_store \
  --collection sample_app
```

### 2. Test Different Scenarios
Try natural language descriptions for various flows:
- "test item list scrolling"
- "verify logout functionality"
- "test invalid login credentials"

### 3. Integrate with CI/CD
- Add RAG-enhanced test generation to automation pipeline
- Generate tests from feature descriptions
- Run generated tests in simulator

### 4. Extend to Other Apps
To use with a different iOS app:
```bash
# Build new RAG index
python ios_rag_mvp.py ingest \
  --app-dir /path/to/your/app \
  --persist ./rag_store_myapp \
  --collection myapp

# Update backend environment variable
export RAG_PERSIST_DIR="./rag_store_myapp"
export RAG_COLLECTION="myapp"
```

## Troubleshooting

### Server won't start
- Check Python dependencies: `pip install -r python-backend/requirements.txt`
- Verify ANTHROPIC_API_KEY is set in `.env`

### RAG returns empty context
- Rebuild the RAG index
- Check that Swift files have accessibility identifiers
- Verify RAG_PERSIST_DIR points to correct location

### Tests not found
- Ensure `LLMGeneratedTest.swift` is in Xcode project
- Check it's added to the SampleAppUITests target
- Clean and rebuild: `xcodebuild clean`

## Success Metrics

✅ RAG index built successfully (35 documents)
✅ Backend integration complete
✅ Test generation working
✅ Tests execute in simulator
✅ Video recording functional
✅ Xcode project fixed (tests discoverable)

## Architecture

```
┌─────────────────────┐
│ Natural Language    │
│ Test Description    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ RAG Query           │
│ (Vector Search)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Retrieved Context:  │
│ - Screens           │
│ - Accessibility IDs │
│ - Code Snippets     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ LLM (Claude 4.5)    │
│ + Context           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Generated XCUITest  │
│ Swift Code          │
└─────────────────────┘
```

## Credits

- **RAG Implementation**: `python-rag/ios_rag_mvp.py`
- **Backend Integration**: `python-backend/main.py`
- **Test Framework**: XCUITest
- **LLM**: Claude Sonnet 4.5
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
