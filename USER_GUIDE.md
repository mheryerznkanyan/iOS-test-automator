# iOS Test Automator - User Guide

Welcome to iOS Test Automator! This guide will help you get started with automated iOS testing using natural language and AI.

## Table of Contents

1. [What is iOS Test Automator?](#what-is-ios-test-automator)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Using the Tool](#using-the-tool)
5. [Common Use Cases](#common-use-cases)
6. [Tips & Best Practices](#tips--best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## What is iOS Test Automator?

iOS Test Automator is an AI-powered tool that helps you create and run iOS tests without writing code. Simply describe what you want to test in plain English, and the tool will:

✨ **Generate** Swift test code automatically
🔍 **Find** the right UI elements in your app
▶️ **Execute** tests on iOS Simulator
📹 **Record** video of test execution
📊 **Show** detailed test results

### Key Features

- **Natural Language Input**: Describe tests like "Login with valid email and password"
- **Smart Context Retrieval**: Automatically finds accessibility IDs and UI elements
- **Instant Execution**: Run tests immediately in iOS Simulator
- **Video Recordings**: Watch exactly what happened during the test
- **Web Interface**: Beautiful UI, no terminal needed
- **AI-Powered**: Uses Claude Sonnet 4.5 for intelligent test generation

---

## Installation

### Option 1: Homebrew (Recommended)

```bash
# Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install iOS Test Automator
brew tap yourusername/tap
brew install ios-test-automator

# Initialize
ios-test-automator init
```

### Option 2: Direct Install

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/iOS-test-automator/main/install.sh | bash
```

### Prerequisites

Before installing, make sure you have:

- ✅ macOS 14.0 or later
- ✅ Xcode 15.0 or later
- ✅ An Anthropic API key ([Get one here](https://console.anthropic.com/))

---

## Getting Started

### Step 1: Configure Your API Key

After installation, add your Anthropic API key:

```bash
# Open the config file
ios-test-automator config
```

Or edit it manually:

```bash
nano ~/.ios-test-automator/.env
```

Add your API key:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Step 2: Index Your iOS App

The tool needs to understand your app's structure. Index your iOS app codebase:

```bash
ios-test-automator rag ingest --app-dir /path/to/your/ios/app
```

**Example:**

```bash
# If your app is in ~/Projects/MyApp/Sources
ios-test-automator rag ingest --app-dir ~/Projects/MyApp/Sources
```

This will scan your code and find all UI elements, screens, and accessibility IDs.

### Step 3: Start the Services

Open **two terminal windows**:

**Terminal 1 - Backend Server:**
```bash
ios-test-automator server
```

Wait for: `INFO: Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Web Interface:**
```bash
ios-test-automator ui
```

Wait for: `You can now view your Streamlit app in your browser`

### Step 4: Open the Web Interface

Open your browser to: **http://localhost:8501**

🎉 You're ready to create tests!

---

## Using the Tool

### Creating Your First Test

1. **Open the UI** at http://localhost:8501

2. **Describe your test** in plain English:
   ```
   Test login with email test@example.com and password password123,
   verify the home screen appears
   ```

3. **Click "Generate & Run"**

4. **Watch the magic happen**:
   - Test code is generated
   - iOS Simulator opens
   - App launches automatically
   - Test executes
   - Video is recorded
   - Results are shown

### Understanding the Results

After the test runs, you'll see:

#### ✅ Test Status
- **PASSED** - Test completed successfully
- **FAILED** - Test failed (check logs for details)

#### 📊 Test Details
- **Duration**: How long the test took
- **RAG Context**: What UI elements were found
- **Generated Code**: The Swift test code created

#### 📹 Video Recording
- Watch the test execution
- Download the recording
- Share with your team

#### 📝 Test Logs
- Detailed execution logs
- Error messages (if any)
- Build output

---

## Common Use Cases

### 1. Login Flow Testing

**Test Description:**
```
Test successful login: Enter email test@example.com and password password123,
tap login, verify the home screen appears with "Welcome" text
```

**What happens:**
- Enters email in email field
- Enters password in password field
- Taps login button
- Verifies home screen loaded
- Checks for "Welcome" text

---

### 2. Form Validation

**Test Description:**
```
Test login with invalid email: Enter "notanemail" in email field,
tap login, verify error message shows "Invalid email format"
```

**What happens:**
- Enters invalid email
- Taps login
- Checks for error message
- Verifies correct error text

---

### 3. Navigation Testing

**Test Description:**
```
Test navigation: Tap on Settings tab, verify Settings screen appears,
tap Profile button, verify Profile screen appears
```

**What happens:**
- Taps Settings tab
- Verifies Settings screen
- Taps Profile button
- Verifies Profile screen

---

### 4. List Interaction

**Test Description:**
```
Test scrolling items list: Scroll to bottom of items list,
tap on the first item, verify item detail screen appears
```

**What happens:**
- Scrolls through list
- Taps first item
- Verifies detail screen

---

### 5. Logout Testing

**Test Description:**
```
Test logout: Tap logout button in settings,
verify return to login screen
```

**What happens:**
- Finds and taps logout
- Verifies login screen appears

---

## Tips & Best Practices

### Writing Good Test Descriptions

✅ **DO:**
- Be specific: "Tap the blue Login button"
- Include expected results: "verify Home screen appears"
- Use actual text/values: "enter test@example.com"
- Describe step-by-step

❌ **DON'T:**
- Be vague: "test the app"
- Skip verifications: "tap login" (without checking result)
- Use complex logic: "if X then Y else Z"
- Assume context: "tap it" (tap what?)

### Good Examples

```
✅ Test login with valid credentials: Enter email "john@example.com",
   enter password "Secret123", tap Login button, verify Dashboard screen
   appears with text "Welcome, John"

✅ Test adding item to cart: Tap first product in list, tap "Add to Cart"
   button, verify cart badge shows "1", verify success message appears

✅ Test search functionality: Enter "iPhone" in search field, tap Search
   button, verify results screen shows at least one item with "iPhone" in title
```

### Performance Tips

- **Index once**: Only re-index when your app code changes
- **Keep backend running**: Start it once, use all day
- **Use specific descriptions**: More specific = faster generation
- **Check recordings**: Videos help debug failed tests

### Managing Tests

- **Save descriptions**: Keep a list of your test descriptions
- **Version control**: Track test history in the UI
- **Regular re-indexing**: Re-index after major app changes
- **Clean simulators**: Reset simulators occasionally

---

## Troubleshooting

### Backend Won't Start

**Error:** `ANTHROPIC_API_KEY not set`

**Solution:**
```bash
ios-test-automator config
# Add your API key
```

---

### No UI Elements Found

**Error:** `0 Accessibility IDs found`

**Solution:**
```bash
# Re-index your app
ios-test-automator rag ingest --app-dir /path/to/your/app
```

---

### Simulator Issues

**Error:** `Device 'iPhone 17' not found`

**Solution:**
```bash
# List available simulators
xcrun simctl list devices | grep iPhone

# Update config with available simulator
ios-test-automator config
# Set SIMULATOR_NAME to an available device
```

---

### Test Build Failed

**Error:** Build errors in test output

**Solution:**
1. Open your Xcode project
2. Try building manually
3. Fix any compilation errors
4. Try again in the tool

---

### Can't Connect to Backend

**Error:** `Backend Offline` in UI

**Solution:**
```bash
# Check if backend is running
ios-test-automator status

# If not, start it
ios-test-automator server
```

---

## FAQ

### Q: Do I need to know Swift or iOS development?

**A:** No! That's the whole point. Just describe what you want to test in plain English.

---

### Q: How much does it cost to use?

**A:** The tool is free, but you need an Anthropic API key which costs:
- ~$0.01-0.02 per test generation
- Most tests cost less than a penny

---

### Q: Can I test any iOS app?

**A:** You can test any app you have the source code for. The tool needs to index your app's codebase.

---

### Q: What if my test fails?

**A:** Check the:
1. Video recording (see what happened)
2. Test logs (error details)
3. Generated code (see what it tried to do)

Then adjust your test description and try again.

---

### Q: Can I run tests in CI/CD?

**A:** Yes! The tool can be automated. See the [CI/CD Integration Guide](CICD_INTEGRATION.md) for details.

---

### Q: How do I update the tool?

**A:** With Homebrew:
```bash
brew update
brew upgrade ios-test-automator
```

---

### Q: Can I test on a real device?

**A:** Currently, the tool uses iOS Simulator. Real device support is coming soon.

---

### Q: My test is flaky/unreliable

**A:** Try:
- Adding more specific waits/delays in description
- Making assertions more explicit
- Checking if UI elements are animating
- Verifying element accessibility IDs are stable

---

### Q: How do I report bugs or request features?

**A:** Open an issue on GitHub:
```bash
open https://github.com/yourusername/iOS-test-automator/issues
```

---

## Advanced Usage

### Custom Configuration

Edit `~/.ios-test-automator/.env` for advanced settings:

```bash
# Use different model
ANTHROPIC_MODEL=claude-opus-4-5-20251101

# Adjust RAG retrieval
RAG_TOP_K=15  # Get more context

# Change ports
BACKEND_PORT=9000
STREAMLIT_PORT=9501

# Simulator preferences
SIMULATOR_NAME="iPhone 15 Pro Max"
```

### Command Line Interface

```bash
# Check system status
ios-test-automator status

# View RAG statistics
ios-test-automator rag stats

# Query RAG directly
ios-test-automator rag query "login button"

# Show version
ios-test-automator version

# Get help
ios-test-automator help
```

### Multiple Apps

You can index multiple apps:

```bash
# Index App 1
ios-test-automator rag ingest --app-dir ~/Projects/App1 --collection app1

# Index App 2
ios-test-automator rag ingest --app-dir ~/Projects/App2 --collection app2

# Configure which to use
export RAG_COLLECTION=app1  # or app2
```

---

## Getting Help

### Documentation

- **Quick Start**: Fast introduction to the tool
- **Full Guide**: Comprehensive documentation
- **Troubleshooting**: Common issues and solutions
- **API Reference**: For advanced users

### Support Channels

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Questions and community help
- **Email**: support@yourdomain.com
- **Twitter**: @yourhandle

---

## Quick Reference

### Essential Commands

```bash
# Initialize
ios-test-automator init

# Configure
ios-test-automator config

# Index app
ios-test-automator rag ingest --app-dir /path/to/app

# Start backend
ios-test-automator server

# Start UI
ios-test-automator ui

# Check status
ios-test-automator status

# Get help
ios-test-automator help
```

### URLs

- **Web UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### File Locations

- **Config**: `~/.ios-test-automator/.env`
- **RAG Store**: `~/.ios-test-automator/rag_store`
- **Recordings**: `~/.ios-test-automator/recordings`

---

## Next Steps

1. ✅ **Install** the tool
2. ✅ **Configure** your API key
3. ✅ **Index** your iOS app
4. ✅ **Start** the services
5. ✅ **Create** your first test
6. 📚 **Learn** from examples
7. 🚀 **Automate** your testing workflow

---

## Feedback

We'd love to hear from you!

- 🐛 **Found a bug?** [Report it](https://github.com/yourusername/iOS-test-automator/issues)
- 💡 **Have an idea?** [Suggest a feature](https://github.com/yourusername/iOS-test-automator/discussions)
- ⭐ **Like the tool?** [Give us a star](https://github.com/yourusername/iOS-test-automator)

---

**Happy Testing!** 🎉

If you need help, don't hesitate to reach out. We're here to make iOS testing easier for everyone.
