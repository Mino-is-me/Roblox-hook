#!/usr/bin/env python3
"""
확장 정보가 포함된 3D 다운로더 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from real_3d_downloader import RobloxAvatar3DDownloader

def test_extended_downloader():
    print("=== 확장 정보 포함 3D 다운로더 테스트 ===\n")
    
    # 다운로더 생성
    downloader = RobloxAvatar3DDownloader("test_extended_full")
    
    # 테스트 사용자 (정보가 많은 사용자 선택)
    username = "builderman"
    
    print(f"🎯 '{username}' 확장 정보 포함 다운로드 테스트...")
    
    # 유저 입력 처리
    user_id = downloader.resolve_user_input(username)
    
    if user_id:
        print(f"✅ 유저 '{username}' → ID: {user_id}")
        
        # 3D 다운로드 (확장 정보 포함)
        success = downloader.download_avatar_3d_complete(user_id, include_textures=True)
        
        if success:
            print(f"\n🎉 '{username}' 확장 정보 포함 다운로드 성공!")
            print("📁 다음 파일들을 확인해보세요:")
            print("   - avatar.obj, avatar.mtl (3D 파일)")
            print("   - textures/ (텍스처들)")
            print("   - metadata.json (확장 아바타 정보 포함)")
            print("   - README.md (상세한 사용법과 아바타 정보)")
        else:
            print(f"❌ '{username}' 다운로드 실패")
    else:
        print(f"❌ '{username}' 유저 찾기 실패")

if __name__ == "__main__":
    test_extended_downloader()