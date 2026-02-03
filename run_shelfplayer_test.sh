#!/bin/bash
#
# Standalone test runner for ShelfPlayer
# Runs generated UI tests without needing to add them to the Xcode project
#

set -e

# Configuration
SHELFPLAYER_DIR="/Users/mheryerznkanyan/Projects/ShelfPlayer"
TEST_FILE="$SHELFPLAYER_DIR/ShelfPlayerUITests/LLMGeneratedTest.swift"
SCHEME="Multiplatform"
SIMULATOR_NAME="${SIMULATOR_NAME:-iPhone 17}"

echo "🧪 ShelfPlayer UI Test Runner"
echo "=============================="

# Check if test file exists
if [ ! -f "$TEST_FILE" ]; then
    echo "❌ Test file not found: $TEST_FILE"
    exit 1
fi

# Get simulator ID
echo "📱 Finding simulator..."
SIMULATOR_ID=$(xcrun simctl list devices | grep "$SIMULATOR_NAME" | grep -oE '[A-F0-9-]{36}' | head -1)

if [ -z "$SIMULATOR_ID" ]; then
    echo "❌ Simulator not found: $SIMULATOR_NAME"
    exit 1
fi

echo "✅ Found simulator: $SIMULATOR_ID"

# Boot simulator if needed
echo "🚀 Booting simulator..."
xcrun simctl boot "$SIMULATOR_ID" 2>/dev/null || echo "Simulator already booted"
open -a Simulator
sleep 3

# For now, just show the generated test
echo ""
echo "📝 Generated Test Code:"
echo "======================="
cat "$TEST_FILE"
echo ""
echo ""
echo "⚠️  To run this test, you need to:"
echo "1. Open ShelfPlayer.xcodeproj in Xcode"
echo "2. Add a UI Testing target named 'ShelfPlayerUITests'"
echo "3. Add the file ShelfPlayerUITests/LLMGeneratedTest.swift to the target"
echo "4. Run the test from Xcode or use xcodebuild"
echo ""
echo "Or use the Streamlit UI after completing the Xcode setup!"
