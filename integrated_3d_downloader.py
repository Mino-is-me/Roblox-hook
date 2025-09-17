#!/usr/bin/env python3
"""
Roblox Avatar 3D Model Downloader (Latest API + Attachment Integration)
최신 로블록스 3D Avatar API와 Attachment 정보를 통합한 다운로더
"""

import os
import requests
import json
from typing import Optional, List, Dict, Tuple
from pathlib import Path
import time

class RobloxAvatar3DDownloaderIntegrated:
    """로블록스 3D 아바타 다운로더 (Attachment 정보 통합)"""
    
    def __init__(self, download_folder: str = "integrated_avatar_3d"):
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
    
    def calculate_cdn_url(self, hash_id: str) -> str:
        """
        해시 ID에서 올바른 CDN URL 계산
        최신 로블록스 CDN 해시 알고리즘 사용 (2024년 업데이트)
        """
        # 2024년 업데이트된 해시 계산 공식
        i = 31
        for t in range(min(38, len(hash_id))):
            if t < len(hash_id):
                i ^= ord(hash_id[t])
        
        cdn_number = i % 8
        return f"https://t{cdn_number}.rbxcdn.com/{hash_id}"
    
    def resolve_user_input(self, user_input: str) -> Optional[int]:
        """유저명 또는 ID를 처리하여 유저 ID 반환"""
        # 숫자인 경우 (유저 ID)
        if user_input.isdigit():
            user_id = int(user_input)
            print(f"🔍 유저 ID {user_id}로 인식")
            return user_id
        
        # 문자열인 경우 (유저명 -> ID 변환)
        return self.get_user_id_by_username(user_input)
    
    def get_user_id_by_username(self, username: str) -> Optional[int]:
        """유저명으로 유저 ID 찾기"""
        print(f"🔍 유저명 '{username}'으로 검색 중...")
        
        try:
            url = "https://users.roblox.com/v1/usernames/users"
            data = {
                "usernames": [username],
                "excludeBannedUsers": False
            }
            
            response = self.session.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                if "data" in result and len(result["data"]) > 0:
                    user_data = result["data"][0]
                    user_id = user_data["id"]
                    display_name = user_data.get("displayName", username)
                    print(f"✅ 유저명 '{username}' → ID: {user_id} (@{display_name})")
                    return user_id
                else:
                    print(f"❌ 유저명 '{username}'을 찾을 수 없습니다")
                    return None
            else:
                print(f"❌ 유저명 검색 실패: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 유저명 검색 오류: {e}")
            return None
    
    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """사용자 정보 조회"""
        try:
            response = self.session.get(f"https://users.roblox.com/v1/users/{user_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 사용자 정보 조회 실패: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 사용자 정보 조회 오류: {e}")
            return None
    
    def get_3d_avatar_metadata(self, user_id: int) -> Optional[Dict]:
        """3D 아바타 메타데이터 조회"""
        url = f"https://thumbnails.roblox.com/v1/users/avatar-3d?userIds={user_id}&format=Obj&size=768x432"
        print(f"🔍 3D 메타데이터 가져오는 중: {url}")
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    avatar_data = data["data"][0]
                    if "imageUrl" in avatar_data:
                        # 메타데이터 URL에서 실제 데이터 가져오기
                        meta_response = self.session.get(avatar_data["imageUrl"])
                        if meta_response.status_code == 200:
                            metadata = meta_response.json()
                            print("✅ 3D 메타데이터 획득 완료")
                            return metadata
                        else:
                            print(f"❌ 메타데이터 다운로드 실패: {meta_response.status_code}")
                            return None
            print(f"❌ 3D 메타데이터 조회 실패: {response.status_code}")
            return None
        except Exception as e:
            print(f"❌ 3D 메타데이터 조회 오류: {e}")
            return None
    
    def get_extended_avatar_info(self, user_id: int) -> dict:
        """확장된 아바타 정보 수집"""
        print(f"📊 확장 아바타 정보 수집 중...")
        
        extended_info = {
            "user_id": user_id,
            "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "api_responses": {}
        }
        
        # 1. 아바타 구성 정보
        try:
            print("   👤 아바타 구성 정보...")
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/avatar")
            if response.status_code == 200:
                extended_info["api_responses"]["avatar_config"] = response.json()
                print("   ✅ 아바타 구성 정보 수집 완료")
            else:
                print(f"   ⚠️ 아바타 구성 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 아바타 구성 오류: {e}")
        
        # 2. 착용 아이템 정보
        try:
            print("   🎽 착용 아이템 정보...")
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing")
            if response.status_code == 200:
                extended_info["api_responses"]["currently_wearing"] = response.json()
                print("   ✅ 착용 아이템 정보 수집 완료")
            elif response.status_code == 429:
                print("   ⚠️ 착용 아이템 정보 - API 제한 (429)")
            else:
                print(f"   ⚠️ 착용 아이템 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 착용 아이템 오류: {e}")
        
        # 3. 썸네일 정보
        try:
            print("   📸 썸네일 정보...")
            response = self.session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=720x720&format=Png&isCircular=false")
            if response.status_code == 200:
                extended_info["api_responses"]["thumbnails"] = response.json()
                print("   ✅ 썸네일 정보 수집 완료")
            else:
                print(f"   ⚠️ 썸네일 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 썸네일 오류: {e}")
        
        # 4. 게임 정보
        try:
            print("   🎮 게임 정보...")
            response = self.session.get(f"https://games.roblox.com/v2/users/{user_id}/games?accessFilter=Public&limit=10")
            if response.status_code == 200:
                games_data = response.json()
                if games_data.get("data"):
                    extended_info["api_responses"]["games"] = games_data
                    print(f"   ✅ 게임 정보 수집 완료 ({len(games_data['data'])}개)")
                else:
                    print("   📝 공개 게임 없음")
            else:
                print(f"   ⚠️ 게임 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 게임 정보 오류: {e}")
        
        # 5. 그룹 정보
        try:
            print("   👥 그룹 정보...")
            response = self.session.get(f"https://groups.roblox.com/v2/users/{user_id}/groups/roles")
            if response.status_code == 200:
                groups_data = response.json()
                if groups_data.get("data"):
                    extended_info["api_responses"]["groups"] = groups_data
                    print(f"   ✅ 그룹 정보 수집 완료 ({len(groups_data['data'])}개)")
                else:
                    print("   📝 소속 그룹 없음")
            else:
                print(f"   ⚠️ 그룹 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 그룹 정보 오류: {e}")
        
        return extended_info
    
    def analyze_obj_structure(self, obj_path: Path) -> dict:
        """OBJ 파일의 구조를 분석하여 attachment 정보 추출"""
        print(f"   🎯 OBJ 파일 구조 분석...")
        
        structure = {
            "file_path": str(obj_path),
            "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "groups": [],
            "objects": [],
            "materials": [],
            "vertices": 0,
            "faces": 0,
            "normals": 0,
            "texture_coords": 0,
            "body_parts": []
        }
        
        try:
            with open(obj_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    # 버텍스
                    if line.startswith('v '):
                        structure["vertices"] += 1
                    # 노말
                    elif line.startswith('vn '):
                        structure["normals"] += 1
                    # 텍스처 좌표
                    elif line.startswith('vt '):
                        structure["texture_coords"] += 1
                    # 면
                    elif line.startswith('f '):
                        structure["faces"] += 1
                    # 그룹 (아바타 파트)
                    elif line.startswith('g '):
                        group_name = line[2:].strip()
                        group_info = {
                            "name": group_name,
                            "line": line_num,
                            "type": self.classify_body_part(group_name)
                        }
                        structure["groups"].append(group_info)
                        
                        # 바디 파트 분류
                        if group_info["type"] != "unknown":
                            structure["body_parts"].append(group_info)
                    # 오브젝트
                    elif line.startswith('o '):
                        obj_name = line[2:].strip()
                        structure["objects"].append({
                            "name": obj_name,
                            "line": line_num
                        })
                    # 재질
                    elif line.startswith('usemtl '):
                        material = line[7:].strip()
                        if material not in structure["materials"]:
                            structure["materials"].append(material)
            
            print(f"   ✅ OBJ 구조 분석 완료:")
            print(f"      - 버텍스: {structure['vertices']:,}개")
            print(f"      - 면: {structure['faces']:,}개")
            print(f"      - 그룹: {len(structure['groups'])}개")
            print(f"      - 바디 파트: {len(structure['body_parts'])}개")
            print(f"      - 재질: {len(structure['materials'])}개")
            
        except Exception as e:
            print(f"   ❌ OBJ 분석 오류: {e}")
            structure["error"] = str(e)
        
        return structure
    
    def classify_body_part(self, group_name: str) -> str:
        """그룹 이름으로 바디 파트 분류"""
        name_lower = group_name.lower()
        
        part_mappings = {
            "head": ["player1", "head"],
            "torso": ["player2", "torso", "chest"],
            "left_arm": ["player3", "leftarm", "left_arm"],
            "right_arm": ["player4", "rightarm", "right_arm"],
            "left_leg": ["player5", "leftleg", "left_leg"],
            "right_leg": ["player6", "rightleg", "right_leg"],
            "hat": ["player7", "hat", "cap", "helmet"],
            "hair": ["player8", "hair"],
            "face": ["player9", "face"],
            "shirt": ["player10", "shirt", "top"],
            "pants": ["player11", "pants", "bottom"],
            "shoes": ["player12", "shoes", "boot"],
            "accessory": ["player13", "player14", "player15", "accessory", "gear"],
            "handle": ["handle", "grip", "tool"]
        }
        
        for part_type, keywords in part_mappings.items():
            if any(keyword in name_lower for keyword in keywords):
                return part_type
        
        return "unknown"
    
    def download_file_from_hash(self, hash_id: str, file_path: Path, file_type: str = "파일") -> bool:
        """해시 ID로부터 파일 다운로드 (향상된 재시도 로직)"""
        # 브라우저 요청처럼 보이도록 헤더 추가
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.roblox.com/',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        # 여러 CDN 서버 시도
        cdn_urls_to_try = []
        
        # 1. 기본 계산된 CDN URL
        try:
            primary_cdn_url = self.calculate_cdn_url(hash_id)
            cdn_urls_to_try.append(primary_cdn_url)
        except Exception as e:
            print(f"⚠️ 기본 CDN URL 계산 실패: {e}")
        
        # 2. 모든 CDN 서버 번호 시도 (t0~t7)
        for cdn_num in range(8):
            alt_url = f"https://t{cdn_num}.rbxcdn.com/{hash_id}"
            if alt_url not in cdn_urls_to_try:
                cdn_urls_to_try.append(alt_url)
        
        print(f"📥 {file_type} 다운로드 중...")
        
        # 각 URL 시도
        for i, url in enumerate(cdn_urls_to_try):
            try:
                if i == 0:
                    print(f"   🎯 기본 서버: {url}")
                else:
                    print(f"   🔄 대체 서버 #{i}: {url}")
                
                response = self.session.get(url, headers=headers, stream=True, timeout=30)
                
                if response.status_code == 200:
                    # 파일 크기 확인
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) == 0:
                        print(f"   ⚠️ 빈 파일 응답, 다음 서버 시도...")
                        continue
                    
                    # 파일 저장
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    # 파일 크기 검증
                    if file_path.exists() and file_path.stat().st_size > 0:
                        print(f"   ✅ {file_type} 다운로드 완료: {file_path}")
                        return True
                    else:
                        print(f"   ⚠️ 다운로드된 파일이 비어있음, 다음 서버 시도...")
                        if file_path.exists():
                            file_path.unlink()
                        continue
                else:
                    print(f"   ❌ HTTP {response.status_code}: {response.reason}")
                    
            except requests.exceptions.Timeout:
                print(f"   ⏰ 타임아웃, 다음 서버 시도...")
                continue
            except requests.exceptions.ConnectionError:
                print(f"   🔌 연결 오류, 다음 서버 시도...")
                continue
            except Exception as e:
                print(f"   ❌ 예상치 못한 오류: {e}")
                continue
                
            # 서버 간 딜레이
            if i < len(cdn_urls_to_try) - 1:
                time.sleep(0.5)
        
        print(f"   💔 모든 CDN 서버에서 {file_type} 다운로드 실패")
        return False
    
    def download_avatar_3d_complete(self, user_id: int, include_textures: bool = True) -> bool:
        """완전한 3D 아바타 다운로드 (Attachment 정보 통합)"""
        print(f"🎯 유저 ID {user_id}의 완전한 3D 아바타 다운로드 시작...")
        
        # 사용자 정보 조회
        user_info = self.get_user_info(user_id)
        if not user_info:
            print("❌ 사용자 정보를 찾을 수 없습니다")
            return False
        
        username = user_info.get("name", "Unknown")
        display_name = user_info.get("displayName", username)
        print(f"👤 {display_name} (@{username})")
        
        # 3D 메타데이터 조회
        metadata = self.get_3d_avatar_metadata(user_id)
        if not metadata:
            print("❌ 3D 아바타 메타데이터를 가져올 수 없습니다")
            return False
        
        # 폴더 생성
        user_folder = self.download_folder / f"{username}_{user_id}_3D"
        user_folder.mkdir(exist_ok=True)
        
        textures_folder = user_folder / "textures"
        textures_folder.mkdir(exist_ok=True)
        
        # 다운로드 카운터
        total_files = 0
        success_count = 0
        
        # OBJ 파일 다운로드
        obj_hash = metadata.get("obj")
        if obj_hash:
            obj_file = user_folder / "avatar.obj"
            total_files += 1
            if self.download_file_from_hash(obj_hash, obj_file, "OBJ 모델"):
                success_count += 1
        
        # MTL 파일 다운로드
        mtl_hash = metadata.get("mtl")
        if mtl_hash:
            mtl_file = user_folder / "avatar.mtl"
            total_files += 1
            if self.download_file_from_hash(mtl_hash, mtl_file, "MTL 재질"):
                success_count += 1
        
        # 텍스처 파일들 다운로드
        if include_textures:
            textures = metadata.get("textures", [])
            if textures:
                print(f"🎨 {len(textures)}개의 텍스처 다운로드 중...")
                
                texture_success = 0
                for i, texture_hash in enumerate(textures):
                    texture_file = textures_folder / f"texture_{i+1:03d}.png"
                    total_files += 1
                    
                    print(f"   🖼️ 텍스처 {i+1}/{len(textures)} 처리 중...")
                    if self.download_file_from_hash(texture_hash, texture_file, f"텍스처 {i+1}"):
                        success_count += 1
                        texture_success += 1
                    
                    # API 제한 방지를 위한 딜레이
                    if i < len(textures) - 1:
                        time.sleep(0.3)
                
                print(f"   🎨 텍스처 다운로드 결과: {texture_success}/{len(textures)} 성공")
            else:
                print("🎨 텍스처 정보 없음")
        
        # 확장 아바타 정보 수집
        extended_info = self.get_extended_avatar_info(user_id)
        
        # OBJ 파일 구조 분석 (Attachment 정보 포함)
        if obj_hash and (user_folder / "avatar.obj").exists():
            obj_structure = self.analyze_obj_structure(user_folder / "avatar.obj")
            extended_info["obj_structure"] = obj_structure
        
        # 메타데이터 저장 (확장 정보 포함)
        self.save_integrated_metadata(user_info, metadata, user_folder, extended_info)
        
        # 핵심 파일 다운로드 여부 확인
        core_files_success = 0
        if obj_hash and (user_folder / "avatar.obj").exists():
            core_files_success += 1
        if mtl_hash and (user_folder / "avatar.mtl").exists():
            core_files_success += 1
        
        # 결과 출력
        print(f"\n🎉 다운로드 완료: {success_count}/{total_files} 파일 성공")
        
        # 최소한 OBJ 또는 MTL 중 하나는 성공해야 함
        download_success = core_files_success > 0
        
        if download_success:
            print(f"📁 저장 위치: {user_folder}")
            print(f"📦 포함된 파일:")
            if obj_hash and (user_folder / "avatar.obj").exists():
                obj_size = (user_folder / "avatar.obj").stat().st_size
                print(f"   📄 avatar.obj (3D 모델, {obj_size:,} bytes)")
            if mtl_hash and (user_folder / "avatar.mtl").exists():
                print(f"   🎨 avatar.mtl (재질 정보)")
            if include_textures and textures:
                texture_count = len([f for f in textures_folder.glob("texture_*.png")])
                print(f"   🖼️ textures/ ({texture_count}/{len(textures)}개 텍스처)")
            print(f"   📋 metadata.json (통합 메타데이터)")
            print(f"   📖 README.md (상세 사용법)")
            
            if success_count < total_files:
                missing_count = total_files - success_count
                print(f"   ⚠️ {missing_count}개 파일 다운로드 실패 (하지만 핵심 파일은 다운로드됨)")
        else:
            print(f"   ❌ 핵심 3D 파일 다운로드 실패")
        
        return download_success
    
    def save_integrated_metadata(self, user_info: Dict, metadata: Dict, user_folder: Path, extended_info: Optional[Dict] = None):
        """통합 메타데이터와 상세 README 저장"""
        # 통합 메타데이터 저장
        full_metadata = {
            "user_info": user_info,
            "avatar_3d_metadata": metadata,
            "download_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "api_info": {
                "source": "Roblox Avatar 3D API + Attachment Integration",
                "endpoint": "https://thumbnails.roblox.com/v1/users/avatar-3d",
                "cdn_calculation": "Updated 2024 hash algorithm",
                "attachment_apis": [
                    "https://avatar.roblox.com/v1/users/{id}/avatar",
                    "https://avatar.roblox.com/v1/users/{id}/currently-wearing",
                    "https://thumbnails.roblox.com/v1/users/avatar",
                    "https://games.roblox.com/v2/users/{id}/games",
                    "https://groups.roblox.com/v2/users/{id}/groups/roles"
                ]
            }
        }
        
        # 확장 정보가 있으면 추가
        if extended_info:
            full_metadata["extended_avatar_info"] = extended_info
        
        metadata_file = user_folder / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(full_metadata, f, indent=2, ensure_ascii=False)
        
        # 통합 README 생성
        self.create_integrated_readme(user_info, metadata, user_folder, extended_info)
        
        print(f"📋 통합 메타데이터 저장: {metadata_file}")
    
    def create_integrated_readme(self, user_info: Dict, metadata: Dict, user_folder: Path, extended_info: Optional[Dict] = None):
        """통합된 상세 README 생성"""
        camera_info = metadata.get("camera", {})
        aabb_info = metadata.get("aabb", {})
        
        readme_content = f"""# 🎯 통합 3D 아바타 모델 (Attachment 정보 포함)

## 📁 다운로드된 파일들
- `avatar.obj`: 3D 메시 파일 (Wavefront OBJ 형식)
- `avatar.mtl`: 재질 정보 파일
- `textures/`: 텍스처 이미지들
- `metadata.json`: **통합 메타데이터** (확장 정보 + Attachment 정보 포함)
- `README.md`: 이 상세 사용법 파일

## 🎮 유저 정보
- **이름**: {user_info.get('displayName')} (@{user_info.get('name')})
- **유저 ID**: {user_info.get('id')}
- **가입일**: {user_info.get('created', 'N/A')}
- **인증 배지**: {'✅' if user_info.get('hasVerifiedBadge') else '❌'}
- **다운로드 시간**: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""

        # 확장 아바타 정보 추가
        if extended_info and "api_responses" in extended_info:
            readme_content += "\n## 👤 아바타 상세 정보\n"
            
            # 아바타 구성 정보
            avatar_config = extended_info["api_responses"].get("avatar_config", {})
            if avatar_config:
                readme_content += f"- **아바타 타입**: {avatar_config.get('playerAvatarType', 'N/A')}\n"
                
                # 바디 색상
                if "bodyColors" in avatar_config:
                    colors = avatar_config["bodyColors"]
                    readme_content += "- **바디 색상**:\n"
                    color_names = {
                        'headColorId': '머리',
                        'torsoColorId': '몸통',
                        'rightArmColorId': '오른팔',
                        'leftArmColorId': '왼팔',
                        'rightLegColorId': '오른다리',
                        'leftLegColorId': '왼다리'
                    }
                    for part, color_id in colors.items():
                        part_name = color_names.get(part, part)
                        readme_content += f"  - {part_name}: 색상 ID {color_id}\n"
                
                # 착용 아이템
                if "assets" in avatar_config:
                    items = avatar_config["assets"]
                    readme_content += f"- **착용 아이템** ({len(items)}개):\n"
                    for item in items[:10]:  # 처음 10개만
                        item_name = item.get('name', 'Unknown')
                        item_type = item.get('assetType', {}).get('name', 'Unknown')
                        item_id = item.get('id', 'N/A')
                        readme_content += f"  - {item_name} ({item_type}, ID: {item_id})\n"
                    if len(items) > 10:
                        readme_content += f"  - ... 그리고 {len(items) - 10}개 더\n"
            
            # 게임 정보
            games = extended_info["api_responses"].get("games", {})
            if games and "data" in games:
                game_count = len(games["data"])
                readme_content += f"\n## 🎮 제작한 게임 ({game_count}개)\n"
                for game in games["data"][:5]:  # 처음 5개만
                    name = game.get("name", "Untitled")
                    plays = game.get("placeVisits", 0)
                    readme_content += f"- **{name}**: {plays:,} 플레이\n"
            
            # 그룹 정보
            groups = extended_info["api_responses"].get("groups", {})
            if groups and "data" in groups:
                group_count = len(groups["data"])
                readme_content += f"\n## 👥 소속 그룹 ({group_count}개)\n"
                for group_data in groups["data"][:5]:  # 처음 5개만
                    group = group_data.get("group", {})
                    role = group_data.get("role", {})
                    group_name = group.get("name", "Unknown Group")
                    role_name = role.get("name", "Member")
                    readme_content += f"- **{group_name}**: {role_name}\n"

        # OBJ 구조 정보 추가 (Attachment 핵심 정보)
        if extended_info and "obj_structure" in extended_info:
            obj_struct = extended_info["obj_structure"]
            readme_content += f"\n## 🎯 3D 모델 구조 정보 (Attachment Points)\n"
            readme_content += f"- **버텍스**: {obj_struct.get('vertices', 0):,}개\n"
            readme_content += f"- **면**: {obj_struct.get('faces', 0):,}개\n"
            readme_content += f"- **그룹**: {len(obj_struct.get('groups', []))}개\n"
            readme_content += f"- **재질**: {len(obj_struct.get('materials', []))}개\n"
            
            # 바디 파트 정보 (Attachment 포인트)
            body_parts = obj_struct.get('body_parts', [])
            if body_parts:
                readme_content += f"\n### 🚶 아바타 바디 파트 (Attachment Points)\n"
                part_types = {}
                for part in body_parts:
                    part_type = part.get('type', 'unknown')
                    if part_type not in part_types:
                        part_types[part_type] = []
                    part_types[part_type].append(part.get('name', 'Unknown'))
                
                for part_type, names in part_types.items():
                    part_names = ', '.join(names)
                    readme_content += f"- **{part_type.replace('_', ' ').title()}**: {part_names}\n"
                
                readme_content += f"\n#### 🎯 Attachment Point 매핑\n"
                readme_content += f"```\n"
                readme_content += f"Player1  → Head (머리)\n"
                readme_content += f"Player2  → Torso (몸통)\n" 
                readme_content += f"Player3  → Left Arm (왼팔)\n"
                readme_content += f"Player4  → Right Arm (오른팔)\n"
                readme_content += f"Player5  → Left Leg (왼다리)\n"
                readme_content += f"Player6  → Right Leg (오른다리)\n"
                readme_content += f"Player7+ → Accessories (액세서리들)\n"
                readme_content += f"Handle   → Tools/Gear (도구)\n"
                readme_content += f"```\n"
            
            # 사용된 재질들
            materials = obj_struct.get('materials', [])
            if materials:
                readme_content += f"\n### 🎨 사용된 재질들\n"
                for material in materials:
                    readme_content += f"- {material}\n"

        readme_content += f"""
