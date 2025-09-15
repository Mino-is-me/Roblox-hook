#!/usr/bin/env python3
"""
유저명 검색 테스트 스크립트
"""

from username_to_id import RobloxUserLookup

def test_username_lookup():
    """유저명 검색 테스트"""
    print("=== 유저명 → ID 변환 테스트 ===\n")
    
    lookup = RobloxUserLookup()
    
    # 단일 유저명 테스트
    test_usernames = ["Roblox", "builderman", "John Doe", "Jane Doe"]
    
    print("단일 유저명 검색 테스트:")
    for username in test_usernames:
        user_id = lookup.get_user_id_by_username(username)
        if user_id:
            print(f"✅ {username} → ID: {user_id}")
        else:
            print(f"❌ {username} → 찾을 수 없음")
    
    print(f"\n여러 유저명 일괄 검색 테스트:")
    results = lookup.get_user_ids_by_usernames(test_usernames)
    
    found_ids = []
    for username, user_id in results.items():
        if user_id:
            print(f"✅ {username} → ID: {user_id}")
            found_ids.append(user_id)
        else:
            print(f"❌ {username} → 찾을 수 없음")
    
    if found_ids:
        print(f"\n발견된 ID들 (아바타 다운로더용):")
        print(f"{','.join(map(str, found_ids))}")
    
    # 키워드 검색 테스트
    print(f"\n키워드 검색 테스트 ('roblox'):")
    search_results = lookup.search_users_by_keyword("roblox", 5)
    
    if search_results:
        for i, user in enumerate(search_results, 1):
            print(f"{i}. {user.get('displayName', 'N/A')} (@{user.get('name', 'N/A')}) - ID: {user.get('id', 'N/A')}")
    else:
        print("검색 결과 없음")

if __name__ == "__main__":
    test_username_lookup()
