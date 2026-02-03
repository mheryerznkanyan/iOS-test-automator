#!/usr/bin/env python3
"""
Add ShelfPlayerUITests target to ShelfPlayer.xcodeproj
"""
import uuid
import re
import shutil
from pathlib import Path

# Paths
PROJECT_DIR = Path("/Users/mheryerznkanyan/Projects/ShelfPlayer")
PROJECT_FILE = PROJECT_DIR / "ShelfPlayer.xcodeproj" / "project.pbxproj"
SCHEME_FILE = PROJECT_DIR / "ShelfPlayer.xcodeproj" / "xcshareddata" / "xcschemes" / "Multiplatform.xcscheme"
UI_TESTS_DIR = PROJECT_DIR / "ShelfPlayerUITests"
TEST_FILE = UI_TESTS_DIR / "LLMGeneratedTest.swift"

# Backup
BACKUP_FILE = PROJECT_FILE.with_suffix('.pbxproj.backup')

def generate_uuid():
    """Generate a 24-character uppercase hex UUID (Xcode format)"""
    return uuid.uuid4().hex.upper()[:24]

def read_file(path):
    """Read file content"""
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    """Write content to file"""
    with open(path, 'w') as f:
        f.write(content)

def find_multiplatform_target_uuid(content):
    """Find the UUID of the Multiplatform target"""
    match = re.search(r'([A-F0-9]{24}) /\* Multiplatform \*/ = \{[^}]*isa = PBXNativeTarget', content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)
    return None

def find_main_group_uuid(content):
    """Find the main group UUID"""
    match = re.search(r'mainGroup = ([A-F0-9]{24})', content)
    if match:
        return match.group(1)
    return None

def find_product_group_uuid(content):
    """Find the products group UUID"""
    match = re.search(r'productRefGroup = ([A-F0-9]{24})', content)
    if match:
        return match.group(1)
    return None

