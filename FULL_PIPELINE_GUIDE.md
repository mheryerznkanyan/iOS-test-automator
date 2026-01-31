# Full Pipeline Testing Guide

## Overview

This guide walks you through testing the complete iOS test automation pipeline with RAG integration.

## What Gets Tested

The full pipeline includes:

1. **RAG-Enhanced Test Generation** - Natural language → Swift test code
2. **iOS Simulator Management** - Boot and prepare simulator
3. **Project Build** - Compile the app and tests
4. **Test Execution** - Run tests in simulator
5. **Video Recording** - Capture the test execution
6. **Results Analysis** - Parse and display results

## Prerequisites

### 1. Backend Server Must Be Running

```bash
cd python-backend
python main.py
```

Verify it's running:
```bash
curl http://localhost:8000/health
```

### 2. RAG Index Must Exist

The RAG vector store should be at: `python-rag/rag_store/`

If not, build it:
```bash
cd python-rag
python ios_rag_mvp.py ingest \
  --app-dir ../ios-app/src/SampleApp/SampleApp \
  --persist ./rag_store \
  --collection sample_app
```

### 3. iOS Simulator Available

Check available simulators:
```bash
xcrun simctl list devices | grep iPhone
```

The script uses "iPhone 17" by default. Update the `DEVICE` variable if needed.

## Running the Full Pipeline

### Quick Start

```bash
./test_full_pipeline_with_rag.sh
```

### What Happens

```
[0/5] Preparing iOS Simulator
  - Shutdown all simulators
  - Boot iPhone 17
  - Open Simulator window
  - Verify device is ready

[1/5] Generating test code via RAG endpoint
  - Send natural language description to /generate-test-with-rag
  - RAG retrieves relevant accessibility IDs, screens, code snippets
  - LLM generates Swift XCUITest code
  - Save to LLMGeneratedTest.swift
  - Show retrieved context and validation results

[2/5] Building project
  - Clean build
  - Build for testing
  - Target: SampleApp (UI Tests)

[3/5] Running UI tests in Simulator
  - Start video recording
  - Bring Simulator to foreground
  - Execute the generated test
  - Capture output to test_output.log

[4/5] Test Results
  - Parse test results (PASSED/FAILED)
  - Show test summary

[5/5] Summary
  - Display RAG context statistics
  - List generated files
  - Show next steps
```

## Output Files

After running, you'll have:

- **LLMGeneratedTest.swift** - Generated test code
- **test_output.log** - Complete test execution logs
- **test_recording.mp4** - Video of test execution in simulator

## Example Test Description

The script uses this natural language description:

```
"I want to test the login flow. User should enter email test@example.com
and password password123, tap login button, and verify successful login
by checking for the Items tab"
```

RAG automatically finds:
- Accessibility IDs: `emailTextField`, `passwordTextField`, `loginButton`, `itemsTab`
- Screens: `LoginView`, `ItemsView`
- Code snippets: LoginView structure, AuthService logic

## Customizing the Test

Edit the `TEST_REQUEST` variable in the script:

```bash
TEST_REQUEST='{
  "test_description": "YOUR NATURAL LANGUAGE DESCRIPTION HERE",
  "test_type": "ui",
  "class_name": "YourTestClassName"
}'
```

### Example Descriptions

**Login Flow:**
```
"Test login with valid credentials and verify Items screen appears"
```

**Logout Flow:**
```
"Test logout functionality - tap logout button and verify return to login screen"
```

**Invalid Credentials:**
```
"Test login with invalid credentials and verify error message appears"
```

**Item List:**
```
"Test scrolling through the item list and tapping on an item"
```

## RAG Context Information

The script shows what RAG found:

```json
{
  "accessibility_ids": 9,        // Number of IDs found
  "screens": 2,                  // Number of screens identified
  "code_snippets": 5,            // Snippets used for context
  "docs_retrieved": 10           // Total documents searched
}
```

## Troubleshooting

### Backend Not Running

```
❌ Backend server is not running!
```

**Solution:**
```bash
cd python-backend
python main.py
```

### Simulator Not Found

```
❌ Device 'iPhone 17' not found
```

