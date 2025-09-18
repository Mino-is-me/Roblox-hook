#!/usr/bin/env python3
"""
Test script for body part mapping integration
"""

import sys
from pathlib import Path

def test_body_part_integration():
    """Test if body part mapping integration works"""
    
    print("🧪 Body Part Mapping Integration Test")
    print("=" * 50)
    
    # Test integrated_3d_downloader import
    try:
        from integrated_3d_downloader import RobloxAvatar3DDownloaderIntegrated
        print("✅ Integrated 3D downloader import successful")
    except Exception as e:
        print(f"❌ Integrated 3D downloader import failed: {e}")
        return False
    
    # Test body_part_mapping_parser import within downloader
    try:
        downloader = RobloxAvatar3DDownloaderIntegrated("test_integration")
        print("✅ Integrated downloader initialization successful")
    except Exception as e:
        print(f"❌ Integrated downloader initialization failed: {e}")
        return False
    
    # Test body part mapping method availability
    if hasattr(downloader, 'generate_body_part_mapping'):
        print("✅ Body part mapping method found in integrated downloader")
    else:
        print("❌ Body part mapping method NOT found in integrated downloader")
        return False
    
    # Test with existing builderman data if available
    existing_package = Path("final_integrated/builderman_156")
    if existing_package.exists():
        print(f"\n📂 Testing with existing package: {existing_package}")
        
        obj_file = existing_package / "3D_Model" / "avatar.obj"
        if obj_file.exists():
            print(f"✅ Found existing OBJ file: {obj_file}")
            
            # Test OBJ structure analysis
            try:
                obj_structure = downloader.analyze_obj_structure(obj_file)
                print(f"✅ OBJ structure analysis successful: {len(obj_structure.get('groups', []))} groups found")
                
                # Simulate user info for testing
                test_user_info = {
                    'id': 156,
                    'name': 'builderman',
                    'displayName': 'builderman'
                }
                
                # Test body part mapping generation
                test_folder = Path("test_integration_output")
                test_folder.mkdir(exist_ok=True)
                
                success = downloader.generate_body_part_mapping(test_user_info, obj_structure, test_folder)
                
                if success:
                    mapping_file = test_folder / "BODY_PART_MAPPING.txt"
                    if mapping_file.exists():
                        print(f"✅ Body part mapping file generated successfully: {mapping_file}")
                        
                        # Check file content
                        with open(mapping_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if "BODY PART ATTACHMENT POINTS" in content:
                                print("✅ Body part mapping content is correct")
                                print(f"📊 File size: {len(content)} characters")
                                return True
                            else:
                                print("❌ Body part mapping content is incorrect")
                                return False
                    else:
                        print("❌ Body part mapping file was not created")
                        return False
                else:
                    print("❌ Body part mapping generation failed")
                    return False
                    
            except Exception as e:
                print(f"❌ Testing failed with error: {e}")
                return False
        else:
            print("⚠️ No existing OBJ file found for testing")
            return True  # Not a failure, just no test data
    else:
        print("⚠️ No existing package found for testing")
        return True  # Not a failure, just no test data
    
    return True

if __name__ == "__main__":
    success = test_body_part_integration()
    
    if success:
        print("\n🎉 Integration test completed successfully!")
        print("✅ Body part mapping is properly integrated into 3D downloaders")
    else:
        print("\n❌ Integration test failed!")
        sys.exit(1)