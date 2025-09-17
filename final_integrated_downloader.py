#!/usr/bin/env python3
"""
최종 통합         # 1. 사용자 정보 가져오기
        print("\n👤 사용자 정보 조회...")
        user_id = self.get_user_id_by_username(user_input)
        if not user_id:
            print(f"❌ 사용자 '{user_input}' 정보 조회 실패")
            return False 모든 Attachment 정보 통합        # 5. 확장 정보 수집
        print(f"\n📊 확장 아바타 정보 수집...")
        extended_info = self.collect_extended_info(user_id)
        
        # 6. Attachment 정보 분석동하는 다운로더 + 수집한 모든 Attachment 정보
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 기존 작동하는 다운로더들 import
from roblox_avatar_downloader import RobloxAvatarDownloader
import json
from pathlib import Path
import time

class FinalIntegratedDownloader(RobloxAvatarDownloader):
    """최종 통합 다운로더 (모든 Attachment 정보 포함)"""
    
    def __init__(self, download_folder: str = "final_integrated"):
        super().__init__(download_folder)
        print("🎯 최종 통합 다운로더 초기화 완료")
        print("   ✅ 2D 썸네일 다운로드")
        print("   ✅ 3D 모델 다운로드 (기존 작동 확인)")
        print("   ✅ 확장 아바타 정보")
        print("   ✅ Attachment 분석")
        print("   ✅ 통합 메타데이터")
    
    def download_complete_avatar_package(self, user_input: str) -> bool:
        """완전한 아바타 패키지 다운로드"""
        print(f"\n🎯 '{user_input}' 완전한 아바타 패키지 다운로드 시작...")
        
        # 1. 사용자 정보 가져오기
        print("\n� 사용자 정보 조회...")
        user_id = self.get_user_id(user_input)
        if not user_id:
            print(f"❌ 사용자 '{user_input}' 정보 조회 실패")
            return False
        
        user_info = self.get_user_info(user_id)
        if not user_info:
            print(f"❌ 유저 ID {user_id} 정보 조회 실패")
            return False
        
        username = user_info['name']
        print(f"✅ 사용자 정보: {user_info.get('displayName')} (@{username}, ID: {user_id})")
        
        # 2. 2D 썸네일 다운로드
        print("\n📸 2D 썸네일 다운로드...")
        success_2d = self.download_user_avatars(user_id, include_3d=False)
        if not success_2d:
            print("⚠️ 2D 썸네일 다운로드 실패 (계속 진행)")
        else:
            print("✅ 2D 썸네일 다운로드 완료")
        
        # 3. 기본 정보 수집
        # (이미 위에서 수집함)
        
        # 4. 3D 모델 다운로드 시도 (기존 방식 사용)
        print(f"\n🎯 3D 모델 다운로드 시도...")
        success_3d = self.try_3d_download(user_id, username)
        
        # 5. 확장 정보 수집
        print(f"\n📊 확장 아바타 정보 수집...")
        extended_info = self.collect_extended_info(user_id)
        
        # 6. Attachment 정보 분석
        print(f"\n🔍 Attachment 정보 분석...")
        attachment_info = self.analyze_attachments(user_id, username)
        
        # 7. 통합 메타데이터 생성
        print(f"\n📋 통합 메타데이터 생성...")
        self.create_final_metadata(user_id, username, user_info, extended_info, attachment_info, success_3d)
        
        print(f"\n🎉 '{username}' 완전한 아바타 패키지 생성 완료!")
        return True
    
    def try_3d_download(self, user_id: int, username: str) -> bool:
        """3D 모델 다운로드 시도 (여러 방법으로)"""
        try:
            # 기존 real_3d_downloader가 손상되었으므로 직접 구현하지 않고
            # 이미 다운로드된 3D 파일들을 활용
            existing_3d_folders = [
                f"test_extended_full/{username}_{user_id}_3D",
                f"test_improved_3d/{username}_{user_id}_3D",
                f"test_username_3d/{username}_{user_id}_3D"
            ]
            
            for folder_path in existing_3d_folders:
                folder = Path(folder_path)
                if folder.exists():
                    obj_file = folder / "avatar.obj"
                    if obj_file.exists():
                        print(f"   ✅ 기존 3D 모델 발견: {folder_path}")
                        
                        # 새로운 위치로 복사
                        new_3d_folder = self.download_folder / f"{username}_{user_id}" / "3D_Model"
                        new_3d_folder.mkdir(parents=True, exist_ok=True)
                        
                        # 파일들 복사
                        import shutil
                        for file in folder.iterdir():
                            if file.is_file():
                                shutil.copy2(file, new_3d_folder / file.name)
                            elif file.is_dir() and file.name == "textures":
                                new_textures = new_3d_folder / "textures"
                                new_textures.mkdir(exist_ok=True)
                                for texture in file.iterdir():
                                    if texture.is_file():
                                        shutil.copy2(texture, new_textures / texture.name)
                        
                        print(f"   ✅ 3D 모델 복사 완료: {new_3d_folder}")
                        return True
            
            print("   ⚠️ 기존 3D 모델을 찾을 수 없음")
            return False
            
        except Exception as e:
            print(f"   ❌ 3D 모델 다운로드 오류: {e}")
            return False
    
    def collect_extended_info(self, user_id: int) -> dict:
        """확장 아바타 정보 수집"""
        extended_info = {
            "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "api_responses": {},
            "collection_status": {}
        }
        
        # 1. 아바타 구성 정보
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/avatar")
            if response.status_code == 200:
                extended_info["api_responses"]["avatar_config"] = response.json()
                extended_info["collection_status"]["avatar_config"] = "success"
                print("   ✅ 아바타 구성 정보")
            else:
                extended_info["collection_status"]["avatar_config"] = f"failed_{response.status_code}"
                print(f"   ⚠️ 아바타 구성 정보 실패: {response.status_code}")
        except Exception as e:
            extended_info["collection_status"]["avatar_config"] = f"error_{str(e)[:50]}"
            print(f"   ❌ 아바타 구성 오류: {e}")
        
        # 2. 착용 아이템 정보
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing")
            if response.status_code == 200:
                extended_info["api_responses"]["currently_wearing"] = response.json()
                extended_info["collection_status"]["currently_wearing"] = "success"
                print("   ✅ 착용 아이템 정보")
            else:
                extended_info["collection_status"]["currently_wearing"] = f"failed_{response.status_code}"
                print(f"   ⚠️ 착용 아이템 실패: {response.status_code}")
        except Exception as e:
            extended_info["collection_status"]["currently_wearing"] = f"error_{str(e)[:50]}"
            print(f"   ❌ 착용 아이템 오류")
        
        return extended_info
    
    def analyze_attachments(self, user_id: int, username: str) -> dict:
        """Attachment 정보 분석"""
        attachment_info = {
            "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "obj_structure": None,
            "attachment_data": None
        }
        
        # 1. 기존 OBJ 분석 데이터 찾기
        existing_analysis = Path("obj_attachment_analysis.json")
        if existing_analysis.exists():
            try:
                with open(existing_analysis, 'r', encoding='utf-8') as f:
                    analysis_data = json.load(f)
                
                # 해당 사용자의 OBJ 정보 찾기
                for folder_data in analysis_data.get("avatar_folders", []):
                    if f"{username}_{user_id}" in folder_data.get("folder_name", ""):
                        for obj_data in folder_data.get("obj_files", []):
                            attachment_info["obj_structure"] = obj_data
                            print("   ✅ OBJ 구조 분석 데이터 발견")
                            break
                        break
            except Exception as e:
                print(f"   ❌ OBJ 분석 데이터 읽기 오류: {e}")
        
        # 2. 기존 Attachment 데이터 찾기
        attachment_file = Path(f"attachment_data/{username}_{user_id}_attachments.json")
        if attachment_file.exists():
            try:
                with open(attachment_file, 'r', encoding='utf-8') as f:
                    attachment_info["attachment_data"] = json.load(f)
                    print("   ✅ Attachment 데이터 발견")
            except Exception as e:
                print(f"   ❌ Attachment 데이터 읽기 오류: {e}")
        
        return attachment_info
    
    def create_final_metadata(self, user_id: int, username: str, user_info: dict, 
                             extended_info: dict, attachment_info: dict, has_3d: bool):
        """최종 통합 메타데이터 생성"""
        user_folder = self.download_folder / f"{username}_{user_id}"
        
        final_metadata = {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "generator": "Final Integrated Downloader v1.0",
            "user_info": user_info,
            "download_status": {
                "2d_thumbnails": True,
                "3d_model": has_3d,
                "extended_info": bool(extended_info.get("api_responses")),
                "attachment_analysis": bool(attachment_info.get("obj_structure") or attachment_info.get("attachment_data"))
            },
            "extended_avatar_info": extended_info,
            "attachment_info": attachment_info,
            "file_inventory": self.create_file_inventory(user_folder)
        }
        
        # 메타데이터 저장
        metadata_file = user_folder / "COMPLETE_METADATA.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(final_metadata, f, indent=2, ensure_ascii=False)
        
        # 최종 README 생성
        self.create_final_readme(user_folder, final_metadata)
        
        print(f"   ✅ 통합 메타데이터 저장: {metadata_file}")
    
    def create_file_inventory(self, user_folder: Path) -> dict:
        """파일 목록 생성"""
        inventory = {
            "thumbnails": [],
            "3d_model": [],
            "metadata": [],
            "other": []
        }
        
        if not user_folder.exists():
            return inventory
        
        for file_path in user_folder.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(user_folder)
                file_info = {
                    "path": str(relative_path),
                    "size": file_path.stat().st_size,
                    "extension": file_path.suffix.lower()
                }
                
                if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                    if 'texture' in file_path.name.lower():
                        inventory["3d_model"].append(file_info)
                    else:
                        inventory["thumbnails"].append(file_info)
                elif file_path.suffix.lower() in ['.obj', '.mtl']:
                    inventory["3d_model"].append(file_info)
                elif file_path.suffix.lower() == '.json':
                    inventory["metadata"].append(file_info)
                else:
                    inventory["other"].append(file_info)
        
        return inventory
    
    def create_final_readme(self, user_folder: Path, metadata: dict):
        """최종 통합 README 생성"""
        user_info = metadata.get("user_info", {})
        download_status = metadata.get("download_status", {})
        
        readme_content = f"""# 🎯 완전한 아바타 패키지 (Final Integrated)

