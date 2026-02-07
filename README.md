# iOS Test Automator

An AI-powered iOS test automation tool that reads test specifications from markdown files, generates XCTest/XCUITest code, runs tests using Apple-native tools, and generates comprehensive reports.

## Features

- **Spec Parser**: Parse markdown test specifications into structured test definitions
- **Test Generator**: Generate XCTest (unit) and XCUITest (UI) Swift code
- **Test Runner**: Execute tests via `xcodebuild` with simulator management
- **Result Parser**: Parse `.xcresult` bundles for detailed test metrics
- **Report Generator**: Generate markdown/HTML/JSON test reports

## Installation

### Prerequisites

- macOS 14.0+
- Xcode 15.0+
- Swift 5.9+

### Build

```bash
cd src/TestAutomatorCLI
swift build
```

The built executable will be at `.build/debug/testautomator`.

## Usage

### Parse Test Specifications

```bash
testautomator parse --specs ./specs --verbose
```

### Generate Test Code

```bash
testautomator generate --specs ./specs --output ./generated_tests
```

### Run Tests

```bash
testautomator run \
  --project ./SampleApp/SampleApp.xcodeproj \
  --scheme SampleApp \
  --device "iPhone 15" \
  --result-bundle ./results.xcresult
```

### Generate Report

```bash
testautomator report \
  --results ./results.xcresult \
  --output ./report.md \
  --format markdown
```

### Full Pipeline

```bash
testautomator all \
  --specs ./specs \
  --project ./SampleApp/SampleApp.xcodeproj \
  --scheme SampleApp \
  --output ./reports
```

### Manage Simulators

```bash
# List simulators
testautomator simulators --list

# Boot simulator
testautomator simulators --boot "iPhone 15"

# Take screenshot
testautomator simulators --screenshot ./screenshot.png
```

## Test Specification Format

Create markdown files in the `specs/` directory:

```markdown
# Test: Login Flow

## Type: UI

## Preconditions
- App is launched
- User is logged out

## Steps
1. Tap "Login" button
2. Enter "test@example.com" in email field
3. Enter "password123" in password field
4. Tap "Submit" button

## Expected Results
- User sees home screen
- Welcome message displays username

## Tags
- login
- smoke-test
```

### Supported Test Types

- `UI` - Generates XCUITest code
- `Unit` - Generates XCTest code

### Supported Actions

| Action | Example |
|--------|---------|
| Tap | `Tap "Login" button` |
| Enter | `Enter "text" in email field` |
| Verify | `Verify "Welcome" is displayed` |
| Wait | `Wait for "Loading" to disappear` |
| Scroll | `Scroll to "Submit" button` |

## Project Structure

```
ios-app/
├── .specify/                    # SpecKit configuration
│   ├── memory/constitution.md   # Project principles
│   ├── scripts/                 # Automation scripts
│   └── templates/               # Document templates
├── src/
│   └── TestAutomatorCLI/       # Main CLI tool
│       ├── Package.swift
│       └── Sources/
│           ├── TestAutomatorCLI/    # CLI executable
│           └── TestAutomatorLib/    # Core library
│               ├── Parser/          # Spec parsing
│               ├── Generator/       # Test generation
│               ├── Runner/          # Test execution
│               ├── Results/         # Result parsing
│               └── Reporter/        # Report generation
├── specs/                       # Test specifications
└── reports/                     # Generated reports
```

## Apple-Native Tools Used

- `xcrun xcodebuild` - Build and run tests
- `xcrun simctl` - Simulator management
- `xcrun xcresulttool` - Parse test results
- `xcrun xccov` - Code coverage

## License

MIT
