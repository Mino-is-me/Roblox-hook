#!/usr/bin/env python3
"""
Roblox Username to User ID Converter
로블록스 유저명으로 유저 ID를 찾는 헬퍼 스크립트
"""

import requests
import json
from typing import List, Dict, Optional

class RobloxUserLookup:
    """로블록스 유저 검색 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json'
        })
    
    def get_user_id_by_username(self, username: str) -> Optional[int]:
        """
        유저명으로 유저 ID 찾기
        
        Args:
            username (str): 로블록스 유저명
            
        Returns:
            int: 유저 ID 또는 None
        """
        try:
            url = "https://users.roblox.com/v1/usernames/users"
            data = {"usernames": [username]}
            
            response = self.session.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("data") and len(result["data"]) > 0:
                return result["data"][0].get("id")
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"유저 ID 검색 실패 ({username}): {e}")
            return None
    
    def get_user_ids_by_usernames(self, usernames: List[str]) -> Dict[str, Optional[int]]:
        """
        여러 유저명으로 유저 ID들 찾기
        
        Args:
            usernames (List[str]): 유저명 리스트
            
        Returns:
            Dict[str, Optional[int]]: 유저명 -> 유저 ID 매핑
        """
        result = {}
        
        # API는 한 번에 최대 10개까지만 처리 가능
        for i in range(0, len(usernames), 10):
            batch = usernames[i:i+10]
            
            try:
                url = "https://users.roblox.com/v1/usernames/users"
                data = {"usernames": batch}
                
                response = self.session.post(url, json=data)
                response.raise_for_status()
                
                response_data = response.json()
                found_users = {user["name"].lower(): user["id"] for user in response_data.get("data", [])}
                
                # 결과 매핑
                for username in batch:
                    result[username] = found_users.get(username.lower())
                    
            except requests.exceptions.RequestException as e:
                print(f"배치 검색 실패 ({batch}): {e}")
                for username in batch:
                    result[username] = None
        
        return result
    
    def search_users_by_keyword(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        키워드로 유저 검색 (완전한 유저명을 모를 때 사용)
        
        Args:
            keyword (str): 검색 키워드
            limit (int): 최대 결과 수
            
        Returns:
            List[Dict]: 검색된 유저 정보 리스트
        """
        try:
            # 이 API는 공식적이지 않으므로 변경될 수 있습니다
            url = f"https://users.roblox.com/v1/users/search"
            params = {
                "keyword": keyword,
                "limit": min(limit, 25)  # 최대 25개
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            result = response.json()
            return result.get("data", [])
            
        except requests.exceptions.RequestException as e:
            print(f"유저 검색 실패 ({keyword}): {e}")
            return []


def main():
    """메인 함수"""
    print("=== 로블록스 유저명 → 유저 ID 변환기 ===\n")
    
    lookup = RobloxUserLookup()
    
    print("사용 방법을 선택하세요:")
    print("1. 단일 유저명으로 ID 찾기")
    print("2. 여러 유저명으로 ID들 찾기")
    print("3. 키워드로 유저 검색")
    
    try:
        choice = input("\n선택 (1-3): ").strip()
        
        if choice == "1":
            username = input("유저명 입력: ").strip()
            user_id = lookup.get_user_id_by_username(username)
            
            if user_id:
                print(f"\n✅ 찾았습니다!")
                print(f"유저명: {username}")
                print(f"유저 ID: {user_id}")
                print(f"프로필 URL: https://www.roblox.com/users/{user_id}/profile")
            else:
                print(f"\n❌ 유저명 '{username}'를 찾을 수 없습니다.")
        
        elif choice == "2":
            usernames_input = input("유저명들 입력 (쉼표로 구분): ").strip()
            usernames = [name.strip() for name in usernames_input.split(",")]
            
            print(f"\n{len(usernames)}개의 유저명을 검색 중...")
            results = lookup.get_user_ids_by_usernames(usernames)
            
            print(f"\n=== 검색 결과 ===")
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
        
        elif choice == "3":
            keyword = input("검색 키워드 입력: ").strip()
            limit = input("최대 결과 수 (기본값: 10): ").strip()
            
            try:
                limit = int(limit) if limit else 10
            except ValueError:
                limit = 10
            
            print(f"\n'{keyword}' 검색 중...")
            results = lookup.search_users_by_keyword(keyword, limit)
            
            if results:
                print(f"\n=== 검색 결과 ({len(results)}개) ===")
                for i, user in enumerate(results, 1):
                    print(f"{i}. {user.get('displayName', 'N/A')} (@{user.get('name', 'N/A')})")
                    print(f"   ID: {user.get('id', 'N/A')}")
                    print(f"   설명: {user.get('description', 'N/A')[:50]}...")
                    print()
                
                # ID 리스트 출력
                ids = [str(user.get('id')) for user in results if user.get('id')]
                if ids:
                    print(f"모든 ID들 (아바타 다운로더용):")
                    print(f"{','.join(ids)}")
            else:
                print(f"\n❌ '{keyword}'로 검색된 유저가 없습니다.")
        
        else:
            print("잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main()