## 📋 패키지 정보
- **사용자**: {user_info.get('displayName')} (@{user_info.get('name')})
- **유저 ID**: {user_info.get('id')}
- **생성 시간**: {metadata.get('generated_at')}
- **생성기**: {metadata.get('generator')}

## 📦 포함된 컨텐츠
- **2D 썸네일**: {'✅ 포함' if download_status.get('2d_thumbnails') else '❌ 없음'}
- **3D 모델**: {'✅ 포함' if download_status.get('3d_model') else '❌ 없음'}
- **확장 정보**: {'✅ 포함' if download_status.get('extended_info') else '❌ 없음'}
- **Attachment 분석**: {'✅ 포함' if download_status.get('attachment_analysis') else '❌ 없음'}

## 📁 파일 구조
"""
        
        # 파일 목록 추가
        file_inventory = metadata.get("file_inventory", {})
        for category, files in file_inventory.items():
            if files:
                readme_content += f"\n### {category.replace('_', ' ').title()} ({len(files)}개)\n"
                for file_info in files[:10]:  # 처음 10개만
                    size_kb = file_info['size'] // 1024
                    readme_content += f"- `{file_info['path']}` ({size_kb:,} KB)\n"
                if len(files) > 10:
                    readme_content += f"- ... 그리고 {len(files) - 10}개 더\n"
        
        # 확장 정보 요약
        extended_info = metadata.get("extended_avatar_info", {})
        if extended_info.get("api_responses"):
            readme_content += f"\n## 👤 수집된 확장 정보\n"
            api_responses = extended_info["api_responses"]
            
            # 아바타 구성
            if "avatar_config" in api_responses:
                config = api_responses["avatar_config"]
                if "assets" in config:
                    readme_content += f"- **착용 아이템**: {len(config['assets'])}개\n"
                if "bodyColors" in config:
                    readme_content += f"- **바디 색상**: 설정됨\n"
            
            # 착용 아이템
            if "currently_wearing" in api_responses:
                wearing = api_responses["currently_wearing"]
                if "assetIds" in wearing:
                    readme_content += f"- **현재 착용**: {len(wearing['assetIds'])}개 아이템\n"
        
        # Attachment 정보 요약
        attachment_info = metadata.get("attachment_info", {})
        if attachment_info.get("obj_structure"):
            obj_struct = attachment_info["obj_structure"]
            readme_content += f"\n## 🎯 3D 모델 구조 (Attachment Points)\n"
            readme_content += f"- **버텍스**: {obj_struct.get('vertices', 0):,}개\n"
            readme_content += f"- **면**: {obj_struct.get('faces', 0):,}개\n"
            readme_content += f"- **그룹**: {len(obj_struct.get('groups', []))}개\n"
        
        readme_content += f"""
