#!/usr/bin/env python3
"""
Add UI Test Target to ShelfPlayer Xcode Project
"""

import sys
from pbxproj import XcodeProject

# Paths
PROJECT_PATH = '/Users/mheryerznkanyan/Projects/ShelfPlayer/ShelfPlayer.xcodeproj/project.pbxproj'
TEST_FILE_PATH = 'ShelfPlayerUITests/LLMGeneratedTest.swift'

print("🔧 Adding UI Test Target to ShelfPlayer...")
print("=" * 50)

try:
    # Load the project
    print("📂 Loading Xcode project...")
    project = XcodeProject.load(PROJECT_PATH)

    # Add the UI test target
    print("➕ Adding ShelfPlayerUITests target...")
    target = project.add_target(
        target_name='ShelfPlayerUITests',
        target_type='UI testing bundle',
        bundle_id='com.example.ShelfPlayer.ShelfPlayerUITests'
    )

    # Add the test file to the target
    print(f"📝 Adding test file: {TEST_FILE_PATH}")
    project.add_file(TEST_FILE_PATH, target_name='ShelfPlayerUITests')

    # Link with the app target
    print("🔗 Linking with Multiplatform target...")
    # Find the main app target
    multiplatform_target = None
    for t in project.objects.get_targets():
        if t.name == 'Multiplatform':
            multiplatform_target = t
            break

    if multiplatform_target:
        # Add dependency
        project.add_target_dependency(target, multiplatform_target)
        print("✅ Linked ShelfPlayerUITests to Multiplatform")
    else:
        print("⚠️  Could not find Multiplatform target")

    # Save the project
    print("💾 Saving project...")
    project.save()

    print("\n" + "=" * 50)
    print("✅ UI Test Target Added Successfully!")
    print("\nNext steps:")
    print("1. Open ShelfPlayer.xcodeproj in Xcode")
    print("2. Verify the ShelfPlayerUITests target is present")
    print("3. Run tests using Streamlit UI or backend API")
    print("=" * 50)

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nStack trace:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