## 📐 3D 모델 정보
- **카메라 위치**: {camera_info.get('position', 'N/A')}
- **카메라 FOV**: {camera_info.get('fov', 'N/A')}
- **바운딩 박스**: {aabb_info.get('min', 'N/A')} ~ {aabb_info.get('max', 'N/A')}

## 🛠️ 사용 방법

### Blender에서 사용하기 (Attachment 활용)
1. Blender를 실행합니다
2. File > Import > Wavefront (.obj) 선택
3. `avatar.obj` 파일을 선택하여 임포트
4. **각 그룹(Player1-15)이 개별 오브젝트로 분리됩니다**
5. **그룹 이름으로 바디 파트 식별 가능**
6. **Attachment Point로 활용 가능**

### Unity에서 사용하기 (Attachment 활용)
1. Unity 프로젝트의 Assets 폴더에 모든 파일을 복사
2. `avatar.obj` 파일을 씬에 드래그
3. **Asset ID를 통해 원본 Roblox 아이템 추적 가능**
4. **bodyColors로 아바타 색상 재현 가능**
5. **그룹별로 Attachment Point 설정 가능**

### 프로그래밍에서 Attachment 정보 활용
```python
import json

# 메타데이터 로드
with open('metadata.json', 'r') as f:
    metadata = json.load(f)

# 확장 아바타 정보 접근
ext_info = metadata['extended_avatar_info']
avatar_config = ext_info['api_responses']['avatar_config']

# 착용 중인 모자 찾기
for asset in avatar_config['assets']:
    if asset['assetType']['name'] == 'Hat':
        print(f"모자: {{asset['name']}} (ID: {{asset['id']}})")

# OBJ 구조 정보 접근
obj_structure = ext_info['obj_structure']
for part in obj_structure['body_parts']:
    print(f"{{part['name']}} → {{part['type']}}")
```