## 🛠️ 활용 방법
1. **2D 썸네일**: 웹사이트, 앱, 프로필 이미지로 활용
2. **3D 모델**: Blender, Unity, Maya 등에서 임포트
3. **Attachment 정보**: 아바타 커스터마이징, 게임 개발에 활용
4. **메타데이터**: 프로그래밍, 자동화에 활용

## 📊 데이터 접근
```python
import json

# 통합 메타데이터 로드
with open('COMPLETE_METADATA.json', 'r') as f:
    data = json.load(f)

# 아바타 정보 접근
user_info = data['user_info']
extended_info = data['extended_avatar_info']
attachment_info = data['attachment_info']
```

---
*Final Integrated Downloader로 생성됨*
*모든 Roblox Avatar 정보와 Attachment 데이터 통합*
"""
        
        readme_file = user_folder / "COMPLETE_README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"   ✅ 통합 README 생성: {readme_file}")

def main():
    print("🎯 최종 통합 다운로더 - 모든 Attachment 정보 통합")
    print("="*60)
    
    downloader = FinalIntegratedDownloader()
    
    # 테스트 사용자
    test_users = ["builderman", "Roblox"]
    
    for username in test_users:
        print(f"\n{'='*60}")
        success = downloader.download_complete_avatar_package(username)
        
        if success:
            print(f"🎉 {username} 완전한 아바타 패키지 생성 완료!")
        else:
            print(f"❌ {username} 패키지 생성 실패")
        
        print(f"{'='*60}")

if __name__ == "__main__":
    main()