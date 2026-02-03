# iOS Test Automator - Beta Testing Guide

Thank you for helping test iOS Test Automator! Your feedback will help make this tool better for everyone.

## What is Beta Testing?

You're trying out iOS Test Automator before it's released to the public. We need your help to:
- Find bugs and issues
- Test real-world use cases
- Improve the user experience
- Validate performance and reliability

## Beta Test Timeline

- **Start Date**: [Your Date]
- **Duration**: 2-4 weeks
- **End Date**: [Your Date]
- **Feedback Deadline**: [Your Date]

---

## Getting Started

### 1. Installation (Beta)

```bash
# Clone the repository
git clone https://github.com/yourusername/iOS-test-automator.git
cd iOS-test-automator

# Run the setup
ios-test-automator setup

# Initialize
ios-test-automator init
```

**OR** use the install script:

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/iOS-test-automator/main/install.sh | bash
```

### 2. Get Your API Key

1. Go to https://console.anthropic.com/
2. Create an account (if needed)
3. Generate an API key
4. Add it to your config:
   ```bash
   ios-test-automator config
   ```

### 3. Join the Beta Community

- **Slack/Discord**: [Invite Link]
- **Email**: beta-testers@yourdomain.com
- **GitHub Discussions**: [Link]

---

## What to Test

### Priority 1: Core Functionality ⭐⭐⭐

These are the most important features to test:

#### ✅ Test Generation
- [ ] Generate tests from natural language descriptions
- [ ] Verify RAG finds correct UI elements
- [ ] Check that generated Swift code is valid
- [ ] Try various test scenarios (login, navigation, forms, etc.)

**How to test:**
1. Open UI at http://localhost:8501
2. Try these test descriptions:
   - "Test login with valid credentials"
   - "Test navigation to settings screen"
   - "Test adding item to favorites"
3. Click "Generate Test"
4. Review generated code
5. **Report**: Does it match your expectations?

#### ✅ Test Execution
- [ ] Tests run successfully in simulator
- [ ] Video recording works
- [ ] Test results are accurate
- [ ] Logs are helpful

**How to test:**
1. Generate a test (see above)
2. Click "Generate & Run"
3. Watch the simulator
4. Review the video recording
5. **Report**: Any issues during execution?

#### ✅ RAG Indexing
- [ ] Successfully index your iOS app
- [ ] RAG finds accessibility IDs
- [ ] RAG finds screens/view controllers
- [ ] RAG finds UI components

**How to test:**
1. Run: `ios-test-automator rag ingest --app-dir /path/to/your/app`
2. Check output for number of files indexed
3. Generate a test and see if RAG context is relevant
4. **Report**: Were the right elements found?

---

### Priority 2: User Experience ⭐⭐

#### ✅ Setup & Installation
- [ ] Installation process is smooth
- [ ] Configuration is clear
- [ ] Error messages are helpful
- [ ] Documentation is accurate

**What to check:**
- Was installation confusing at any point?
- Did you get stuck anywhere?
- Were error messages clear?

#### ✅ Web Interface
- [ ] UI is intuitive
- [ ] Layout is clear
- [ ] Buttons work as expected
- [ ] Videos play correctly

**What to check:**
- Is anything confusing in the UI?
- Are buttons labeled clearly?
- Does the layout make sense?

#### ✅ CLI Interface
- [ ] Commands are easy to use
- [ ] Help text is clear
- [ ] Output is readable
- [ ] Status checks work

**How to test:**
```bash
ios-test-automator help
ios-test-automator status
ios-test-automator rag stats
```

---

### Priority 3: Edge Cases & Reliability ⭐

#### ✅ Error Handling
- [ ] Graceful failures
- [ ] Helpful error messages
- [ ] Recovery from errors

**Try these scenarios:**
- Missing API key
- Invalid test description
- Simulator not available
- App build failure
- Network issues

#### ✅ Performance
- [ ] Fast test generation (< 30 seconds)
- [ ] Responsive UI
- [ ] Reasonable memory usage
- [ ] Smooth video playback

**What to measure:**
- How long does test generation take?
- How long does test execution take?
- Is the UI responsive?

---

## Testing Scenarios

### Scenario 1: Login Flow (15 minutes)

**Goal**: Test a complete login flow

**Steps:**
1. Index your iOS app
2. Create test: "Test successful login with email test@example.com and password password123"
3. Generate and run the test
4. Watch the video
5. Review results

**Report:**
- Did it work as expected?
- Was the video clear?
- Were results accurate?

---

### Scenario 2: Complex Navigation (20 minutes)

**Goal**: Test multi-screen navigation

**Steps:**
1. Create test: "Test navigation: tap Settings, tap Profile, verify profile screen shows user email"
2. Generate and run
3. Check if all screens were navigated correctly

**Report:**
- Did it navigate correctly?
- Were all screens found?
- Any issues with timing?

---

### Scenario 3: Form Validation (15 minutes)

**Goal**: Test form validation

**Steps:**
1. Create test: "Test invalid email: enter 'notanemail', tap submit, verify error message shows"
2. Generate and run
3. Check validation behavior

**Report:**
- Did validation work?
- Was error message detected?

---

### Scenario 4: Multiple Tests (30 minutes)

**Goal**: Create and run multiple tests

**Steps:**
1. Create 5 different tests
2. Run them all
3. Review test history

**Report:**
- Can you organize multiple tests?
- Is history useful?
- Any issues running many tests?

---

### Scenario 5: Your Real App (1 hour)

**Goal**: Test with your actual iOS app

**Steps:**
1. Index your real iOS app
2. Create 3-5 tests for actual features
3. Run them all
4. Review results

**Report:**
- How well did it work with your app?
- What worked well?
- What didn't work?
- What would make it better?

---

## What to Report

### For Each Issue/Bug

Please include:

1. **Title**: Short description of the issue
2. **Steps to Reproduce**:
   - What did you do?
   - What command/button did you use?
   - What was the input?
3. **Expected Result**: What should have happened?
4. **Actual Result**: What actually happened?
5. **Screenshots/Video**: If applicable
6. **Environment**:
   - macOS version
   - Xcode version
   - iOS Test Automator version
7. **Logs**: Any error messages or logs

**Example Bug Report:**

```markdown
**Title**: Test generation fails for long descriptions

