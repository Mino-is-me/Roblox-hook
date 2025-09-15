#!/usr/bin/env python3
"""
유저명 입력 테스트 스크립트
"""

from real_3d_downloader import RobloxAvatar3DDownloader

def test_username_input():
    print("=== 유저명 입력 테스트 ===\n")
    
    downloader = RobloxAvatar3DDownloader("test_username")
    
    # 다양한 입력 테스트
    test_inputs = [
        "Roblox",        # 유저명
        "builderman",    # 유저명
        "1",             # 유저 ID (숫자)
        "156",           # 유저 ID (숫자)
        "InvalidUser123" # 존재하지 않는 유저명
    ]
    
    for user_input in test_inputs:
        print(f"\n📝 입력 테스트: '{user_input}'")
        user_id = downloader.resolve_user_input(user_input)
        
        if user_id:
            print(f"   결과: 유저 ID {user_id}")
            # 유저 정보 확인
            user_info = downloader.get_user_info(user_id)
            if user_info:
                print(f"   확인: {user_info.get('displayName')} (@{user_info.get('name')})")
        else:
            print(f"   결과: 찾을 수 없음")
        
        print("-" * 50)

if __name__ == "__main__":
    test_username_input()
