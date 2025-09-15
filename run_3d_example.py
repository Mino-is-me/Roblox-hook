#!/usr/bin/env python3
"""
3D 다운로더 예시 실행
"""

from roblox_3d_downloader import Roblox3DDownloader

def run_example():
    print("=== 3D 아바타 다운로더 예시 실행 ===\n")
    
    downloader = Roblox3DDownloader("example_3d")
    
    # 유명한 로블록스 유저 1명만 테스트
    user_id = 1  # Roblox 창시자
    
    print(f"유저 ID {user_id}의 3D 아바타 정보 다운로드 중...")
    success = downloader.download_3d_avatar(user_id, include_textures=True)
    
    if success:
        print("\n🎉 예시 실행 완료!")
    else:
        print("\n❌ 예시 실행 실패")

if __name__ == "__main__":
    run_example()