**Steps to Reproduce**:
1. Open UI at http://localhost:8501
2. Enter a very long test description (500+ words)
3. Click "Generate Test"

**Expected**: Test is generated successfully

**Actual**: Error: "Description too long"

**Environment**:
- macOS 14.2
- Xcode 15.1
- iOS Test Automator v1.0.0-beta

**Logs**:
```
ERROR: Description exceeds maximum length
```

### For Feature Requests

Please include:

1. **Feature Title**: What feature do you want?
2. **Use Case**: Why do you need it?
3. **How it Should Work**: Describe the ideal behavior
4. **Priority**: How important is this? (Low/Medium/High)

**Example Feature Request:**

```markdown
**Title**: Export tests to Xcode project

**Use Case**: I want to add generated tests to my Xcode project permanently

**How it Should Work**:
- Button in UI: "Export to Xcode"
- Copies Swift file to my test target
- Updates test target automatically

**Priority**: Medium
```

---

## Feedback Channels

### Report Bugs

**GitHub Issues** (Preferred):
```bash
open https://github.com/yourusername/iOS-test-automator/issues
```

**Email**:
beta-bugs@yourdomain.com

---

### Share Feedback

**Slack/Discord**: [Invite Link]

**Feedback Form**: [Google Form Link]

**Email**: beta-feedback@yourdomain.com

---

### Quick Questions

**Slack/Discord**: #beta-testers channel

**Email**: beta-help@yourdomain.com

---

## Testing Checklist

Use this checklist to track your testing:

### Week 1: Basic Testing
- [ ] Install the tool successfully
- [ ] Configure API key
- [ ] Index a sample iOS app
- [ ] Generate first test
- [ ] Run first test
- [ ] Watch video recording
- [ ] Explore web UI
- [ ] Try CLI commands
- [ ] Report any issues found

### Week 2: Real-World Testing
- [ ] Index your actual iOS app
- [ ] Create 5+ real tests
- [ ] Run all tests
- [ ] Try different test scenarios
- [ ] Test error cases
- [ ] Check performance
- [ ] Review test history
- [ ] Report feedback

### Week 3: Advanced Testing
- [ ] Test edge cases
- [ ] Try complex flows
- [ ] Test with multiple apps
- [ ] Check resource usage
- [ ] Test on different macOS versions
- [ ] Try all CLI features
- [ ] Complete feedback form

### Week 4: Final Feedback
- [ ] Fill out final survey
- [ ] Submit bug reports
- [ ] Share feature requests
- [ ] Provide overall feedback

---

## Testing Rewards 🎁

As a thank you for beta testing:

- ✨ **Free credits**: $25 Anthropic API credits
- 🎟️ **Early access**: Lifetime free tier when we launch
- 🏆 **Beta tester badge**: In our credits/acknowledgments
- 📧 **Direct line**: Priority support during beta

---

## Important Notes

### Known Issues

We're already aware of these issues (no need to report):

- ❌ Real device testing not supported yet
- ❌ Parallel test execution not implemented
- ❌ Test results export to CI/CD format pending
- ❌ Dark mode not fully implemented

### Privacy & Data

- ❌ We do NOT collect your code
- ❌ We do NOT store your tests
- ✅ We may collect anonymous usage metrics
- ✅ Your API key stays on your machine
- ✅ All data is local to your computer

### Beta Access

- This is a **private beta**
- Please don't share install links publicly yet
- Feel free to discuss with other beta testers
- We'll announce public release soon

---

## Schedule

### Week 1
- **Goal**: Get familiar with the tool
- **Focus**: Basic functionality
- **Check-in**: Friday Slack call

### Week 2
- **Goal**: Test with real apps
- **Focus**: Real-world usage
- **Check-in**: Friday Slack call

### Week 3
- **Goal**: Edge cases & stress testing
- **Focus**: Breaking things
- **Check-in**: Friday Slack call

### Week 4
- **Goal**: Final feedback
- **Focus**: Overall experience
- **Check-in**: Final survey

---

## Contact

### Beta Program Manager
- **Name**: [Your Name]
- **Email**: beta@yourdomain.com
- **Slack**: @yourname

### Technical Support
- **Email**: beta-support@yourdomain.com
- **Slack**: #beta-support

---

## Thank You! 🙏

Your participation in this beta test is invaluable. Every bug you find, every suggestion you make, helps us build a better product.

We're excited to have you on this journey with us!

**Questions?** Reach out anytime via Slack or email.

**Happy Testing!** 🚀
