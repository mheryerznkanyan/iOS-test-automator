#!/usr/bin/env python3
"""
Add UI Test Target to ShelfPlayer - Manual Approach
This script manually adds the necessary entries to create a UI test target
"""

import uuid
import re

PROJECT_FILE = '/Users/mheryerznkanyan/Projects/ShelfPlayer/ShelfPlayer.xcodeproj/project.pbxproj'

def generate_uuid():
    """Generate a unique 24-character hex ID for Xcode"""
    return uuid.uuid4().hex[:24].upper()

print("🔧 Adding UI Test Target to ShelfPlayer...")
print("=" * 60)

try:
    # Read the project file
    print("📂 Reading project file...")
    with open(PROJECT_FILE, 'r') as f:
        content = f.read()

    # Generate UUIDs for new objects
    test_file_ref_id = generate_uuid()
    test_file_build_id = generate_uuid()
    test_target_id = generate_uuid()
    test_product_ref_id = generate_uuid()
    test_sources_phase_id = generate_uuid()
    test_frameworks_phase_id = generate_uuid()
    test_resources_phase_id = generate_uuid()
    test_dependency_id = generate_uuid()
    test_target_dependency_id = generate_uuid()
    test_container_item_proxy_id = generate_uuid()

    # Find the Multiplatform target ID
    multiplatform_match = re.search(r'([A-F0-9]{24}) /\* Multiplatform \*/ = \{[^}]*isa = PBXNativeTarget', content)
    if not multiplatform_match:
        raise Exception("Could not find Multiplatform target")
    multiplatform_target_id = multiplatform_match.group(1)
    print(f"✅ Found Multiplatform target: {multiplatform_target_id}")

    # Find the Products group
    products_match = re.search(r'([A-F0-9]{24}) /\* Products \*/ = \{', content)
    if not products_match:
        raise Exception("Could not find Products group")
    products_group_id = products_match.group(1)

    # 1. Add file reference for LLMGeneratedTest.swift
    print("📝 Adding test file reference...")
    file_ref_section = re.search(r'(/\* Begin PBXFileReference section \*/.*?/\* End PBXFileReference section \*/)', content, re.DOTALL)
    if file_ref_section:
        new_file_ref = f"""		{test_file_ref_id} /* LLMGeneratedTest.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = LLMGeneratedTest.swift; sourceTree = "<group>"; }};
		{test_product_ref_id} /* ShelfPlayerUITests.xctest */ = {{isa = PBXFileReference; explicitFileType = wrapper.cfbundle; includeInIndex = 0; path = ShelfPlayerUITests.xctest; sourceTree = BUILT_PRODUCTS_DIR; }};
/* End PBXFileReference section */"""
        content = content.replace('/* End PBXFileReference section */', new_file_ref)

    # 2. Add build file
    print("🔨 Adding build file...")
    build_file_section = re.search(r'(/\* Begin PBXBuildFile section \*/)', content)
    if build_file_section:
        new_build_file = f"""/* Begin PBXBuildFile section */
		{test_file_build_id} /* LLMGeneratedTest.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {test_file_ref_id} /* LLMGeneratedTest.swift */; }};
"""
        content = content.replace('/* Begin PBXBuildFile section */', new_build_file)

    # 3. Add PBXGroup for ShelfPlayerUITests
    print("📁 Adding UI test group...")
    # Find where to insert the group (after ShelfPlayerTests)
    test_group_match = re.search(r'([A-F0-9]{24}) /\* ShelfPlayerTests \*/ = \{[^}]*isa = PBXFileSystemSynchronizedRootGroup[^}]*\};', content)
    if test_group_match:
        new_group = f"""
		{generate_uuid()} /* ShelfPlayerUITests */ = {{
			isa = PBXGroup;
			children = (
				{test_file_ref_id} /* LLMGeneratedTest.swift */,
			);
			path = ShelfPlayerUITests;
			sourceTree = "<group>";
		}};"""
        insert_pos = test_group_match.end()
        content = content[:insert_pos] + new_group + content[insert_pos:]

    # 4. Add the UI test target
    print("🎯 Adding UI test target...")
    native_target_section = re.search(r'(/\* End PBXNativeTarget section \*/)', content)
    if native_target_section:
        new_target = f"""		{test_target_id} /* ShelfPlayerUITests */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {generate_uuid()} /* Build configuration list for PBXNativeTarget "ShelfPlayerUITests" */;
			buildPhases = (
				{test_sources_phase_id} /* Sources */,
				{test_frameworks_phase_id} /* Frameworks */,
				{test_resources_phase_id} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
				{test_dependency_id} /* PBXTargetDependency */,
			);
			name = ShelfPlayerUITests;
			productName = ShelfPlayerUITests;
			productReference = {test_product_ref_id} /* ShelfPlayerUITests.xctest */;
			productType = "com.apple.product-type.bundle.ui-testing";
		}};
/* End PBXNativeTarget section */"""
        content = content.replace('/* End PBXNativeTarget section */', new_target)

    # 5. Add build phases
    print("⚙️  Adding build phases...")
    # Sources phase
    sources_phase = f"""
/* Begin PBXSourcesBuildPhase section */
		{test_sources_phase_id} /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{test_file_build_id} /* LLMGeneratedTest.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
"""

    # Find PBXSourcesBuildPhase section
    sources_section_match = re.search(r'(/\* Begin PBXSourcesBuildPhase section \*/)', content)
    if sources_section_match:
        content = content.replace('/* Begin PBXSourcesBuildPhase section */', sources_phase)

    # Frameworks phase
    frameworks_phase = f"""		{test_frameworks_phase_id} /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
"""
    frameworks_section_match = re.search(r'(/\* Begin PBXFrameworksBuildPhase section \*/)', content)
    if frameworks_section_match:
        insert_pos = frameworks_section_match.end()
        content = content[:insert_pos] + "\n" + frameworks_phase + content[insert_pos:]

    # Resources phase
    resources_phase = f"""		{test_resources_phase_id} /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
"""
    resources_section_match = re.search(r'(/\* Begin PBXResourcesBuildPhase section \*/)', content)
    if resources_section_match:
        insert_pos = resources_section_match.end()
        content = content[:insert_pos] + "\n" + resources_phase + content[insert_pos:]

    # 6. Add target dependency
    print("🔗 Adding target dependency...")
    target_dependency = f"""		{test_dependency_id} /* PBXTargetDependency */ = {{
			isa = PBXTargetDependency;
			target = {multiplatform_target_id} /* Multiplatform */;
			targetProxy = {test_container_item_proxy_id} /* PBXContainerItemProxy */;
		}};
"""
    dependency_section_match = re.search(r'(/\* Begin PBXTargetDependency section \*/)', content)
    if dependency_section_match:
        insert_pos = dependency_section_match.end()
        content = content[:insert_pos] + "\n" + target_dependency + content[insert_pos:]

    # 7. Add container item proxy
    container_proxy = f"""		{test_container_item_proxy_id} /* PBXContainerItemProxy */ = {{
			isa = PBXContainerItemProxy;
			containerPortal = 3A0AE6992AB623F400ACCD68 /* Project object */;
			proxyType = 1;
			remoteGlobalIDString = {multiplatform_target_id};
			remoteInfo = Multiplatform;
		}};
"""
    proxy_section_match = re.search(r'(/\* Begin PBXContainerItemProxy section \*/)', content)
    if proxy_section_match:
        insert_pos = proxy_section_match.end()
        content = content[:insert_pos] + "\n" + container_proxy + content[insert_pos:]

    # 8. Add product to Products group and project targets
    print("📦 Adding product reference...")
    # Add to Products group children
    products_children_match = re.search(rf'{products_group_id} /\* Products \*/ = \{{[^}}]*children = \(([^)]*)\)', content, re.DOTALL)
    if products_children_match:
        children_content = products_children_match.group(1)
        new_children = children_content.rstrip() + f"\n\t\t\t\t{test_product_ref_id} /* ShelfPlayerUITests.xctest */,"
        content = content.replace(products_children_match.group(1), new_children)

    # Add to project targets
    project_targets_match = re.search(r'(targets = \([^)]*)', content)
    if project_targets_match:
        targets_content = project_targets_match.group(1)
        new_targets = targets_content + f"\n\t\t\t\t{test_target_id} /* ShelfPlayerUITests */,"
        content = content.replace(targets_content, new_targets)

    # Write the modified project file
    print("💾 Saving project file...")
    with open(PROJECT_FILE, 'w') as f:
        f.write(content)

    print("\n" + "=" * 60)
    print("✅ UI Test Target Added Successfully!")
    print("\n⚠️  Important: You need to add build configurations for the target")
    print("Open the project in Xcode and:")
    print("1. Select the ShelfPlayerUITests target")
    print("2. Go to Build Settings")
    print("3. Configure any necessary settings")
    print("\nThen you can run tests using Streamlit!")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    # Restore backup
    print("\n🔄 Restoring from backup...")
    import shutil
    shutil.copy(PROJECT_FILE + '.backup', PROJECT_FILE)
    print("✅ Backup restored")
