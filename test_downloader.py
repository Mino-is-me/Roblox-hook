#!/usr/bin/env python3
"""
테스트 스크립트 - 로블록스 아바타 다운로더 간단 테스트
"""

from roblox_avatar_downloader import RobloxAvatarDownloader

def test_single_user():
    """단일 유저 테스트"""
    print("=== 단일 유저 테스트 ===")
    
    downloader = RobloxAvatarDownloader("test_downloads")
    
    # 로블록스 창시자 (ID: 1) 테스트
    user_id = 1
    sizes = ["150x150", "420x420"]
    
    print(f"유저 ID {user_id}의 아바타 다운로드 테스트...")
    success = downloader.download_user_avatars(user_id, sizes)
    
    if success:
        print("✅ 테스트 성공!")
    else:
        print("❌ 테스트 실패!")
    
    return success

def test_user_info():
    """유저 정보 가져오기 테스트"""
    print("\n=== 유저 정보 테스트 ===")
    
    downloader = RobloxAvatarDownloader()
    
    # 여러 유명 유저들 테스트
    test_user_ids = [1, 2, 3, 156]
    
    for user_id in test_user_ids:
        user_info = downloader.get_user_info(user_id)
        if user_info:
            print(f"✅ ID {user_id}: {user_info.get('displayName', 'N/A')} (@{user_info.get('name', 'N/A')})")
        else:
            print(f"❌ ID {user_id}: 정보를 가져올 수 없음")

def test_thumbnails():
    """썸네일 URL 가져오기 테스트"""
    print("\n=== 썸네일 URL 테스트 ===")
    
    downloader = RobloxAvatarDownloader()
    user_id = 1  # Roblox 창시자
    
    print(f"유저 ID {user_id}의 썸네일 URL 테스트...")
    
    # 아바타 썸네일
    avatar_data = downloader.get_user_avatar_thumbnails(user_id, "420x420")
    if avatar_data:
        for item in avatar_data:
            if item.get("state") == "Completed":
                print(f"✅ 아바타 URL: {item.get('imageUrl', 'N/A')}")
    
    # 헤드샷 썸네일  
    headshot_data = downloader.get_user_headshot_thumbnails(user_id, "420x420")
    if headshot_data:
        for item in headshot_data:
            if item.get("state") == "Completed":
                print(f"✅ 헤드샷 URL: {item.get('imageUrl', 'N/A')}")
    
    # 흉상 썸네일
    bust_data = downloader.get_user_bust_thumbnails(user_id, "420x420")
    if bust_data:
        for item in bust_data:
            if item.get("state") == "Completed":
                print(f"✅ 흉상 URL: {item.get('imageUrl', 'N/A')}")

def main():
    """메인 테스트 함수"""
    print("=== 로블록스 아바타 다운로더 테스트 ===\n")
    
    try:
        # 1. 유저 정보 테스트
        test_user_info()
        
        # 2. 썸네일 URL 테스트
        test_thumbnails()
        
        # 3. 실제 다운로드 테스트 (사용자 확인 후)
        print("\n실제 다운로드 테스트를 진행하시겠습니까? (y/n): ", end="")
        if input().lower().strip() == 'y':
            test_single_user()
        
        print("\n테스트 완료!")
        
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
