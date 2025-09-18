#!/usr/bin/env python3
"""
Roblox Avatar 3D Model Downloader (Latest API)
최신 로블록스 3D Avatar API를 사용한 실제 3D 모델 다운로더
"""

import os
import requests
import json
from typing import Optional, List, Dict, Tuple
from pathlib import Path
import time
from body_part_mapping_parser import BodyPartMapper

class RobloxAvatar3DDownloader:
    """로블록스 3D 아바타 다운로더 (최신 API 사용)"""
    
    def __init__(self, download_folder: str = "avatar_3d_models"):
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
        
        Args:
            hash_id (str): 파일 해시 ID
            
        Returns:
            str: 완전한 CDN URL
        """
        # 포럼에서 업데이트된 JavaScript 공식을 Python으로 변환
        # function get(hash) {
        #  for (var i = 31, t = 0; t < 38; t++)
        #    i ^= hash[t].charCodeAt(0);
        #  return `https://t${(i % 8).toString()}.rbxcdn.com/${hash}`;
        # }
        
        i = 31
        for t in range(min(38, len(hash_id))):  # 최대 38자까지만 처리
            i ^= ord(hash_id[t])
        
        cdn_number = i % 8
        return f"https://t{cdn_number}.rbxcdn.com/{hash_id}"
    
    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """유저 정보 가져오기"""
        try:
            url = f"https://users.roblox.com/v1/users/{user_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ 유저 정보 가져오기 실패 (ID: {user_id}): {e}")
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
    
    def get_avatar_3d_metadata(self, user_id: int) -> Optional[Dict]:
        """
        3D 아바타 메타데이터 가져오기
        
        Args:
            user_id (int): 로블록스 유저 ID
            
        Returns:
            Dict: 3D 아바타 메타데이터 또는 None
        """
        try:
            # 첫 번째 API 호출: 3D 아바타 요청
            url = f"https://thumbnails.roblox.com/v1/users/avatar-3d"
            params = {"userId": user_id}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # state가 Completed인지 확인
            if data.get("state") != "Completed":
                print(f"⚠️ 아바타가 아직 처리 중입니다. 상태: {data.get('state')}")
                return None
            
            image_url = data.get("imageUrl")
            if not image_url:
                print(f"❌ 이미지 URL을 찾을 수 없습니다.")
                return None
            
            # 두 번째 API 호출: 실제 3D 데이터 가져오기
            print(f"🔍 3D 메타데이터 가져오는 중: {image_url}")
            metadata_response = self.session.get(image_url)
            metadata_response.raise_for_status()
            
            metadata = metadata_response.json()
            print(f"✅ 3D 메타데이터 획득 완료")
            return metadata
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 3D 메타데이터 가져오기 실패: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON 파싱 실패: {e}")
            return None
    
    def download_file_from_hash(self, hash_id: str, file_path: Path, file_type: str = "파일") -> bool:
        """
        해시 ID로부터 파일 다운로드 (향상된 재시도 로직)
        
        Args:
            hash_id (str): 파일 해시 ID
            file_path (Path): 저장할 파일 경로
            file_type (str): 파일 타입 (로깅용)
            
        Returns:
            bool: 성공 여부
        """
        # 브라우저 요청처럼 보이도록 헤더 추가
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.roblox.com/',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'DNT': '1',
            'Sec-GPC': '1'
        }
        
        # 여러 CDN 서버 시도 (기본 계산된 URL부터 시작)
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
        
        # 3. 추가 CDN 패턴들
        additional_patterns = [
            f"https://tr.rbxcdn.com/{hash_id}",
            f"https://c0.rbxcdn.com/{hash_id}",
            f"https://c1.rbxcdn.com/{hash_id}"
        ]
        for pattern in additional_patterns:
            if pattern not in cdn_urls_to_try:
                cdn_urls_to_try.append(pattern)
        
        print(f"� {file_type} 다운로드 중...")
        
        # 각 URL 시도
        for i, url in enumerate(cdn_urls_to_try):
            try:
                if i == 0:
                    print(f"   🎯 기본 서버: {url}")
                else:
                    print(f"   🔄 대체 서버 #{i}: {url}")
                
                # 타임아웃과 재시도 추가
                response = self.session.get(
                    url, 
                    headers=headers, 
                    stream=True, 
                    timeout=30,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    # 파일 크기 확인
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) == 0:
                        print(f"   ⚠️ 빈 파일 응답, 다음 서버 시도...")
                        continue
                    
                    # 파일 저장
                    with open(file_path, 'wb') as f:
                        downloaded = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                    
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
            except requests.exceptions.RequestException as e:
                print(f"   ❌ 요청 오류: {e}")
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
        """
        완전한 3D 아바타 다운로드 (OBJ + MTL + 텍스처)
        
        Args:
            user_id (int): 로블록스 유저 ID
            include_textures (bool): 텍스처 포함 여부
            
        Returns:
            bool: 성공 여부
        """
        print(f"🎯 유저 ID {user_id}의 완전한 3D 아바타 다운로드 시작...")
        
        # 유저 정보 가져오기
        user_info = self.get_user_info(user_id)
        if not user_info:
            return False
        
        username = user_info.get("name", f"user_{user_id}")
        display_name = user_info.get("displayName", username)
        print(f"👤 {display_name} (@{username})")
        
        # 3D 메타데이터 가져오기
        metadata = self.get_avatar_3d_metadata(user_id)
        if not metadata:
            return False
        
        # 유저별 폴더 생성
        user_folder = self.download_folder / f"{username}_{user_id}_3D"
        user_folder.mkdir(exist_ok=True)
        
        # 텍스처 폴더 생성
        if include_textures:
            textures_folder = user_folder / "textures"
            textures_folder.mkdir(exist_ok=True)
        
        success_count = 0
        total_files = 0
        
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
            
            # 바디 파트 매핑 생성
            self.generate_body_part_mapping(user_info, obj_structure, user_folder)
        
        # 메타데이터 저장 (확장 정보 포함)
        self.save_metadata(user_info, metadata, user_folder, extended_info)
        
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
            print(f"   📋 metadata.json (상세 정보)")
            print(f"   📖 README.md (사용법)")
            
            if success_count < total_files:
                missing_count = total_files - success_count
                print(f"   ⚠️ {missing_count}개 파일 다운로드 실패 (하지만 핵심 파일은 다운로드됨)")
        else:
            print(f"   ❌ 핵심 3D 파일 다운로드 실패")
        
        return download_success
    
    def get_extended_avatar_info(self, user_id: int) -> dict:
        """
        사용자 아바타의 확장 정보 수집
        
        Args:
            user_id (int): 사용자 ID
            
        Returns:
            dict: 확장된 아바타 정보
        """
        print(f"📊 확장 아바타 정보 수집 중...")
        
        extended_info = {
            "user_id": user_id,
            "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "api_responses": {}
        }
        
        # 1. 아바타 구성 정보 (가장 중요)
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
            
        # 2. 현재 착용 중인 아바타 아이템들
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
            
        # 3. 다양한 썸네일 정보
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
            
        # 4. 게임 정보 (공개 게임만)
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
        """
        OBJ 파일의 구조를 분석하여 attachment 정보 추출
        
        Args:
            obj_path (Path): OBJ 파일 경로
            
        Returns:
            dict: OBJ 구조 분석 결과
        """
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
        
        # 로블록스 아바타 파트 매핑
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

    def generate_body_part_mapping(self, user_info: Dict, obj_structure: Dict, user_folder: Path) -> bool:
        """바디 파트 매핑 텍스트 파일 생성"""
        try:
            print("   📋 바디 파트 매핑 텍스트 생성...")
            
            # BodyPartMapper 초기화
            mapper = BodyPartMapper()
            
            # 아바타 데이터 준비 (BodyPartMapper가 기대하는 형식으로)
            avatar_data = {
                'user_id': user_info.get('id'),
                'username': user_info.get('name'),
                'display_name': user_info.get('displayName'),
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'obj_path': obj_structure.get('file_path'),
                'vertices': obj_structure.get('vertices', 0),
                'faces': obj_structure.get('faces', 0),
                'groups': obj_structure.get('groups', [])
            }
            
            # 바디 파트 매핑 텍스트 파일 생성
            output_path = user_folder / "BODY_PART_MAPPING.txt"
            success = mapper.create_body_part_mapping_text(avatar_data, output_path)
            
            if success:
                print(f"   ✅ 바디 파트 매핑 파일 생성: {output_path.name}")
                return True
            else:
                print("   ❌ 바디 파트 매핑 파일 생성 실패")
                return False
                
        except Exception as e:
            print(f"   ❌ 바디 파트 매핑 생성 오류: {e}")
            return False

    def save_metadata(self, user_info: Dict, metadata: Dict, user_folder: Path, extended_info: Optional[Dict] = None):
        """메타데이터와 사용법 저장"""
        # 메타데이터 저장
        full_metadata = {
            "user_info": user_info,
            "avatar_3d_metadata": metadata,
            "download_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "api_info": {
                "source": "Roblox Avatar 3D API",
                "endpoint": "https://thumbnails.roblox.com/v1/users/avatar-3d",
                "cdn_calculation": "Updated 2024 hash algorithm"
            }
        }
        
        # 확장 정보가 있으면 추가
        if extended_info:
            full_metadata["extended_avatar_info"] = extended_info
        
        metadata_file = user_folder / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(full_metadata, f, indent=2, ensure_ascii=False)
        
        # 확장 사용법 안내 생성 (확장 정보 포함)
        self.create_extended_readme(user_info, metadata, user_folder, extended_info)
    
    def create_extended_readme(self, user_info: Dict, metadata: Dict, user_folder: Path, extended_info: Optional[Dict] = None):
        """확장된 사용법 README 생성"""
        camera_info = metadata.get("camera", {})
        aabb_info = metadata.get("aabb", {})
        
        readme_content = f"""# 3D 아바타 모델 사용법

