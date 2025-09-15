#!/usr/bin/env python3
"""
Roblox 3D Avatar Model Downloader
로블록스 3D 아바타 모델 전용 다운로더
"""

import os
import requests
import json
from typing import Optional, List, Dict
from pathlib import Path
import time
import zipfile

class Roblox3DDownloader:
    """로블록스 3D 모델 다운로더 클래스"""
    
    def __init__(self, download_folder: str = "3d_models"):
        """
        초기화
        
        Args:
            download_folder (str): 다운로드할 폴더 경로
        """
        self.download_folder = Path(download_folder)
        self.download_folder.mkdir(exist_ok=True)
        
        # 세션 생성
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """유저 정보 가져오기"""
        try:
            url = f"https://users.roblox.com/v1/users/{user_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"유저 정보 가져오기 실패 (ID: {user_id}): {e}")
            return None
    
    def get_avatar_data(self, user_id: int) -> Optional[Dict]:
        """아바타 데이터 가져오기"""
        try:
            url = f"https://avatar.roblox.com/v1/users/{user_id}/avatar"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"아바타 데이터 가져오기 실패 (ID: {user_id}): {e}")
            return None
    
    def download_obj_model(self, user_id: int, user_folder: Path) -> bool:
        """OBJ 3D 모델 다운로드 (대체 방법)"""
        print("⚠️  로블록스에서 직접 OBJ 다운로드는 더 이상 지원되지 않습니다.")
        print("🔄 대신 아바타 구성 요소 정보를 수집합니다...")
        
        # 아바타 구성 정보 저장
        try:
            avatar_data = self.get_avatar_data(user_id)
            if avatar_data:
                # 아바타 구성 정보를 상세히 저장
                detailed_info = {
                    "avatar_type": avatar_data.get("playerAvatarType", "R15"),
                    "scales": avatar_data.get("scales", {}),
                    "body_colors": avatar_data.get("bodyColors", {}),
                    "assets": [],
                    "note": "로블록스에서 직접 OBJ 다운로드는 지원되지 않습니다. 이 정보를 사용하여 Roblox Studio에서 아바타를 재구성할 수 있습니다."
                }
                
                # 각 아이템의 상세 정보 수집
                for asset in avatar_data.get("assets", []):
                    asset_id = asset.get("id")
                    if asset_id:
                        try:
                            # 아이템 상세 정보 가져오기
                            detail_url = f"https://catalog.roblox.com/v1/assets/{asset_id}/details"
                            detail_response = self.session.get(detail_url)
                            
                            if detail_response.status_code == 200:
                                detail_data = detail_response.json()
                                
                                asset_info = {
                                    "id": asset_id,
                                    "name": asset.get("name"),
                                    "assetType": asset.get("assetType"),
                                    "meta": asset.get("meta", {}),
                                    "details": detail_data,
                                    "catalog_url": f"https://www.roblox.com/catalog/{asset_id}",
                                    "thumbnail_url": f"https://thumbnails.roblox.com/v1/assets?assetIds={asset_id}&size=420x420&format=Png"
                                }
                                detailed_info["assets"].append(asset_info)
                                
                        except Exception as e:
                            print(f"아이템 {asset_id} 정보 수집 실패: {e}")
                
                # 상세 아바타 정보 저장
                avatar_composition_file = user_folder / "avatar_composition.json"
                with open(avatar_composition_file, 'w', encoding='utf-8') as f:
                    json.dump(detailed_info, f, indent=2, ensure_ascii=False)
                
                print(f"📦 아바타 구성 정보 저장: {avatar_composition_file}")
                
                # Roblox Studio 스크립트 생성
                self.create_studio_script(detailed_info, user_folder)
                
                return True
            
        except Exception as e:
            print(f"아바타 구성 정보 수집 실패: {e}")
            return False
        
        return False
    
    def create_studio_script(self, avatar_info: Dict, user_folder: Path):
        """Roblox Studio에서 아바타를 재구성하는 스크립트 생성"""
        script_content = f'''-- 로블록스 스튜디오에서 아바타 재구성 스크립트
-- 이 스크립트를 Roblox Studio의 ServerScript에 붙여넣고 실행하세요

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

-- 아바타 타입: {avatar_info.get("avatar_type", "R15")}

local assetIds = {{
'''
        
        # 아이템 ID들 추가
        for asset in avatar_info.get("assets", []):
            asset_id = asset.get("id")
            asset_name = asset.get("name", "Unknown")
            if asset_id:
                script_content += f'    {asset_id}, -- {asset_name}\n'
        
        script_content += '''
}

-- 아바타 생성 함수
local function createAvatar()
    local humanoid = workspace:FindFirstChild("Humanoid")
    if not humanoid then
        print("Humanoid not found. Please create a character first.")
        return
    end
    
    -- 아이템 착용
    for _, assetId in pairs(assetIds) do
        local success, result = pcall(function()
            humanoid:AddAccessory(assetId)
        end)
        
        if success then
            print("Added asset: " .. assetId)
        else
            print("Failed to add asset: " .. assetId .. " - " .. tostring(result))
        end
        
        wait(0.1) -- API 제한 방지
    end
end

-- 실행
createAvatar()
print("아바타 재구성 완료!")
'''
        
        script_file = user_folder / "roblox_studio_script.lua"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"📜 Roblox Studio 스크립트 생성: {script_file}")
    
    def download_mtl_file(self, user_id: int, user_folder: Path) -> bool:
        """MTL 재질 파일 다운로드 (존재하는 경우)"""
        try:
            # MTL 파일 URL 시도
            url = f"https://avatar.roblox.com/v1/users/{user_id}/avatar/mtl"
            response = self.session.get(url, stream=True)
            
            if response.status_code == 200:
                mtl_file = user_folder / "avatar_model.mtl"
                with open(mtl_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"🎨 MTL 재질 파일 다운로드 완료: {mtl_file}")
                return True
            else:
                print(f"MTL 파일이 존재하지 않습니다 (ID: {user_id})")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"MTL 파일 다운로드 실패 (ID: {user_id}): {e}")
            return False
    
    def download_asset_textures(self, avatar_data: Dict, user_folder: Path) -> int:
        """아바타 아이템의 텍스처들 다운로드"""
        textures_folder = user_folder / "textures"
        textures_folder.mkdir(exist_ok=True)
        
        downloaded_count = 0
        assets = avatar_data.get("assets", [])
        
        print(f"🎨 {len(assets)}개의 아이템 텍스처 다운로드 중...")
        
        for asset in assets:
            asset_id = asset.get("id")
            asset_name = asset.get("name", f"asset_{asset_id}")
            asset_type = asset.get("assetType", {}).get("name", "unknown")
            
            if asset_id:
                # 아이템 상세 정보 가져오기
                try:
                    detail_url = f"https://catalog.roblox.com/v1/assets/{asset_id}/details"
                    detail_response = self.session.get(detail_url)
                    
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        
                        # 텍스처 이미지 다운로드
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
                                        
                                        tex_response = self.session.get(item["imageUrl"], stream=True)
                                        if tex_response.status_code == 200:
                                            with open(file_path, 'wb') as f:
                                                for chunk in tex_response.iter_content(chunk_size=8192):
                                                    f.write(chunk)
                                            downloaded_count += 1
                                            print(f"  ✅ {file_name}")
                                        
                                        time.sleep(0.1)  # API 제한 방지
                
                except Exception as e:
                    print(f"  ❌ 아이템 {asset_id} 텍스처 다운로드 실패: {e}")
                    continue
        
        return downloaded_count
    
    def create_model_info(self, user_id: int, user_info: Dict, avatar_data: Dict, user_folder: Path):
        """3D 모델 정보 파일 생성"""
        model_info = {
            "user_info": user_info,
            "avatar_data": avatar_data,
            "model_files": {
                "avatar_composition": "avatar_composition.json",
                "studio_script": "roblox_studio_script.lua",
                "textures_folder": "textures/"
            },
            "download_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "instructions": {
                "roblox_studio": "Roblox Studio에서 roblox_studio_script.lua 스크립트를 실행하여 아바타를 재구성하세요",
                "blender_alternative": "각 아이템 ID를 사용하여 Roblox 에셋을 개별적으로 추출할 수 있습니다",
                "note": "로블록스에서 직접 OBJ 다운로드는 더 이상 지원되지 않습니다. 대신 아바타 구성 정보를 제공합니다."
            },
            "asset_count": len(avatar_data.get("assets", [])),
            "avatar_type": avatar_data.get("playerAvatarType", "R15"),
            "body_colors": avatar_data.get("bodyColors", {}),
            "scales": avatar_data.get("scales", {})
        }
        
        info_file = user_folder / "model_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(model_info, f, indent=2, ensure_ascii=False)
        
        print(f"📄 모델 정보 파일 생성: {info_file}")
        
        # 사용법 안내 파일도 생성
        readme_content = f"""# 아바타 3D 모델 사용법

## 📁 포함된 파일들
- `avatar_composition.json`: 아바타의 전체 구성 정보
- `roblox_studio_script.lua`: Roblox Studio에서 아바타 재구성 스크립트
- `textures/`: 아바타 아이템들의 텍스처 이미지
- `model_info.json`: 상세 메타데이터

## 🎮 Roblox Studio에서 사용하기
1. Roblox Studio를 열고 새 프로젝트를 생성합니다
2. Workspace에 캐릭터 또는 Humanoid를 배치합니다
3. `roblox_studio_script.lua` 파일의 내용을 ServerScript에 복사합니다
4. 스크립트를 실행하면 아바타가 재구성됩니다

## 🛠️ 3D 소프트웨어에서 사용하기
아바타를 3D 소프트웨어로 가져오려면:
1. `avatar_composition.json`에서 각 아이템의 ID를 확인합니다
2. 각 아이템을 개별적으로 Roblox에서 추출해야 합니다
3. 서드파티 도구나 Roblox 개발자 도구를 사용할 수 있습니다

## 🎨 텍스처 정보
`textures/` 폴더에는 아바타 아이템들의 썸네일 이미지가 있습니다.
실제 3D 텍스처는 각 아이템을 개별적으로 추출해야 얻을 수 있습니다.

## ⚠️ 참고사항
- 로블록스에서 직접 OBJ 파일 다운로드는 더 이상 지원되지 않습니다
- 이 정보를 사용하여 Roblox Studio에서 아바타를 재구성할 수 있습니다
- 상업적 사용 시 로블록스 이용약관을 준수해야 합니다

## 📋 아바타 정보
- 유저: {user_info.get('displayName')} (@{user_info.get('name')})
- 아바타 타입: {avatar_data.get('playerAvatarType', 'R15')}
- 착용 아이템 수: {len(avatar_data.get('assets', []))}개
- 다운로드 시간: {time.strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        readme_file = user_folder / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📋 사용법 안내 파일 생성: {readme_file}")
    
    def download_3d_avatar(self, user_id: int, include_textures: bool = True) -> bool:
        """전체 3D 아바타 다운로드"""
        print(f"🎯 유저 ID {user_id}의 3D 아바타 다운로드 시작...")
        
        # 유저 정보 가져오기
        user_info = self.get_user_info(user_id)
        if not user_info:
            return False
        
        username = user_info.get("name", f"user_{user_id}")
        display_name = user_info.get("displayName", username)
        
        print(f"👤 {display_name} (@{username})")
        
        # 아바타 데이터 가져오기
        avatar_data = self.get_avatar_data(user_id)
        if not avatar_data:
            print("❌ 아바타 데이터를 가져올 수 없습니다.")
            return False
        
        # 유저별 폴더 생성
        user_folder = self.download_folder / f"{username}_{user_id}_3D"
        user_folder.mkdir(exist_ok=True)
        
        success = True
        
        # OBJ 모델 다운로드
        if not self.download_obj_model(user_id, user_folder):
            success = False
        
        # MTL 파일 다운로드 시도
        self.download_mtl_file(user_id, user_folder)
        
        # 텍스처 다운로드
        texture_count = 0
        if include_textures:
            texture_count = self.download_asset_textures(avatar_data, user_folder)
            print(f"🎨 텍스처 {texture_count}개 다운로드 완료")
        
        # 모델 정보 파일 생성
        self.create_model_info(user_id, user_info, avatar_data, user_folder)
        
        if success:
            print(f"✅ 아바타 정보 다운로드 완료: {user_folder}")
            print(f"📁 포함된 파일:")
            print(f"   📦 avatar_composition.json (아바타 구성 정보)")
            print(f"   📜 roblox_studio_script.lua (Studio 스크립트)")
            print(f"   🖼️ textures/ ({texture_count}개 텍스처)")
            print(f"   📄 model_info.json (상세 정보)")
            print(f"   📋 README.md (사용법 안내)")
            print(f"")
            print(f"💡 Roblox Studio에서 스크립트를 실행하여 아바타를 재구성할 수 있습니다!")
        
        return success
    
    def download_multiple_3d_avatars(self, user_ids: List[int], include_textures: bool = True):
        """여러 유저의 3D 아바타 다운로드"""
        print(f"🚀 총 {len(user_ids)}명의 3D 아바타 다운로드 시작...")
        
        for i, user_id in enumerate(user_ids, 1):
            print(f"\n[{i}/{len(user_ids)}] 처리 중...")
            self.download_3d_avatar(user_id, include_textures)
            
            # API 제한 방지
            if i < len(user_ids):
                time.sleep(2)
        
        print(f"\n🎉 모든 3D 아바타 다운로드 완료!")
        print(f"📁 저장 위치: {self.download_folder.absolute()}")


def main():
    """메인 함수"""
    print("=== 로블록스 3D 아바타 모델 다운로더 ===\n")
    
    downloader = Roblox3DDownloader("3d_avatars")
    
    print("다운로드 방식을 선택하세요:")
    print("1. 단일 유저 3D 아바타 (텍스처 포함)")
    print("2. 단일 유저 3D 아바타 (모델만)")
    print("3. 여러 유저 3D 아바타")
    print("4. 예시 실행 (유명 유저들)")
    
    try:
        choice = input("\n선택 (1-4): ").strip()
        
        if choice in ["1", "2"]:
            user_id = int(input("유저 ID 입력: "))
            include_textures = choice == "1"
            
            downloader.download_3d_avatar(user_id, include_textures)
        
        elif choice == "3":
            user_ids_input = input("유저 ID들 입력 (쉼표로 구분): ")
            user_ids = [int(uid.strip()) for uid in user_ids_input.split(",")]
            
            include_textures = input("텍스처도 포함하시겠습니까? (y/n) [기본값: y]: ").strip().lower() != 'n'
            
            downloader.download_multiple_3d_avatars(user_ids, include_textures)
        
        elif choice == "4":
            print("예시: 유명한 로블록스 유저들의 3D 아바타 다운로드")
            example_user_ids = [1, 156]  # Roblox, builderman
            
            downloader.download_multiple_3d_avatars(example_user_ids, include_textures=True)
        
        else:
            print("잘못된 선택입니다.")
    
    except ValueError:
        print("올바른 숫자를 입력해주세요.")
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main()