def add_ui_test_target(content, multiplatform_uuid):
    """Add UI test target to project.pbxproj"""

    # Generate UUIDs for new objects
    target_uuid = generate_uuid()
    product_ref_uuid = generate_uuid()
    file_ref_uuid = generate_uuid()
    build_file_uuid = generate_uuid()
    sources_phase_uuid = generate_uuid()
    frameworks_phase_uuid = generate_uuid()
    resources_phase_uuid = generate_uuid()
    test_host_dependency_uuid = generate_uuid()
    target_dependency_uuid = generate_uuid()
    container_proxy_uuid = generate_uuid()
    group_uuid = generate_uuid()

    print(f"Generated UUIDs:")
    print(f"  Target: {target_uuid}")
    print(f"  Product: {product_ref_uuid}")
    print(f"  File: {file_ref_uuid}")

    # 1. Add PBXBuildFile section
    build_file_section = f"\t\t{build_file_uuid} /* LLMGeneratedTest.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {file_ref_uuid} /* LLMGeneratedTest.swift */; }};"

    # Find PBXBuildFile section and add our entry
    content = re.sub(
        r'(/\* Begin PBXBuildFile section \*/\n)',
        r'\1' + build_file_section + '\n',
        content
    )

    # 2. Add PBXContainerItemProxy for target dependency
    container_proxy_section = f"""		{container_proxy_uuid} /* PBXContainerItemProxy */ = {{
			isa = PBXContainerItemProxy;
			containerPortal = 3A0AE6982AB623F400ACCD68 /* Project object */;
			proxyType = 1;
			remoteGlobalIDString = {multiplatform_uuid};
			remoteInfo = Multiplatform;
		}};"""

    # Find PBXContainerItemProxy section and add our entry
    if '/* Begin PBXContainerItemProxy section */' in content:
        content = re.sub(
            r'(/\* Begin PBXContainerItemProxy section \*/\n)',
            r'\1' + container_proxy_section + '\n',
            content
        )
    else:
        # Add section if it doesn't exist
        content = re.sub(
            r'(/\* End PBXBuildFile section \*/)',
            r'\1\n\n/* Begin PBXContainerItemProxy section */\n' + container_proxy_section + '\n/* End PBXContainerItemProxy section */',
            content
        )

    # 3. Add PBXFileReference for test file
    file_ref_section = f'\t\t{file_ref_uuid} /* LLMGeneratedTest.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = LLMGeneratedTest.swift; sourceTree = "<group>"; }};'

    content = re.sub(
        r'(/\* Begin PBXFileReference section \*/\n)',
        r'\1' + file_ref_section + '\n',
        content
    )

    # Add product reference
    product_ref_section = f'\t\t{product_ref_uuid} /* ShelfPlayerUITests.xctest */ = {{isa = PBXFileReference; explicitFileType = wrapper.cfbundle; includeInIndex = 0; path = ShelfPlayerUITests.xctest; sourceTree = BUILT_PRODUCTS_DIR; }};'

    content = re.sub(
        r'(/\* Begin PBXFileReference section \*/\n)',
        r'\1' + product_ref_section + '\n',
        content
    )

    # 4. Add PBXFrameworksBuildPhase
    frameworks_phase_section = f"""		{frameworks_phase_uuid} /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};"""

    content = re.sub(
        r'(/\* Begin PBXFrameworksBuildPhase section \*/\n)',
        r'\1' + frameworks_phase_section + '\n',
        content
    )

    # 5. Add PBXGroup for test files
    group_section = f"""		{group_uuid} /* ShelfPlayerUITests */ = {{
			isa = PBXGroup;
			children = (
				{file_ref_uuid} /* LLMGeneratedTest.swift */,
			);
			path = ShelfPlayerUITests;
			sourceTree = "<group>";
		}};"""

    # Find main group and add our group
    main_group_uuid = find_main_group_uuid(content)
    if main_group_uuid:
        # Add to main group's children
        content = re.sub(
            rf'({main_group_uuid} = {{[^}}]*children = \([^)]*)',
            rf'\1\n				{group_uuid} /* ShelfPlayerUITests */,',
            content
        )

    # Add group definition
    content = re.sub(
        r'(/\* Begin PBXGroup section \*/\n)',
        r'\1' + group_section + '\n',
        content
    )

    # 6. Add PBXNativeTarget
    target_section = f"""		{target_uuid} /* ShelfPlayerUITests */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {generate_uuid()} /* Build configuration list for PBXNativeTarget "ShelfPlayerUITests" */;
			buildPhases = (
				{sources_phase_uuid} /* Sources */,
				{frameworks_phase_uuid} /* Frameworks */,
				{resources_phase_uuid} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
				{target_dependency_uuid} /* PBXTargetDependency */,
			);
			name = ShelfPlayerUITests;
			productName = ShelfPlayerUITests;
			productReference = {product_ref_uuid} /* ShelfPlayerUITests.xctest */;
			productType = "com.apple.product-type.bundle.ui-testing";
		}};"""

    content = re.sub(
        r'(/\* Begin PBXNativeTarget section \*/\n)',
        r'\1' + target_section + '\n',
        content
    )

    # 7. Add PBXResourcesBuildPhase
    resources_phase_section = f"""		{resources_phase_uuid} /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};"""

    content = re.sub(
        r'(/\* Begin PBXResourcesBuildPhase section \*/\n)',
        r'\1' + resources_phase_section + '\n',
        content
    )

    # 8. Add PBXSourcesBuildPhase
    sources_phase_section = f"""		{sources_phase_uuid} /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{build_file_uuid} /* LLMGeneratedTest.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};"""

    content = re.sub(
        r'(/\* Begin PBXSourcesBuildPhase section \*/\n)',
        r'\1' + sources_phase_section + '\n',
        content
    )

    # 9. Add PBXTargetDependency
    target_dependency_section = f"""		{target_dependency_uuid} /* PBXTargetDependency */ = {{
			isa = PBXTargetDependency;
			target = {multiplatform_uuid} /* Multiplatform */;
			targetProxy = {container_proxy_uuid} /* PBXContainerItemProxy */;
		}};"""

    if '/* Begin PBXTargetDependency section */' in content:
        content = re.sub(
            r'(/\* Begin PBXTargetDependency section \*/\n)',
            r'\1' + target_dependency_section + '\n',
            content
        )
    else:
        content = re.sub(
            r'(/\* End PBXTargetDependency section \*/)',
            r'/* Begin PBXTargetDependency section */\n' + target_dependency_section + '\n/* End PBXTargetDependency section */',
            content
        )

    # 10. Add target to project targets list
    content = re.sub(
        r'(targets = \([^)]*)',
        rf'\1\n				{target_uuid} /* ShelfPlayerUITests */,',
        content
    )

    # 11. Add product to products group
    product_group_uuid = find_product_group_uuid(content)
    if product_group_uuid:
        content = re.sub(
            rf'({product_group_uuid} /\* Products \*/ = {{[^}}]*children = \([^)]*)',
            rf'\1\n				{product_ref_uuid} /* ShelfPlayerUITests.xctest */,',
            content
        )

    # 12. Add build configuration
    build_config_uuid = generate_uuid()
    debug_config_uuid = generate_uuid()
    release_config_uuid = generate_uuid()

    build_config_section = f"""		{build_config_uuid} /* Build configuration list for PBXNativeTarget "ShelfPlayerUITests" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{debug_config_uuid} /* Debug */,
				{release_config_uuid} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};"""

    content = re.sub(
        r'(/\* End XCBuildConfiguration section \*/)',
        r'\1\n\n/* Begin XCConfigurationList section */\n' + build_config_section if '/* Begin XCConfigurationList section */' not in content else '',
        content
    )

    if '/* Begin XCConfigurationList section */' in content:
        content = re.sub(
            r'(/\* Begin XCConfigurationList section \*/\n)',
            r'\1' + build_config_section + '\n',
            content
        )

    # Add Debug configuration
    debug_config_section = f"""		{debug_config_uuid} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = ZBY6DA7QB9;
				GENERATE_INFOPLIST_FILE = YES;
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.tinydeskapps.ShelfPlayerUITests;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = NO;
				SWIFT_VERSION = 6.0;
				TARGETED_DEVICE_FAMILY = "1,2";
				TEST_TARGET_NAME = Multiplatform;
			}};
			name = Debug;
		}};"""

    # Add Release configuration
    release_config_section = f"""		{release_config_uuid} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = ZBY6DA7QB9;
				GENERATE_INFOPLIST_FILE = YES;
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.tinydeskapps.ShelfPlayerUITests;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = NO;
				SWIFT_VERSION = 6.0;
				TARGETED_DEVICE_FAMILY = "1,2";
				TEST_TARGET_NAME = Multiplatform;
			}};
			name = Release;
		}};"""

    content = re.sub(
        r'(/\* Begin XCBuildConfiguration section \*/\n)',
        r'\1' + debug_config_section + '\n' + release_config_section + '\n',
        content
    )

    return content