### Three.js/Web에서 사용하기
```javascript
import {{OBJLoader}} from 'three/examples/jsm/loaders/OBJLoader.js';
import {{MTLLoader}} from 'three/examples/jsm/loaders/MTLLoader.js';

const mtlLoader = new MTLLoader();
mtlLoader.load('avatar.mtl', (materials) => {{
    materials.preload();
    
    const objLoader = new OBJLoader();
    objLoader.setMaterials(materials);
    objLoader.load('avatar.obj', (object) => {{
        // 각 그룹(attachment point)별로 접근 가능
        object.children.forEach(child => {{
            console.log('Attachment Point:', child.name);
        }});
        scene.add(object);
    }});
}});
```

## 🎯 Attachment 정보 활용 팁
1. **Asset ID로 원본 아이템 추적**: metadata.json의 avatar_config.assets 참조
2. **바디 색상 적용**: bodyColors의 색상 ID로 부위별 색상 설정
3. **그룹별 Attachment**: Player1-15 그룹을 attachment point로 활용
4. **재질별 텍스처 매핑**: MTL 파일의 재질 정보로 텍스처 적용

## ⚠️ 주의사항
- 이 모델은 로블록스의 R15 또는 R6 형식입니다
- 상업적 사용 시 로블록스 이용약관을 준수해야 합니다
- Asset ID와 attachment 정보는 원본 Roblox 아이템과 연결됩니다

