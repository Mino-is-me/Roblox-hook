#!/usr/bin/env python3
"""
유저명으로 3D 다운로드 테스트
"""

from real_3d_downloader import RobloxAvatar3DDownloader

def test_username_3d_download():
    print("=== 유저명으로 3D 다운로드 테스트 ===\n")
    
    downloader = RobloxAvatar3DDownloader("test_username_3d")
    
    # 유저명으로 다운로드 테스트
    username = "builderman"
    
    print(f"유저명 '{username}'으로 3D 아바타 다운로드 테스트...")
    
    # 유저명을 ID로 변환
    user_id = downloader.resolve_user_input(username)
    
    if user_id:
        print(f"✅ 유저 ID {user_id}로 변환 완료")
        
        # 실제 3D 다운로드 실행
        success = downloader.download_avatar_3d_complete(user_id, include_textures=True)
        
        if success:
            print("🎉 유저명으로 3D 다운로드 테스트 성공!")
        else:
            print("❌ 3D 다운로드 실패")
    else:
        print("❌ 유저명을 ID로 변환 실패")

if __name__ == "__main__":
    test_username_3d_download()