def update_scheme(scheme_path):
    """Add UI test target to scheme"""
    content = read_file(scheme_path)

    # Add testable reference
    testable_ref = """         <TestableReference
            skipped = "NO"
            parallelizable = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "UITEST_TARGET_UUID"
               BuildableName = "ShelfPlayerUITests.xctest"
               BlueprintName = "ShelfPlayerUITests"
               ReferencedContainer = "container:ShelfPlayer.xcodeproj">
            </BuildableReference>
         </TestableReference>"""

    # Insert before </Testables>
    content = re.sub(
        r'(</Testables>)',
        testable_ref + '\n      \\1',
        content
    )

    write_file(scheme_path, content)
    print(f"✅ Updated scheme: {scheme_path}")

def main():
    print("🚀 Adding ShelfPlayerUITests target to ShelfPlayer.xcodeproj")
    print()

    # Check if files exist
    if not PROJECT_FILE.exists():
        print(f"❌ Error: Project file not found: {PROJECT_FILE}")
        return 1

    if not TEST_FILE.exists():
        print(f"❌ Error: Test file not found: {TEST_FILE}")
        return 1

    # Backup project file
    print(f"📦 Creating backup: {BACKUP_FILE}")
    shutil.copy(PROJECT_FILE, BACKUP_FILE)

    # Read project file
    print("📖 Reading project file...")
    content = read_file(PROJECT_FILE)

    # Find Multiplatform target UUID
    multiplatform_uuid = find_multiplatform_target_uuid(content)
    if not multiplatform_uuid:
        print("❌ Error: Could not find Multiplatform target UUID")
        return 1

    print(f"✅ Found Multiplatform target: {multiplatform_uuid}")

    # Add UI test target
    print("🔧 Adding UI test target...")
    updated_content = add_ui_test_target(content, multiplatform_uuid)

    # Write updated project file
    print("💾 Writing updated project file...")
    write_file(PROJECT_FILE, updated_content)

    # Update scheme
    print("🔧 Updating scheme...")
    # Note: We'll need to manually update the BlueprintIdentifier after getting the actual UUID
    # For now, just add a note
    print("⚠️  You'll need to manually add the test target to the scheme in Xcode")
    print("   OR run: Product > Scheme > Edit Scheme > Test > Add ShelfPlayerUITests")

    print()
    print("✅ Done! UI test target added successfully!")
    print()
    print("Next steps:")
    print("1. Open the project in Xcode:")
    print("   open /Users/mheryerznkanyan/Projects/ShelfPlayer/ShelfPlayer.xcodeproj")
    print("2. Verify the ShelfPlayerUITests target appears in the target list")
    print("3. Edit the scheme (Product > Scheme > Edit Scheme)")
    print("4. Add ShelfPlayerUITests to the Test action")
    print()
    print(f"If something goes wrong, restore from backup:")
    print(f"   cp {BACKUP_FILE} {PROJECT_FILE}")

    return 0

if __name__ == "__main__":
    exit(main())