## 📁 다운로드된 파일들
- `avatar.obj`: 3D 메시 파일 (Wavefront OBJ 형식)
- `avatar.mtl`: 재질 정보 파일
- `textures/`: 텍스처 이미지들
- `metadata.json`: 전체 메타데이터 (확장 정보 포함)
- `README.md`: 이 사용법 파일

## 🎮 유저 정보
- **이름**: {user_info.get('displayName')} (@{user_info.get('name')})
- **유저 ID**: {user_info.get('id')}
- **가입일**: {user_info.get('created', 'N/A')}
- **다운로드 시간**: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""

        # 확장 아바타 정보 추가
        if extended_info and "api_responses" in extended_info:
            readme_content += "\n## � 아바타 상세 정보\n"
            
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
                    for item in items[:5]:  # 처음 5개만
                        item_name = item.get('name', 'Unknown')
                        item_type = item.get('assetType', {}).get('name', 'Unknown')
                        readme_content += f"  - {item_name} ({item_type})\n"
                    if len(items) > 5:
                        readme_content += f"  - ... 그리고 {len(items) - 5}개 더\n"
            
            # 게임 정보
            games = extended_info["api_responses"].get("games", {})
            if games and "data" in games:
                game_count = len(games["data"])
                readme_content += f"\n## 🎮 제작한 게임 ({game_count}개)\n"
                for game in games["data"][:3]:  # 처음 3개만
                    name = game.get("name", "Untitled")
                    plays = game.get("placeVisits", 0)
                    readme_content += f"- **{name}**: {plays:,} 플레이\n"
            
            # 그룹 정보
            groups = extended_info["api_responses"].get("groups", {})
            if groups and "data" in groups:
                group_count = len(groups["data"])
                readme_content += f"\n## 👥 소속 그룹 ({group_count}개)\n"
                for group_data in groups["data"][:3]:  # 처음 3개만
                    group = group_data.get("group", {})
                    role = group_data.get("role", {})
                    group_name = group.get("name", "Unknown Group")
                    role_name = role.get("name", "Member")
                    readme_content += f"- **{group_name}**: {role_name}\n"

        readme_content += f"""
## �📐 3D 모델 정보
- **카메라 위치**: {camera_info.get('position', 'N/A')}
- **카메라 FOV**: {camera_info.get('fov', 'N/A')}
- **바운딩 박스**: {aabb_info.get('min', 'N/A')} ~ {aabb_info.get('max', 'N/A')}

## 🛠️ 사용 방법

### Blender에서 사용하기
1. Blender를 실행합니다
2. File > Import > Wavefront (.obj) 선택
3. `avatar.obj` 파일을 선택하여 임포트
4. 재질이 자동으로 적용됩니다

### Unity에서 사용하기
1. Unity 프로젝트의 Assets 폴더에 모든 파일을 복사
2. `avatar.obj` 파일을 씬에 드래그
3. 필요시 텍스처를 수동으로 재질에 적용

### Maya에서 사용하기
1. Maya를 실행합니다
2. File > Import > 선택하고 OBJ 형식 설정
3. `avatar.obj` 파일을 임포트

### Three.js/Web에서 사용하기
```javascript
import {{ OBJLoader }} from 'three/examples/jsm/loaders/OBJLoader.js';
import {{ MTLLoader }} from 'three/examples/jsm/loaders/MTLLoader.js';

const mtlLoader = new MTLLoader();
mtlLoader.load('avatar.mtl', (materials) => {{
    materials.preload();
    
    const objLoader = new OBJLoader();
    objLoader.setMaterials(materials);
    objLoader.load('avatar.obj', (object) => {{
        scene.add(object);
    }});
}});
```

## ⚠️ 주의사항
- 이 모델은 로블록스의 R15 또는 R6 형식입니다
- 상업적 사용 시 로블록스 이용약관을 준수해야 합니다
- 텍스처가 투명하게 보일 경우 알파 채널을 비활성화하세요

## 🔧 문제 해결
- **텍스처가 안 보임**: MTL 파일에서 텍스처 경로를 확인하세요
- **모델이 투명함**: 재질의 투명도 설정을 확인하세요
- **크기가 이상함**: 로블록스는 스터드 단위를 사용합니다 (1 스터드 ≈ 0.28m)

다운로드 도구: Roblox Avatar 3D Downloader
"""
        
        readme_file = user_folder / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📋 사용법 안내 파일 생성: {readme_file}")
    
    def download_multiple_avatars_3d(self, user_ids: List[int], include_textures: bool = True):
        """여러 유저의 3D 아바타 다운로드"""
        print(f"🚀 총 {len(user_ids)}명의 3D 아바타 다운로드 시작...")
        
        for i, user_id in enumerate(user_ids, 1):
            print(f"\n[{i}/{len(user_ids)}] 처리 중...")
            self.download_avatar_3d_complete(user_id, include_textures)
            
            # API 제한 방지
            if i < len(user_ids):
                time.sleep(2)
        
        print(f"\n🎊 모든 3D 아바타 다운로드 완료!")
        print(f"📁 저장 위치: {self.download_folder.absolute()}")


