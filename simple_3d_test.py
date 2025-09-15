#!/usr/bin/env python3
"""
간단한 3D 다운로더 테스트
"""

from roblox_3d_downloader import Roblox3DDownloader

def simple_test():
    print("=== 간단한 3D 테스트 ===")
    
    downloader = Roblox3DDownloader("quick_test")
    
    # 유저 정보만 테스트
    user_id = 1
    user_info = downloader.get_user_info(user_id)
    
    if user_info:
        print(f"✅ 유저: {user_info.get('displayName')} (@{user_info.get('name')})")
        
        # 아바타 데이터 테스트
        avatar_data = downloader.get_avatar_data(user_id)
        if avatar_data:
            print(f"✅ 아바타 아이템: {len(avatar_data.get('assets', []))}개")
            print(f"✅ 아바타 타입: {avatar_data.get('playerAvatarType', 'Unknown')}")
            print("🎯 3D 정보 수집 가능!")
        else:
            print("❌ 아바타 데이터 없음")
    else:
        print("❌ 유저 정보 없음")

if __name__ == "__main__":
    simple_test()
