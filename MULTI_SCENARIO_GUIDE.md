# Multi-Scenario Testing Guide

## Overview

You now have **12 pre-configured test scenarios** covering different app flows, including tests that require login and tests that don't.

## The Login Problem - SOLVED ✅

**Your Question:** "What if a test needs to go to a given page after login?"

**Answer:** The RAG system handles this automatically! When you describe a test that needs login, just include it in your natural language description:

```
"First login with test@example.com and password123, then tap Profile tab..."
```

The LLM will generate code that:
1. Logs in first
2. Then performs the actual test steps

## Available Test Scenarios

### Authentication Tests (No Login Required)
1. **login_success** - Test successful login flow
2. **login_invalid_credentials** - Test with wrong password
3. **logout_flow** - Login, navigate to profile, logout

### Validation Tests (No Login Required)
4. **login_empty_email** - Empty email validation
5. **login_invalid_email_format** - Invalid email format validation

### Items Tests (Login Required)
6. **item_list_display** - View items after login
7. **item_search** - Search functionality with filters
8. **item_pagination** - Load more items
9. **item_edit_flow** - Edit an item's details
10. **item_detail_navigation** - Navigate to item detail

### Navigation Tests (Login Required)
11. **tab_navigation** - Switch between Items and Profile tabs

### Profile Tests (Login Required)
12. **profile_view** - View profile information

## Running Tests

### Option 1: Run a Single Scenario

```bash
./run_scenario_test.sh <scenario_name>
```

**Examples:**

```bash
# Test login
./run_scenario_test.sh login_success

# Test item search (includes automatic login)
./run_scenario_test.sh item_search

# Test profile view (includes automatic login)
./run_scenario_test.sh profile_view
```

### Option 2: Run All Scenarios

```bash
./run_all_scenarios.sh
```

This will:
- Run all 12 scenarios sequentially
- Generate test code for each
- Build and execute each test
- Record video for each
- Save results to timestamped directory
- Show summary report

**Output:**
```
Results Summary:
  ✅ Passed: 10
  ❌ Failed: 2
  ⚠️  Errors: 0
  📊 Total:  12

Success Rate: 83.3%
```

### Option 3: Generate Tests Only (No Execution)

```bash
./generate_multiple_tests.sh
```

This generates Swift code for all scenarios without running them.

## How "Login Required" Tests Work

### Example: Item Search Test

**Description:**
```
"Test item search functionality: first login with test@example.com
and password123, tap on search field with accessibility ID searchField,
type 'Electronics' to filter items, and verify filtered results show
only Electronics category items"
```

**Generated Code Structure:**
```swift
func testItemSearch() throws {
    app.launch()
    sleep(3)

    // Step 1: Login first
    let emailField = app.textFields["emailTextField"]
    emailField.tap()
    emailField.typeText("test@example.com")

    let passwordField = app.secureTextFields["passwordTextField"]
    passwordField.tap()
    passwordField.typeText("password123")

    app.buttons["loginButton"].tap()
    sleep(3)

    // Step 2: Wait for Items tab
    XCTAssertTrue(app.tabBars.buttons["Items"].waitForExistence(timeout: 5))

    // Step 3: Perform search
    let searchField = app.textFields["searchField"]
    searchField.tap()
    searchField.typeText("Electronics")
    sleep(2)

    // Step 4: Verify results
    // ... verification code
}
```

**Key Point:** The LLM automatically understands from your description that login is needed and generates the complete flow!

## Test Scenarios Details

### 1. Login Success
- **Description:** Basic login test
- **Needs Login:** No
- **Tests:** Email input, password input, login button, navigation to Items

### 2. Login Invalid Credentials
- **Description:** Test error handling
- **Needs Login:** No
- **Tests:** Wrong password, error message appears

### 3. Login Empty Email
- **Description:** Validation test
- **Needs Login:** No
- **Tests:** Empty email field, login button disabled

### 4. Login Invalid Email Format
- **Description:** Email format validation
- **Needs Login:** No
- **Tests:** Email without @, error message

### 5. Item List Display
- **Description:** View items after login
- **Needs Login:** Yes (automatic)
- **Tests:** Login → Items list loads → Multiple items visible

### 6. Item Search
- **Description:** Search/filter items
- **Needs Login:** Yes (automatic)
- **Tests:** Login → Search field → Type "Electronics" → Verify filtered results

### 7. Item Detail Navigation
- **Description:** Navigate to item detail
- **Needs Login:** Yes (automatic)
- **Tests:** Login → Tap first item → Detail screen shows

### 8. Item Pagination
- **Description:** Load more items
- **Needs Login:** Yes (automatic)
- **Tests:** Login → Scroll to bottom → Tap "Load More" → Verify more items

### 9. Profile View
- **Description:** View profile screen
- **Needs Login:** Yes (automatic)
- **Tests:** Login → Tap Profile tab → Verify email, welcome message

### 10. Logout Flow
- **Description:** Complete logout test
- **Needs Login:** Yes (automatic)
- **Tests:** Login → Profile → Logout → Back to login screen

### 11. Item Edit Flow
- **Description:** Edit an item
- **Needs Login:** Yes (automatic)
- **Tests:** Login → Open item detail → Tap Edit → Modify → Save

