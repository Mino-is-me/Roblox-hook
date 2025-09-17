#!/usr/bin/env python3
"""
완전 통합 다운로더 - 모든 Attachment 정보 통합
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roblox_avatar_downloader import RobloxAvatarDownloader
import json
from pathlib import Path
import time
import shutil

def create_integrated_avatar_package(username: str):
    """통합 아바타 패키지 생성"""
    print(f"\n🎯 '{username}' 완전한 아바타 패키지 생성 시작...")
    
    # 1. 기본 다운로더로 2D 썸네일 다운로드
    downloader = RobloxAvatarDownloader("final_integrated")
    
    print("👤 사용자 정보 조회...")
    user_id = downloader.get_user_id_by_username(username)
    if not user_id:
        print(f"❌ 사용자 '{username}' 정보 조회 실패")
        return False
    
    user_info = downloader.get_user_info(user_id)
    if not user_info:
        print(f"❌ 유저 ID {user_id} 정보 조회 실패")
        return False
    
    print(f"✅ 사용자 정보: {user_info.get('displayName')} (@{username}, ID: {user_id})")
    
    # 2. 2D 썸네일 다운로드
    print("\n📸 2D 썸네일 다운로드...")
    success_2d = downloader.download_user_avatars(user_id, include_3d=False)
    if success_2d:
        print("✅ 2D 썸네일 다운로드 완료")
    else:
        print("⚠️ 2D 썸네일 다운로드 실패 (계속 진행)")
    
    # 3. 3D 모델 복사 (기존에 다운로드된 것들)
    print("\n🎯 3D 모델 복사...")
    success_3d = copy_existing_3d_model(user_id, username)
    
    # 4. 확장 정보 수집
    print("\n📊 확장 아바타 정보 수집...")
    extended_info = collect_extended_info(downloader, user_id)
    
    # 5. Attachment 정보 분석
    print("\n🔍 Attachment 정보 분석...")
    attachment_info = analyze_existing_attachments(user_id, username)
    
    # 6. 통합 메타데이터 생성
    print("\n📋 통합 메타데이터 생성...")
    create_complete_metadata(user_id, username, user_info, extended_info, attachment_info, success_3d)
    
    print(f"\n🎉 '{username}' 완전한 아바타 패키지 생성 완료!")
    return True

def copy_existing_3d_model(user_id: int, username: str) -> bool:
    """기존 3D 모델 복사"""
    existing_folders = [
        f"test_extended_full/{username}_{user_id}_3D",
        f"test_improved_3d/{username}_{user_id}_3D",
        f"test_username_3d/{username}_{user_id}_3D"
    ]
    
    for folder_path in existing_folders:
        folder = Path(folder_path)
        if folder.exists():
            obj_file = folder / "avatar.obj"
            if obj_file.exists():
                print(f"   ✅ 기존 3D 모델 발견: {folder_path}")
                
                # 새 위치로 복사
                target_folder = Path(f"final_integrated/{username}_{user_id}/3D_Model")
                target_folder.mkdir(parents=True, exist_ok=True)
                
                # 파일들 복사
                for file in folder.iterdir():
                    if file.is_file():
                        shutil.copy2(file, target_folder / file.name)
                    elif file.is_dir() and file.name == "textures":
                        target_textures = target_folder / "textures"
                        target_textures.mkdir(exist_ok=True)
                        for texture in file.iterdir():
                            if texture.is_file():
                                shutil.copy2(texture, target_textures / texture.name)
                
                print(f"   ✅ 3D 모델 복사 완료: {target_folder}")
                return True
    
    print("   ⚠️ 기존 3D 모델을 찾을 수 없음")
    return False

def collect_extended_info(downloader: RobloxAvatarDownloader, user_id: int) -> dict:
    """확장 아바타 정보 수집"""
    extended_info = {
        "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "api_responses": {},
        "collection_status": {}
    }
    
    # 아바타 구성 정보
    try:
        response = downloader.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/avatar")
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
    
    # 착용 아이템 정보
    try:
        response = downloader.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing")
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

def analyze_existing_attachments(user_id: int, username: str) -> dict:
    """기존 Attachment 정보 분석"""
    attachment_info = {
        "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "obj_structure": None,
        "attachment_data": None
    }
    
    # 기존 OBJ 분석 데이터 찾기
    analysis_file = Path("obj_attachment_analysis.json")
    if analysis_file.exists():
        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis_data = json.load(f)
            
            for folder_data in analysis_data.get("avatar_folders", []):
                if f"{username}_{user_id}" in folder_data.get("folder_name", ""):
                    for obj_data in folder_data.get("obj_files", []):
                        attachment_info["obj_structure"] = obj_data
                        print("   ✅ OBJ 구조 분석 데이터 발견")
                        break
                    break
        except Exception as e:
            print(f"   ❌ OBJ 분석 데이터 읽기 오류: {e}")
    
    # 기존 Attachment 데이터 찾기
    attachment_file = Path(f"attachment_data/{username}_{user_id}_attachments.json")
    if attachment_file.exists():
        try:
            with open(attachment_file, 'r', encoding='utf-8') as f:
                attachment_info["attachment_data"] = json.load(f)
                print("   ✅ Attachment 데이터 발견")
        except Exception as e:
            print(f"   ❌ Attachment 데이터 읽기 오류: {e}")
    
    return attachment_info

def create_complete_metadata(user_id: int, username: str, user_info: dict, 
                           extended_info: dict, attachment_info: dict, has_3d: bool):
    """완전한 메타데이터 생성"""
    user_folder = Path(f"final_integrated/{username}_{user_id}")
    user_folder.mkdir(parents=True, exist_ok=True)
    
    complete_metadata = {
        "package_info": {
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "generator": "Complete Integrated Avatar Package v1.0",
            "user_id": user_id,
            "username": username,
            "display_name": user_info.get('displayName', username)
        },
        "content_status": {
            "2d_thumbnails": True,
            "3d_model": has_3d,
            "extended_avatar_info": bool(extended_info.get("api_responses")),
            "attachment_analysis": bool(attachment_info.get("obj_structure") or attachment_info.get("attachment_data"))
        },
        "user_profile": user_info,
        "extended_avatar_data": extended_info,
        "attachment_information": attachment_info
    }
    
    # 메타데이터 저장
    metadata_file = user_folder / "COMPLETE_AVATAR_PACKAGE.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(complete_metadata, f, indent=2, ensure_ascii=False)
    
    # README 생성
    readme_content = f"""# 🎯 완전한 아바타 패키지

