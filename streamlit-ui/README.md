# iOS Test Automator - Streamlit UI

A user-friendly web interface for generating and running iOS UI tests using natural language descriptions.

## Features

- 🤖 **Natural Language Test Generation**: Describe tests in plain English
- 🔍 **RAG-Powered**: Uses Retrieval-Augmented Generation to find correct accessibility IDs
- ▶️ **One-Click Execution**: Generate and run tests with a single click
- 📹 **Video Recording**: Automatically records simulator during test execution
- ⬇️ **Download Recordings**: Save video recordings of your tests
- 📊 **Real-time Results**: See test results, duration, and logs immediately
- 📝 **Test History**: Track all your test runs with status, outputs, and recordings
- 🎨 **Beautiful UI**: Clean, intuitive interface built with Streamlit
- 🚀 **Automated Workflow**: Boots simulator → Builds project → Records video → Runs test

## Prerequisites

1. **Backend server running** (python-backend)
2. **RAG store populated** (python-rag)
3. **Xcode project** (ios-app/src/SampleApp)
4. **iOS Simulator** configured and available

## Installation

1. Create a virtual environment:
```bash
cd streamlit-ui
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Start the Backend Server

First, make sure the backend is running:
```bash
cd ../python-backend
source venv/bin/activate
python main.py
```

The backend should be running on `http://localhost:8000`

### 2. Launch the Streamlit UI

```bash
cd streamlit-ui
source venv/bin/activate
streamlit run app.py
```

The UI will open in your browser at `http://localhost:8501`

### 3. Generate and Run Tests

1. **Enter Test Description**: Describe what you want to test in plain English
   - Example: "Test login with invalid credentials and verify error message appears"
   - Example: "Test adding a new item to the list"
   - Example: "Test logout functionality"

2. **Choose Action**:
   - **Generate Test**: Only generates the test code (doesn't run it)
   - **Generate & Run**: Generates test code and immediately runs it on the simulator

3. **View Results**:
   - Generated Swift code with syntax highlighting
   - RAG context metrics (accessibility IDs found, documents retrieved)
   - Test execution status (PASSED/FAILED)
   - Test duration
   - Full test output logs

4. **Check History**: View all previous test runs in the "Test History" tab

## Configuration

You can configure the UI using environment variables:

```bash
# Backend URL (default: http://localhost:8000)
export BACKEND_URL=http://localhost:8000

# Simulator ID (default: auto-detected iPhone 17)
export SIMULATOR_ID=5BFFD820-697B-4093-8969-74E617604232

# Simulator Name (default: iPhone 17)
export SIMULATOR_NAME="iPhone 17"
```

Or edit the configuration at the top of `app.py`:

```python
BACKEND_URL = "http://localhost:8000"
XCODE_PROJECT = "../ios-app/src/SampleApp/SampleApp.xcodeproj"
SIMULATOR_ID = "5BFFD820-697B-4093-8969-74E617604232"
```

## How It Works

1. **User Input**: You describe a test in natural language
2. **RAG Query**: The backend queries the RAG store to find relevant accessibility IDs and code snippets
3. **Test Generation**: Claude Sonnet 4.5 generates XCUITest Swift code using the RAG context
4. **File Save**: The generated test is saved to `SampleAppUITests/Generated/`
5. **Simulator Boot**: Automatically boots the iOS simulator
6. **Build**: Builds the project with `xcodebuild build-for-testing`
7. **Video Recording**: Starts recording the simulator screen using `xcrun simctl io recordVideo`
8. **Execution**: Runs the test on the simulator with `xcodebuild test`
9. **Video Stop**: Stops the recording and saves the video to `recordings/`
10. **Results**: Test results, logs, video playback, and download button are displayed

## Troubleshooting

### Backend Offline
**Error**: "❌ Backend Offline" in sidebar

**Solution**:
```bash
cd python-backend
source venv/bin/activate
python main.py
```

### RAG Not Finding IDs
**Error**: "0 Accessibility IDs Found"

**Solution**: Regenerate the RAG store:
```bash
cd python-rag
source .venv/bin/activate
python ios_rag_mvp.py ingest --app-dir ../ios-app/src/SampleApp --persist ./rag_store --collection sample_app
```

### Simulator Not Found
**Error**: "Unable to find a device matching the provided destination"

**Solution**: Check available simulators:
```bash
xcrun simctl list devices available
```

Update the `SIMULATOR_ID` in `app.py` with a valid simulator ID.

### Test Build Failed
**Error**: Build errors during test execution

**Solution**: Try building the project manually first:
```bash
cd ios-app/src/SampleApp
xcodebuild -project SampleApp.xcodeproj -scheme SampleApp -destination 'platform=iOS Simulator,id=YOUR_SIMULATOR_ID' build-for-testing
```

## Example Test Descriptions

Here are some example test descriptions you can try:

- "Test login with valid credentials and verify successful login"
- "Test login with empty email field and verify validation error"
- "Test adding a new item to the list"
- "Test deleting an item from the list"
- "Test editing an existing item"
- "Test logout functionality"
- "Test profile screen displays user information"
- "Test navigation from home to profile screen"

## Architecture

```
streamlit-ui/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── run.sh             # Startup script
├── recordings/        # Video recordings directory (auto-created)
└── README.md          # This file

Flow:
User → Streamlit UI → Backend API → RAG Store → Claude → Generated Test
  ↓
Boot Simulator → Build Project → Start Recording → Run Test → Stop Recording
  ↓
Display Results + Video Playback + Download Button
```

## Tips

- Use descriptive test names for better organization
- Check the "Test History" tab to review previous runs and watch recordings
- View full test output logs for debugging failed tests
- The RAG context metrics show how much relevant information was found
- Tests are automatically saved to the `Generated/` folder
- Video recordings are saved to `streamlit-ui/recordings/` with timestamps
- Download videos to share test results with your team
- Videos are useful for debugging UI issues and documenting test behavior

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs: `python-backend/backend.log`
3. Check xcodebuild output in the test results

---

Built with ❤️ using Streamlit, Claude Sonnet 4.5, and RAG
