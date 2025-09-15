#!/usr/bin/env python3
"""
실제 3D 다운로더 테스트
"""

from real_3d_downloader import RobloxAvatar3DDownloader

def test_real_3d():
    print("=== 실제 3D API 테스트 ===\n")
    
    downloader = RobloxAvatar3DDownloader("test_real_3d")
    
    # 유저 ID 1 (Roblox 창시자) 테스트
    user_id = 1
    
    print(f"유저 ID {user_id}로 실제 3D 다운로드 테스트 시작...")
    success = downloader.download_avatar_3d_complete(user_id, include_textures=True)
    
    if success:
        print("🎉 실제 3D 다운로드 테스트 성공!")
    else:
        print("❌ 실제 3D 다운로드 테스트 실패")

if __name__ == "__main__":
    test_real_3d()
