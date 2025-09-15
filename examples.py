#!/usr/bin/env python3
"""
로블록스 아바타 다운로더 - 사용 예시
"""

from roblox_avatar_downloader import RobloxAvatarDownloader
from username_to_id import RobloxUserLookup

def example_download_by_id():
    """유저 ID로 다운로드 예시"""
    print("=== 예시 1: 유저 ID로 아바타 다운로드 ===")
    
    # 다운로더 객체 생성
    downloader = RobloxAvatarDownloader("example_downloads")
    
    # 유명한 로블록스 유저들의 ID
    user_ids = [1, 156]  # Roblox, builderman
    sizes = ["150x150", "420x420"]
    
    print(f"유저 ID {user_ids}의 아바타를 다운로드합니다...")
    downloader.download_multiple_users(user_ids, sizes)

def example_download_by_username():
    """유저명으로 다운로드 예시"""
    print("\n=== 예시 2: 유저명으로 아바타 다운로드 ===")
    
    # 유저명으로 ID 찾기
    lookup = RobloxUserLookup()
    usernames = ["Roblox", "builderman"]
    
    print(f"유저명 {usernames}를 ID로 변환 중...")
    username_to_id = lookup.get_user_ids_by_usernames(usernames)
    
    # 찾은 ID들로 다운로드
    found_ids = [user_id for user_id in username_to_id.values() if user_id]
    
    if found_ids:
        print(f"찾은 ID들: {found_ids}")
        downloader = RobloxAvatarDownloader("username_downloads")
        sizes = ["420x420", "720x720"]  # 고해상도
        downloader.download_multiple_users(found_ids, sizes)
    else:
        print("유효한 유저 ID를 찾지 못했습니다.")

def example_high_quality_download():
    """고품질 다운로드 예시"""
    print("\n=== 예시 3: 고품질 아바타 다운로드 ===")
    
    downloader = RobloxAvatarDownloader("high_quality")
    
    # 최고 해상도로 다운로드
    user_id = 1  # Roblox
    sizes = ["720x720"]  # 최고 해상도
    
    print(f"유저 ID {user_id}의 최고 품질 아바타를 다운로드합니다...")
    downloader.download_user_avatars(user_id, sizes)

def example_custom_usage():
    """커스텀 사용법 예시"""
    print("\n=== 예시 4: 커스텀 사용법 ===")
    
    downloader = RobloxAvatarDownloader("custom_downloads")
    
    # 특정 유저의 정보만 먼저 확인
    user_id = 156  # builderman
    user_info = downloader.get_user_info(user_id)
    
    if user_info:
        print(f"유저 정보:")
        print(f"  이름: {user_info.get('displayName')} (@{user_info.get('name')})")
        print(f"  설명: {user_info.get('description', 'N/A')[:100]}...")
        print(f"  가입일: {user_info.get('created', 'N/A')}")
        print(f"  인증 배지: {'✅' if user_info.get('hasVerifiedBadge') else '❌'}")
        
        # 썸네일 URL만 가져오기 (다운로드 없이)
        avatar_data = downloader.get_user_avatar_thumbnails(user_id, "420x420")
        if avatar_data and avatar_data[0].get("imageUrl"):
            print(f"  아바타 URL: {avatar_data[0]['imageUrl']}")
        
        # 실제 다운로드 여부 묻기
        response = input(f"\n이 유저의 아바타를 다운로드하시겠습니까? (y/n): ")
        if response.lower().strip() == 'y':
            sizes = ["150x150", "420x420"]
            downloader.download_user_avatars(user_id, sizes)

def main():
    """메인 함수"""
    print("=== 로블록스 아바타 다운로더 사용 예시 ===\n")
    
    try:
        # 예시 1: ID로 다운로드
        example_download_by_id()
        
        # 예시 2: 유저명으로 다운로드
        example_download_by_username()
        
        # 예시 3: 고품질 다운로드
        example_high_quality_download()
        
        # 예시 4: 커스텀 사용법
        example_custom_usage()
        
        print(f"\n모든 예시 완료! 다운로드된 파일들을 확인하세요.")
        
    except KeyboardInterrupt:
        print(f"\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
