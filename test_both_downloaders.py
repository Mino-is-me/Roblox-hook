#!/usr/bin/env python3
"""
Test both 3D downloaders for body part mapping integration
"""

def test_both_downloaders():
    """Test both real_3d_downloader and integrated_3d_downloader"""
    
    print("🧪 Testing Body Part Mapping in Both Downloaders")
    print("=" * 60)
    
    success_count = 0
    
    # Test integrated_3d_downloader
    print("\n1️⃣ Testing integrated_3d_downloader...")
    try:
        from integrated_3d_downloader import RobloxAvatar3DDownloaderIntegrated
        downloader1 = RobloxAvatar3DDownloaderIntegrated("test1")
        
        if hasattr(downloader1, 'generate_body_part_mapping'):
            print("   ✅ Has generate_body_part_mapping method")
            success_count += 1
        else:
            print("   ❌ Missing generate_body_part_mapping method")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test real_3d_downloader
    print("\n2️⃣ Testing real_3d_downloader...")
    try:
        from real_3d_downloader import RobloxAvatar3DDownloader
        downloader2 = RobloxAvatar3DDownloader("test2")
        
        if hasattr(downloader2, 'generate_body_part_mapping'):
            print("   ✅ Has generate_body_part_mapping method")
            success_count += 1
        else:
            print("   ❌ Missing generate_body_part_mapping method")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Summary
    print(f"\n📊 Results: {success_count}/2 downloaders have body part mapping integration")
    
    if success_count == 2:
        print("🎉 All downloaders successfully integrated!")
        return True
    else:
        print("⚠️ Some downloaders are missing integration")
        return False

if __name__ == "__main__":
    success = test_both_downloaders()
    if not success:
        exit(1)