## 📋 패키지 정보
- **사용자**: {user_info.get('displayName')} (@{username})
- **유저 ID**: {user_id}
- **생성일**: {complete_metadata['package_info']['created_at']}

## 📦 포함 컨텐츠
- **2D 썸네일**: ✅ 포함
- **3D 모델**: {'✅ 포함' if has_3d else '❌ 없음'}
- **확장 아바타 정보**: {'✅ 포함' if extended_info.get('api_responses') else '❌ 없음'}
- **Attachment 분석**: {'✅ 포함' if attachment_info.get('obj_structure') else '❌ 없음'}

## 🔍 Attachment 정보
"""
    
    if attachment_info.get("obj_structure"):
        obj_data = attachment_info["obj_structure"]
        readme_content += f"""
### 3D 모델 구조
- **버텍스**: {obj_data.get('vertices', 0):,}개
- **면**: {obj_data.get('faces', 0):,}개
- **그룹**: {len(obj_data.get('groups', []))}개

### 발견된 Attachment Points
"""
        groups = obj_data.get("groups", [])
        for group_data in groups:
            if isinstance(group_data, dict):
                group_name = group_data.get("name", "")
            else:
                group_name = str(group_data)
            
            if group_name.startswith("Player1"):
                readme_content += f"- `{group_name}`\\n"
    
    readme_content += f"""
## 📊 확장 아바타 정보
"""
    if extended_info.get("api_responses", {}).get("avatar_config"):
        config = extended_info["api_responses"]["avatar_config"]
        if "assets" in config:
            readme_content += f"- **착용 아이템**: {len(config['assets'])}개\\n"
    
    readme_content += f"""
---
*Complete Integrated Avatar Package로 생성*
*모든 Attachment 정보와 확장 데이터 통합*
"""
    
    readme_file = user_folder / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"   ✅ 통합 메타데이터 저장: {metadata_file}")
    print(f"   ✅ README 생성: {readme_file}")

def main():
    print("🎯 완전 통합 다운로더 - 모든 Attachment 정보 통합")
    print("="*60)
    
    # 테스트 사용자
    test_users = ["builderman"]
    
    for username in test_users:
        print(f"\\n{'='*60}")
        success = create_integrated_avatar_package(username)
        
        if success:
            print(f"🎉 {username} 완전한 패키지 생성 성공!")
        else:
            print(f"❌ {username} 패키지 생성 실패")
        
        print(f"{'='*60}")

if __name__ == "__main__":
    main()