def main():
    """메인 함수"""
    print("=== 로블록스 3D 아바타 다운로더 (최신 API) ===\n")
    
    downloader = RobloxAvatar3DDownloader("real_3d_avatars")
    
    print("다운로드 방식을 선택하세요:")
    print("1. 단일 유저 3D 아바타 (텍스처 포함)")
    print("2. 단일 유저 3D 아바타 (모델만)")
    print("3. 여러 유저 3D 아바타")
    print("4. 예시 실행 (유명 유저들)")
    
    try:
        choice = input("\n선택 (1-4): ").strip()
        
        if choice in ["1", "2"]:
            user_input = input("유저 ID 또는 유저명 입력: ").strip()
            user_id = downloader.resolve_user_input(user_input)
            
            if user_id is None:
                print("❌ 유효한 유저를 찾을 수 없습니다.")
                return
            
            include_textures = choice == "1"
            
            downloader.download_avatar_3d_complete(user_id, include_textures)
        
        elif choice == "3":
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
            
            include_textures = input("텍스처도 포함하시겠습니까? (y/n) [기본값: y]: ").strip().lower() != 'n'
            
            downloader.download_multiple_avatars_3d(user_ids, include_textures)
        
        elif choice == "4":
            print("예시: 유명한 로블록스 유저들의 3D 아바타 다운로드")
            # 유저명과 ID 혼합 예시
            example_inputs = ["Roblox", "builderman", "156"]  # 유저명, 유저명, ID
            
            user_ids = []
            for user_input in example_inputs:
                user_id = downloader.resolve_user_input(user_input)
                if user_id:
                    user_ids.append(user_id)
            
            if user_ids:
                downloader.download_multiple_avatars_3d(user_ids, include_textures=True)
        
        else:
            print("잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main()
