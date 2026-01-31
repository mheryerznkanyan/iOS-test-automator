# Debugging Video Recording Issues

## Problem: Recording shows home screen instead of test

This happens when the video recording and test execution use different simulators.

## Diagnosis Steps

### 1. Verify Simulator Setup

Run the verification script:
```bash
cd streamlit-ui
./verify_simulator.sh
```

This will:
- Find the iPhone 17 simulator
- Boot it
- Open Simulator.app with the correct device
- Show you the simulator ID

### 2. Check Streamlit UI Logs

When you run a test in the Streamlit UI, look for these messages:

```
📱 Using Simulator: iPhone 17 (ID: 5BFFD820-697B-4093-8969-74E617604232)
✅ Simulator booted: iPhone 17 (5BFFD82...)
Starting video recording on simulator: 5BFFD82...
Running test: LoginInvalidCredentialsTest/testLoginWithInvalidCredentials on simulator 5BFFD82...
```

**Important**: All these messages should show the SAME simulator ID!

### 3. Check for Multiple Running Simulators

```bash
# List all booted simulators
xcrun simctl list devices | grep Booted

# You should see only ONE booted simulator
```

If you see multiple simulators booted, that's the problem!

### 4. Manual Test

Try recording manually:

```bash
# Get the simulator ID
SIM_ID=$(xcrun simctl list devices | grep "iPhone 17" | head -1 | grep -o '[A-F0-9-]\{36\}')

echo "Simulator ID: $SIM_ID"

# Boot it
xcrun simctl shutdown all
xcrun simctl boot "$SIM_ID"
open -a Simulator --args -CurrentDeviceUDID "$SIM_ID"
sleep 5

# Start recording
xcrun simctl io "$SIM_ID" recordVideo test_manual.mp4 &
RECORDING_PID=$!
sleep 3

# Launch the app manually in the simulator
# Or run the test
cd ../ios-app/src/SampleApp
xcodebuild test \
  -project SampleApp.xcodeproj \
  -scheme SampleApp \
  -destination "id=$SIM_ID" \
  -only-testing:SampleAppUITests/LoginInvalidCredentialsTestFixed/testLoginWithInvalidCredentials

# Stop recording
kill -SIGINT $RECORDING_PID

# Check the recording
open test_manual.mp4
```

## Common Causes & Fixes

### Issue 1: Xcodebuild creates a new simulator

**Symptom**: Recording shows home screen, test passes

**Cause**: xcodebuild sometimes ignores the `-destination id=` and creates its own simulator

**Fix**: Use test-without-building after a single build

```python
# Build once
xcodebuild build-for-testing -destination "id=$SIM_ID"

# Then run tests without rebuilding
xcodebuild test-without-building -destination "id=$SIM_ID"
```

### Issue 2: Multiple simulators running

**Symptom**: Different simulator IDs in logs

**Cause**: Old simulators weren't shut down properly

**Fix**: Always shutdown all simulators first

```bash
xcrun simctl shutdown all
```

### Issue 3: Simulator not fully booted

**Symptom**: Recording starts before app launches

**Cause**: Not waiting long enough after boot

**Fix**: Add more wait time after booting:

```python
xcrun simctl boot "$SIM_ID"
sleep 3  # Wait for boot
open -a Simulator
sleep 5  # Wait for Simulator.app
# Now start recording
```

### Issue 4: Wrong simulator name

**Symptom**: Can't find simulator

**Cause**: Simulator name doesn't match exactly

**Fix**: Check available simulators:

```bash
xcrun simctl list devices available | grep iPhone
```

Update `SIMULATOR_NAME` in `app.py` to match exactly.

## Verification Checklist

- [ ] Only ONE simulator is booted (check with `xcrun simctl list devices | grep Booted`)
- [ ] Simulator ID is consistent in all log messages
- [ ] Simulator.app shows the correct device in the title bar
- [ ] Wait time after boot is sufficient (5+ seconds)
- [ ] xcodebuild uses `-destination "id=$SIM_ID"` (not name)
- [ ] Recording starts AFTER simulator is fully booted
- [ ] Recording stops AFTER test completes

## Debug Mode

Add this to the Streamlit UI to see what's happening:

```python
# Before recording
st.write(f"DEBUG: Recording on: {simulator_id}")

# Before test
st.write(f"DEBUG: Testing on: {simulator_id}")

# After test
st.write(f"DEBUG: Check recording at: {recording_path}")
```

## Still Not Working?

1. Check xcodebuild output for destination:
   ```bash
   grep -i "destination" test_output.log
   ```

2. Check which simulator xcodebuild actually used:
   ```bash
   grep -i "selected test device" test_output.log
   ```

3. Try the bash script to confirm it works:
   ```bash
   cd ..
   ./run_scenario_test.sh "login_invalid_credentials"
   ```

4. Compare simulator IDs:
   - Bash script uses: `$DEVICE_ID`
   - Streamlit uses: `sim_id`
   - They should be IDENTICAL

## Solution: Use test-without-building

The most reliable approach is:

1. Build ONCE with specific destination
2. Record video
3. Run test-without-building with SAME destination
4. Stop recording

This prevents xcodebuild from spawning new simulators.

Example:
```bash
# Step 1: Build
xcodebuild build-for-testing \
  -project ... \
  -scheme ... \
  -destination "id=$SIM_ID"

# Step 2 & 3: Record + Test
xcrun simctl io "$SIM_ID" recordVideo video.mp4 &
xcodebuild test-without-building \
  -destination "id=$SIM_ID" \
  -only-testing:...
kill -SIGINT $RECORDING_PID
```
