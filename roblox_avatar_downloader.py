#!/usr/bin/env python3
"""
Roblox Avatar & Thumbnail Downloader
로블록스 API를 사용하여 유저 아바타와 썸네일을 다운로드하는 스크립트
"""

import os
import requests
import json
from typing import Optional, List, Dict
from pathlib import Path
import time

class RobloxAvatarDownloader:
    """로블록스 아바타 다운로드 클래스"""
    
    def __init__(self, download_folder: str = "downloads"):
        """
        초기화
        
        Args:
            download_folder (str): 다운로드할 폴더 경로
        """
        self.base_url = "https://www.roblox.com/api"
        self.thumbnails_url = "https://thumbnails.roblox.com"
        self.download_folder = Path(download_folder)
        self.download_folder.mkdir(exist_ok=True)
        
        # 세션 생성 (재사용을 위해)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """
        유저 정보 가져오기
        
        Args:
            user_id (int): 로블록스 유저 ID
            
        Returns:
            Dict: 유저 정보 또는 None
        """
        try:
            url = f"https://users.roblox.com/v1/users/{user_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"유저 정보 가져오기 실패 (ID: {user_id}): {e}")
            return None
    
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
                user_id = result["data"][0].get("id")
                user_name = result["data"][0].get("name")
                print(f"✅ 유저명 '{username}' → ID: {user_id} (@{user_name})")
                return user_id
            else:
                print(f"❌ 유저명 '{username}'을 찾을 수 없습니다.")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 유저 ID 검색 실패 ({username}): {e}")
            return None
    
    def resolve_user_input(self, user_input: str) -> Optional[int]:
        """
        유저 입력을 유저 ID로 변환
        숫자면 ID로 처리, 문자면 유저명으로 처리
        
        Args:
            user_input (str): 유저 입력 (ID 또는 유저명)
            
        Returns:
            int: 유저 ID 또는 None
        """
        user_input = user_input.strip()
        
        # 숫자인 경우 ID로 처리
        if user_input.isdigit():
            user_id = int(user_input)
            print(f"🔍 유저 ID {user_id}로 인식")
            return user_id
        
        # 문자인 경우 유저명으로 처리
        else:
            print(f"🔍 유저명 '{user_input}'으로 검색 중...")
            return self.get_user_id_by_username(user_input)
    
    def get_user_avatar_thumbnails(self, user_id: int, size: str = "420x420") -> Optional[List[Dict]]:
        """
        유저 아바타 썸네일 URL 가져오기
        
        Args:
            user_id (int): 로블록스 유저 ID
            size (str): 썸네일 크기 (30x30, 48x48, 60x60, 75x75, 100x100, 110x110, 140x140, 150x150, 180x180, 352x352, 420x420, 720x720)
            
        Returns:
            List[Dict]: 썸네일 정보 리스트
        """
        try:
            url = f"{self.thumbnails_url}/v1/users/avatar"
            params = {
                "userIds": str(user_id),
                "size": size,
                "format": "Png",
                "isCircular": "false"
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"아바타 썸네일 URL 가져오기 실패 (ID: {user_id}): {e}")
            return None
    
    def get_user_headshot_thumbnails(self, user_id: int, size: str = "420x420") -> Optional[List[Dict]]:
        """
        유저 헤드샷 썸네일 URL 가져오기
        
        Args:
            user_id (int): 로블록스 유저 ID
            size (str): 썸네일 크기
            
        Returns:
            List[Dict]: 썸네일 정보 리스트
        """
        try:
            url = f"{self.thumbnails_url}/v1/users/avatar-headshot"
            params = {
                "userIds": str(user_id),
                "size": size,
                "format": "Png",
                "isCircular": "false"
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"헤드샷 썸네일 URL 가져오기 실패 (ID: {user_id}): {e}")
            return None
    
    def get_user_bust_thumbnails(self, user_id: int, size: str = "420x420") -> Optional[List[Dict]]:
        """
        유저 흉상 썸네일 URL 가져오기
        
        Args:
            user_id (int): 로블록스 유저 ID
            size (str): 썸네일 크기
            
        Returns:
            List[Dict]: 썸네일 정보 리스트
        """
        try:
            url = f"{self.thumbnails_url}/v1/users/avatar-bust"
            params = {
                "userIds": str(user_id),
                "size": size,
                "format": "Png",
                "isCircular": "false"
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"흉상 썸네일 URL 가져오기 실패 (ID: {user_id}): {e}")
            return None
    
    def get_user_avatar_3d_model(self, user_id: int) -> Optional[str]:
        """
        유저 아바타 3D 모델 URL 가져오기
        
        Args:
            user_id (int): 로블록스 유저 ID
            
        Returns:
            str: 3D 모델 URL 또는 None
        """
        try:
            url = f"https://avatar.roblox.com/v1/users/{user_id}/avatar"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            # 아바타 데이터에서 3D 모델 정보 추출
            if data:
                # OBJ 파일 다운로드 URL 생성
                obj_url = f"https://avatar.roblox.com/v1/users/{user_id}/avatar/obj"
                return obj_url
            return None
        except requests.exceptions.RequestException as e:
            print(f"3D 모델 URL 가져오기 실패 (ID: {user_id}): {e}")
            return None
    
    def get_user_avatar_items(self, user_id: int) -> Optional[Dict]:
        """
        유저 아바타 착용 아이템 정보 가져오기
        
        Args:
            user_id (int): 로블록스 유저 ID
            
        Returns:
            Dict: 아바타 아이템 정보 또는 None
        """
        try:
            url = f"https://avatar.roblox.com/v1/users/{user_id}/avatar"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"아바타 아이템 정보 가져오기 실패 (ID: {user_id}): {e}")
            return None
    
    def download_image(self, url: str, file_path: Path) -> bool:
        """
        이미지 다운로드
        
        Args:
            url (str): 이미지 URL
            file_path (Path): 저장할 파일 경로
            
        Returns:
            bool: 성공 여부
        """
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"다운로드 완료: {file_path}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"이미지 다운로드 실패 ({url}): {e}")
            return False
    
    def download_3d_model(self, url: str, file_path: Path) -> bool:
        """
        3D 모델 다운로드 (OBJ 파일)
        
        Args:
            url (str): 3D 모델 URL
            file_path (Path): 저장할 파일 경로
            
        Returns:
            bool: 성공 여부
        """
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"3D 모델 다운로드 완료: {file_path}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"3D 모델 다운로드 실패 ({url}): {e}")
            return False
    
    def download_avatar_textures(self, user_id: int, user_folder: Path) -> bool:
        """
        아바타 텍스처 다운로드
        
        Args:
            user_id (int): 로블록스 유저 ID
            user_folder (Path): 저장할 폴더 경로
            
        Returns:
            bool: 성공 여부
        """
        try:
            # 아바타 아이템 정보 가져오기
            avatar_data = self.get_user_avatar_items(user_id)
            if not avatar_data:
                return False
            
            textures_folder = user_folder / "textures"
            textures_folder.mkdir(exist_ok=True)
            
            success_count = 0
            
            # 착용 중인 아이템들의 텍스처 다운로드
            assets = avatar_data.get("assets", [])
            for asset in assets:
                asset_id = asset.get("id")
                asset_name = asset.get("name", f"asset_{asset_id}")
                asset_type = asset.get("assetType", {}).get("name", "unknown")
                
                if asset_id:
                    # 아이템 썸네일 다운로드
                    thumbnail_url = f"https://thumbnails.roblox.com/v1/assets?assetIds={asset_id}&size=420x420&format=Png"
                    thumb_response = self.session.get(thumbnail_url)
                    
                    if thumb_response.status_code == 200:
                        thumb_data = thumb_response.json()
                        if thumb_data.get("data"):
                            for item in thumb_data["data"]:
                                if item.get("state") == "Completed" and item.get("imageUrl"):
                                    # 안전한 파일명 생성
                                    safe_name = "".join(c for c in asset_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                                    if not safe_name:
                                        safe_name = f"asset_{asset_id}"
                                    
                                    file_name = f"{safe_name}_{asset_type}_{asset_id}.png"
                                    file_path = textures_folder / file_name
                                    
                                    if self.download_image(item["imageUrl"], file_path):
                                        success_count += 1
                                    time.sleep(0.1)
            
            print(f"텍스처 다운로드 완료: {success_count}개")
            return success_count > 0
            
        except Exception as e:
            print(f"텍스처 다운로드 중 오류: {e}")
            return False
    
    def download_user_avatars(self, user_id: int, sizes: List[str] = None, include_3d: bool = False, include_textures: bool = False) -> bool:
        """
        유저의 모든 아바타 이미지 및 3D 모델 다운로드
        
        Args:
            user_id (int): 로블록스 유저 ID
            sizes (List[str]): 다운로드할 크기 리스트
            include_3d (bool): 3D 모델 포함 여부 (실제 OBJ/MTL 파일)
            include_textures (bool): 텍스처 포함 여부
            
        Returns:
            bool: 성공 여부
        """
        if sizes is None:
            sizes = ["150x150", "420x420"]
        
        # 유저 정보 가져오기
        user_info = self.get_user_info(user_id)
        if not user_info:
            return False
        
        username = user_info.get("name", f"user_{user_id}")
        display_name = user_info.get("displayName", username)
        
        print(f"유저 정보: {display_name} (@{username}) - ID: {user_id}")
        
        # 유저별 폴더 생성
        user_folder = self.download_folder / f"{username}_{user_id}"
        user_folder.mkdir(exist_ok=True)
        
        # 유저 정보 저장
        user_info_path = user_folder / "user_info.json"
        with open(user_info_path, 'w', encoding='utf-8') as f:
            json.dump(user_info, f, indent=2, ensure_ascii=False)
        
        success_count = 0
        total_count = 0
        
        # 각 크기별로 2D 이미지 다운로드
        for size in sizes:
            print(f"\n크기 {size} 다운로드 중...")
            
            # 전신 아바타
            avatar_data = self.get_user_avatar_thumbnails(user_id, size)
            if avatar_data:
                for item in avatar_data:
                    if item.get("state") == "Completed" and item.get("imageUrl"):
                        file_name = f"avatar_{size}.png"
                        file_path = user_folder / file_name
                        total_count += 1
                        if self.download_image(item["imageUrl"], file_path):
                            success_count += 1
                        time.sleep(0.1)  # API 제한 방지
            
            # 헤드샷
            headshot_data = self.get_user_headshot_thumbnails(user_id, size)
            if headshot_data:
                for item in headshot_data:
                    if item.get("state") == "Completed" and item.get("imageUrl"):
                        file_name = f"headshot_{size}.png"
                        file_path = user_folder / file_name
                        total_count += 1
                        if self.download_image(item["imageUrl"], file_path):
                            success_count += 1
                        time.sleep(0.1)  # API 제한 방지
            
            # 흉상
            bust_data = self.get_user_bust_thumbnails(user_id, size)
            if bust_data:
                for item in bust_data:
                    if item.get("state") == "Completed" and item.get("imageUrl"):
                        file_name = f"bust_{size}.png"
                        file_path = user_folder / file_name
                        total_count += 1
                        if self.download_image(item["imageUrl"], file_path):
                            success_count += 1
                        time.sleep(0.1)  # API 제한 방지
        
        # 실제 3D 모델 다운로드 (최신 API 사용)
        if include_3d:
            print(f"\n🎯 실제 3D 모델 다운로드 중...")
            try:
                from real_3d_downloader import RobloxAvatar3DDownloader
                
                # 3D 전용 다운로더 사용
                real_3d_downloader = RobloxAvatar3DDownloader(str(user_folder))
                if real_3d_downloader.download_avatar_3d_complete(user_id, include_textures):
                    success_count += 10  # 3D 모델은 큰 작업이므로 보너스 점수
                    print(f"✅ 실제 3D 모델 다운로드 성공!")
                else:
                    print(f"❌ 실제 3D 모델 다운로드 실패")
                    
            except Exception as e:
                print(f"❌ 3D 모델 다운로드 중 오류: {e}")
                
            time.sleep(1)  # 3D 모델은 큰 파일이므로 더 긴 대기
        
        # 텍스처 다운로드 (아바타 아이템들)
        if include_textures and not include_3d:  # 3D 모델에 이미 텍스처가 포함되어 있으면 중복 방지
            print(f"\n아바타 아이템 텍스처 다운로드 중...")
            if self.download_avatar_textures(user_id, user_folder):
                success_count += 5  # 텍스처는 여러 개이므로 보너스 점수
        
        print(f"\n다운로드 완료: {success_count}/{total_count} 성공")
        return success_count > 0
    
    def download_multiple_users(self, user_ids: List[int], sizes: List[str] = None, include_3d: bool = False, include_textures: bool = False) -> None:
        """
        여러 유저의 아바타 다운로드
        
        Args:
            user_ids (List[int]): 유저 ID 리스트
            sizes (List[str]): 다운로드할 크기 리스트
            include_3d (bool): 3D 모델 포함 여부
            include_textures (bool): 텍스처 포함 여부
        """
        print(f"총 {len(user_ids)}명의 유저 아바타 다운로드 시작...")
        if include_3d:
            print("📦 3D 모델 포함")
        if include_textures:
            print("🎨 텍스처 포함")
        
        for i, user_id in enumerate(user_ids, 1):
            print(f"\n[{i}/{len(user_ids)}] 유저 ID {user_id} 처리 중...")
            self.download_user_avatars(user_id, sizes, include_3d, include_textures)
            
            # 다음 유저 처리 전 잠시 대기 (API 제한 방지)
            if i < len(user_ids):
                time.sleep(1)
        
        print(f"\n모든 다운로드 완료! 저장 위치: {self.download_folder.absolute()}")


def main():
    """메인 함수"""
    print("=== 로블록스 아바타 다운로더 ===\n")
    
    # 다운로드 객체 생성
    downloader = RobloxAvatarDownloader("downloads")
    
    # 사용 예시
    print("사용 방법을 선택하세요:")
    print("1. 단일 유저 다운로드 (2D 이미지만)")
    print("2. 단일 유저 다운로드 (2D + 실제 3D 모델)")
    print("3. 단일 유저 다운로드 (2D + 실제 3D + 텍스처)")
    print("4. 여러 유저 다운로드")
    print("5. 예시 실행 (3D 모델 포함)")
    
    try:
        choice = input("\n선택 (1-5): ").strip()
        
        if choice in ["1", "2", "3"]:
            user_input = input("유저 ID 또는 유저명 입력: ").strip()
            user_id = downloader.resolve_user_input(user_input)
            
            if user_id is None:
                print("❌ 유효한 유저를 찾을 수 없습니다.")
                return
            
            sizes = input("크기 입력 (쉼표로 구분, 예: 150x150,420x420) [기본값: 150x150,420x420]: ").strip()
            
            if sizes:
                sizes = [s.strip() for s in sizes.split(",")]
            else:
                sizes = ["150x150", "420x420"]
            
            include_3d = choice in ["2", "3"]
            include_textures = choice == "3"
            
            if include_3d:
                print("🎯 실제 3D 모델(OBJ/MTL)도 함께 다운로드됩니다!")
            if include_textures:
                print("🎨 3D 텍스처도 함께 다운로드됩니다!")
            
            downloader.download_user_avatars(user_id, sizes, include_3d, include_textures)
        
        elif choice == "4":
            user_inputs = input("유저 ID들 또는 유저명들 입력 (쉼표로 구분): ").strip()
            user_input_list = [inp.strip() for inp in user_inputs.split(",")]
            
            # 각 입력을 유저 ID로 변환
            user_ids = []
            for user_input in user_input_list:
                user_id = downloader.resolve_user_input(user_input)
                if user_id:
                    user_ids.append(user_id)
                else:
                    print(f"⚠️ '{user_input}' 건너뜀 (찾을 수 없음)")
            
            if not user_ids:
                print("❌ 유효한 유저를 찾을 수 없습니다.")
                return
            
            print(f"\n📋 총 {len(user_ids)}명의 유저 ID: {user_ids}")
            
            sizes = input("크기 입력 (쉼표로 구분, 예: 150x150,420x420) [기본값: 150x150,420x420]: ").strip()
            
            if sizes:
                sizes = [s.strip() for s in sizes.split(",")]
            else:
                sizes = ["150x150", "420x420"]
            
            print("\n추가 옵션:")
            include_3d = input("실제 3D 모델(OBJ/MTL)도 다운로드하시겠습니까? (y/n) [기본값: n]: ").strip().lower() == 'y'
            include_textures = False
            if include_3d:
                include_textures = input("3D 텍스처도 다운로드하시겠습니까? (y/n) [기본값: y]: ").strip().lower() != 'n'
            
            downloader.download_multiple_users(user_ids, sizes, include_3d, include_textures)
        
        elif choice == "5":
            print("예시 실행: 유명한 로블록스 유저들의 아바타 다운로드 (실제 3D 모델 포함)")
            # 유저명과 ID 혼합 예시
            example_inputs = ["Roblox", "builderman"]  # 유저명들
            
            user_ids = []
            for user_input in example_inputs:
                user_id = downloader.resolve_user_input(user_input)
                if user_id:
                    user_ids.append(user_id)
            
            if user_ids:
                sizes = ["420x420"]
                downloader.download_multiple_users(user_ids, sizes, include_3d=True, include_textures=True)
        
        else:
            print("잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main()