---
*통합 다운로더로 생성됨 - Attachment 정보 포함*
*생성 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # 파일 저장
        readme_path = user_folder / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📖 통합 README 생성: {readme_path}")

def main():
    print("=== 통합 3D 아바타 다운로더 (Attachment 정보 포함) ===\n")
    
    downloader = RobloxAvatar3DDownloaderIntegrated()
    
    while True:
        print("\n" + "="*50)
        user_input = input("🎯 다운로드할 유저명 또는 ID 입력 (종료: 'exit'): ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("👋 다운로더를 종료합니다!")
            break
        
        if not user_input:
            print("❌ 유저명 또는 ID를 입력해주세요")
            continue
        
        # 유저 입력 처리
        user_id = downloader.resolve_user_input(user_input)
        
        if user_id:
            # 3D 다운로드 (확장 정보 + Attachment 정보 포함)
            success = downloader.download_avatar_3d_complete(user_id, include_textures=True)
            
            if success:
                print(f"\n✅ '{user_input}' 통합 다운로드 성공!")
                print("📁 생성된 파일들:")
                print("   - avatar.obj, avatar.mtl (3D 파일)")
                print("   - textures/ (텍스처들)")
                print("   - metadata.json (통합 메타데이터 + Attachment 정보)")
                print("   - README.md (상세한 사용법과 Attachment 가이드)")
            else:
                print(f"❌ '{user_input}' 다운로드 실패")
        else:
            print(f"❌ '{user_input}' 유저를 찾을 수 없습니다")

if __name__ == "__main__":
    main()