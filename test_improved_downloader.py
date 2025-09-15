#!/usr/bin/env python3
"""
개선된 3D 다운로더 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from real_3d_downloader import RobloxAvatar3DDownloader

def test_improved_downloader():
    print("=== 개선된 3D 다운로더 테스트 ===\n")
    
    # 다운로더 생성
    downloader = RobloxAvatar3DDownloader("test_improved_3d")
    
    # 다양한 유저 테스트
    test_users = [
        "builderman",  # 유저명
        "156",         # 유저 ID (문자열)
        1              # 유저 ID (숫자)
    ]
    
    for user_input in test_users:
        print(f"🎯 '{user_input}' 테스트 중...")
        
        # 유저 입력 처리
        user_id = downloader.resolve_user_input(str(user_input))
        
        if user_id:
            # 3D 다운로드 시도
            success = downloader.download_avatar_3d_complete(user_id, include_textures=True)
            
            if success:
                print(f"✅ '{user_input}' 다운로드 성공!\n")
            else:
                print(f"❌ '{user_input}' 다운로드 실패\n")
        else:
            print(f"❌ '{user_input}' 유저 찾기 실패\n")
        
        print("-" * 50)

if __name__ == "__main__":
    test_improved_downloader()