### 12. Tab Navigation
- **Description:** Navigate between tabs
- **Needs Login:** Yes (automatic)
- **Tests:** Login → Profile tab → Items tab → Verify navigation

## Customizing Scenarios

Edit [test_scenarios.json](test_scenarios.json):

```json
{
  "scenarios": [
    {
      "name": "my_custom_test",
      "description": "First login with test@example.com and password123, then do something custom",
      "class_name": "MyCustomTest",
      "needs_login": true,
      "category": "custom"
    }
  ]
}
```

Then run:
```bash
./run_scenario_test.sh my_custom_test
```

## Understanding Test Results

### Result Files (Per Scenario)

When running a single scenario:
```
test_recording_<scenario>.mp4    # Video of test execution
test_output_<scenario>.log       # Complete test logs
LLMGeneratedTest.swift           # Generated test code
```

### Result Directory (All Scenarios)

When running all scenarios:
```
test_results_20260117_143022/
  ├── summary.csv                      # Summary table
  ├── LoginSuccessTest.swift           # Generated code
  ├── login_success_test.log           # Test log
  ├── login_success_recording.mp4      # Video
  ├── ItemSearchTest.swift
  ├── item_search_test.log
  ├── item_search_recording.mp4
  └── ...
```

### Summary Report

```
scenario,result,category
login_success,PASSED,authentication
login_invalid_credentials,PASSED,authentication
login_empty_email,PASSED,validation
item_list_display,PASSED,items
item_search,FAILED,items
...
```

## Tips for Writing Test Descriptions

### ✅ Good Descriptions

**Explicit Login:**
```
"First login with test@example.com and password123, then navigate to
Profile tab and verify email is displayed"
```

**Step-by-Step:**
```
"Test item editing: first login, tap first item in list to open detail
view, tap edit button, modify the title, tap save button, verify sheet dismisses"
```

**With Accessibility IDs:**
```
"First login, tap search field with accessibility ID searchField,
type 'Electronics', verify filtered results"
```

### ❌ Avoid Vague Descriptions

```
"Test the profile"  # Too vague
"Search for items"  # Missing login step
```

## Common Patterns

### Pattern 1: Simple Flow After Login

```json
{
  "description": "First login with test@example.com and password123, then tap Profile tab and verify logout button exists"
}
```

### Pattern 2: Multi-Step Flow

```json
{
  "description": "First login with test@example.com and password123, wait for items to load, scroll to bottom, tap Load More button, wait for new items, verify more items appear in the list"
}
```

### Pattern 3: Form Interaction

```json
{
  "description": "First login with test@example.com and password123, tap first item, tap edit button with accessibility ID editButton, clear title field, type new title 'Updated Item', tap save button, verify sheet dismisses"
}
```

## RAG Handles the Details

You don't need to specify every accessibility ID - RAG finds them!

**You write:**
```
"First login, then tap the search field and search for Electronics"
```

**RAG finds:**
- `emailTextField`, `passwordTextField`, `loginButton` (for login)
- `searchField` (for search)
- `itemList`, `itemRow_*` (for verification)

**LLM generates:**
```swift
let emailField = app.textFields["emailTextField"]
let passwordField = app.secureTextFields["passwordTextField"]
let loginButton = app.buttons["loginButton"]
let searchField = app.textFields["searchField"]
// ... complete implementation
```

## Performance Tips

### Fast Iteration
Generate tests without running:
```bash
./generate_multiple_tests.sh
```

Then manually run specific ones in Xcode.

### Parallel Generation
Generate multiple tests at once:
```bash
# In separate terminals
./run_scenario_test.sh login_success &
./run_scenario_test.sh item_search &
wait
```

### Focus on Categories
Run only authentication tests:
```bash
jq -r '.scenarios[] | select(.category=="authentication") | .name' test_scenarios.json | \
while read scenario; do
  ./run_scenario_test.sh $scenario
done
```

## Troubleshooting

### Login Timeout
If login takes too long, increase wait times in description:
```
"First login with test@example.com and password123, wait 5 seconds for navigation..."
```

### Element Not Found
RAG might miss some IDs. Add explicit hint:
```
"...tap the edit button with accessibility ID editButton..."
```

### Test Fails After Login
Check the video recording to see where it fails:
```bash
open test_recording_<scenario>.mp4
```

## Next Steps

1. **Run All Scenarios** - See which flows work out of the box
   ```bash
   ./run_all_scenarios.sh
   ```

2. **Analyze Failures** - Watch videos of failed tests
   ```bash
   open test_results_*/
   ```

3. **Refine Descriptions** - Update scenarios that failed
   ```bash
   # Edit test_scenarios.json
   ./run_scenario_test.sh <updated_scenario>
   ```

4. **Add Custom Scenarios** - Create your own test flows
   ```bash
   # Add to test_scenarios.json
   ./run_scenario_test.sh my_new_scenario
   ```

## Summary

**The Key Innovation:** You don't need to manually handle "how to get to a page" - just describe it in natural language:

```
"First login with test@example.com and password123, then..."
```

The LLM + RAG system:
- ✅ Generates login code automatically
- ✅ Finds all necessary accessibility IDs
- ✅ Handles waits and transitions
- ✅ Creates complete, runnable tests

**No manual page navigation setup needed!** 🎉
