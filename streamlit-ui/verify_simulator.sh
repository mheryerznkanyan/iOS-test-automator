#!/bin/bash
# Verify simulator setup for Streamlit UI

echo "=== iOS Simulator Verification ==="
echo ""

SIMULATOR_NAME="iPhone 17"

echo "1. Finding simulator '$SIMULATOR_NAME'..."
DEVICE_ID=$(xcrun simctl list devices | grep "$SIMULATOR_NAME" | grep -v "unavailable" | head -1 | grep -o '[A-F0-9-]\{36\}')

if [ -z "$DEVICE_ID" ]; then
  echo "❌ Simulator '$SIMULATOR_NAME' not found"
  echo ""
  echo "Available simulators:"
  xcrun simctl list devices available | grep "iPhone"
  exit 1
fi

echo "✅ Found: $DEVICE_ID"
echo ""

echo "2. Checking simulator status..."
STATUS=$(xcrun simctl list devices | grep "$DEVICE_ID")
echo "$STATUS"
echo ""

echo "3. Shutting down all simulators..."
xcrun simctl shutdown all 2>/dev/null || true
sleep 1
echo "✅ All simulators shut down"
echo ""

echo "4. Booting simulator..."
xcrun simctl boot "$DEVICE_ID"
sleep 2
echo "✅ Simulator booted"
echo ""

echo "5. Opening Simulator app..."
open -a Simulator --args -CurrentDeviceUDID "$DEVICE_ID"
sleep 3
echo "✅ Simulator app opened"
echo ""

echo "6. Bringing Simulator to front..."
osascript -e 'tell application "Simulator" to activate'
sleep 2
echo "✅ Simulator activated"
echo ""

echo "7. Verifying simulator is running..."
xcrun simctl list devices | grep "$DEVICE_ID"
echo ""

echo "=== Setup Complete ==="
echo "Simulator ID: $DEVICE_ID"
echo ""
echo "You can now use this ID in the Streamlit UI:"
echo "export SIMULATOR_NAME='$SIMULATOR_NAME'"
echo ""
echo "Or test recording with:"
echo "xcrun simctl io $DEVICE_ID recordVideo test.mp4"