**Solution:**
List available devices and update `DEVICE` variable:
```bash
xcrun simctl list devices | grep iPhone
```

### Build Failures

**Solution:**
Open Xcode and build manually to see detailed errors:
```bash
open ios-app/src/SampleApp/SampleApp.xcodeproj
```

### Tests Not Found

```
⚠️ Could not extract test method name
```

**Solution:**
Check the generated test file has proper test methods:
```bash
cat ios-app/src/SampleApp/SampleAppUITests/LLMGeneratedTest.swift | grep "func test"
```

### RAG Returns Empty Context

**Solution:**
Rebuild the RAG index:
```bash
cd python-rag
python ios_rag_mvp.py ingest \
  --app-dir ../ios-app/src/SampleApp/SampleApp \
  --persist ./rag_store \
  --collection sample_app
```

## Advanced Usage

### Different Device

```bash
# Edit the script or set environment variable
export TEST_DEVICE="iPhone 15 Pro"
# Then update DEVICE variable in script
```

### Custom Test File Location

Edit `TEST_FILE` variable in the script:
```bash
TEST_FILE="$PROJECT_DIR/SampleAppUITests/MyCustomTest.swift"
```

### More RAG Documents

Increase the number of RAG documents retrieved by modifying the request:
```json
{
  "test_description": "...",
  "test_type": "ui",
  "class_name": "...",
  "rag_top_k": 15
}
```

## Comparison: With vs Without RAG

### Without RAG (Manual)

```bash
curl -X POST 'http://localhost:8000/generate-test' \
  -H 'Content-Type: application/json' \
  -d '{
    "test_description": "Test login",
    "test_type": "ui",
    "app_context": {
      "accessibility_ids": ["emailTextField", "passwordTextField", "loginButton"]
    }
  }'
```

**You must manually specify:**
- All accessibility IDs
- Screen names
- UI element structure

### With RAG (Automatic)

```bash
curl -X POST 'http://localhost:8000/generate-test-with-rag' \
  -H 'Content-Type: application/json' \
  -d '{
    "test_description": "Test login flow with email and password",
    "test_type": "ui"
  }'
```

**RAG automatically finds:**
- All relevant accessibility IDs from codebase
- Screen names and structure
- Code patterns and navigation

## Pipeline Architecture

```
┌──────────────────────────┐
│ Natural Language Input   │
│ "test login flow"        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ RAG Vector Search        │
│ (ChromaDB + Embeddings)  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Retrieved Context:       │
│ - Accessibility IDs      │
│ - Screen structures      │
│ - Code snippets          │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ LLM (Claude Sonnet 4.5)  │
│ + Retrieved Context      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Generated Swift Test     │
│ (XCUITest)               │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Save to Test File        │
│ LLMGeneratedTest.swift   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Xcode Build              │
│ (build-for-testing)      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ iOS Simulator            │
│ - Boot device            │
│ - Start video recording  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Execute Test             │
│ (xcodebuild test)        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Results & Video          │
│ - test_output.log        │
│ - test_recording.mp4     │
└──────────────────────────┘
```

## Success Metrics

After running the pipeline, you should see:

- ✅ Backend server responding
- ✅ Simulator booted and visible
- ✅ RAG context retrieved (>0 accessibility IDs, screens)
- ✅ Swift test code generated
- ✅ Project built successfully
- ✅ Test executed in simulator
- ✅ Video recording saved
- ✅ Test results parsed (PASSED/FAILED)

## Next Steps

1. **Try Different Test Scenarios**
   - Edit the test description in the script
   - Run different user flows

2. **Analyze the Generated Code**
   - Review the Swift test code
   - Understand how RAG context influenced generation

3. **Improve RAG Index**
   - Add more Swift files to the index
   - Update index when codebase changes

4. **Integrate into CI/CD**
   - Automate test generation from feature descriptions
   - Run tests automatically on commits

## Related Files

- **Backend**: `python-backend/main.py`
- **RAG**: `python-rag/ios_rag_mvp.py`
- **Integration Docs**: `RAG_INTEGRATION.md`
- **Original Pipeline**: `generate_and_run_test.sh`
