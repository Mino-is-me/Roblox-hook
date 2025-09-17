#!/usr/bin/env python3
"""
Attachment 정보가 통합된 3D 다운로더 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
import json

def test_attachment_integration():
    print("=== Attachment 정보 통합 테스트 ===\n")
    
    # 기존에 다운로드된 폴더들을 확인
    test_folders = [
        "test_extended_full/builderman_156_3D",
        "downloads/ddotty_48232800/ddotty_48232800_3D"
    ]
    
    for folder_path in test_folders:
        folder = Path(folder_path)
        if not folder.exists():
            continue
        
        print(f"📂 폴더 분석: {folder.name}")
        
        # metadata.json 확인
        metadata_file = folder / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            print(f"   📋 메타데이터 파일 발견")
            
            # 확장 정보 확인
            if "extended_avatar_info" in metadata:
                ext_info = metadata["extended_avatar_info"]
                print(f"   ✅ 확장 아바타 정보 있음")
                
                # API 응답들 확인
                if "api_responses" in ext_info:
                    api_responses = ext_info["api_responses"]
                    print(f"      - API 응답 종류: {list(api_responses.keys())}")
                    
                    # 아바타 구성 정보
                    if "avatar_config" in api_responses:
                        config = api_responses["avatar_config"]
                        if "assets" in config:
                            print(f"      - 착용 아이템: {len(config['assets'])}개")
                        if "bodyColors" in config:
                            print(f"      - 바디 색상 정보: 있음")
                    
                    # 게임 정보
                    if "games" in api_responses and "data" in api_responses["games"]:
                        games = api_responses["games"]["data"]
                        print(f"      - 제작 게임: {len(games)}개")
                    
                    # 그룹 정보
                    if "groups" in api_responses and "data" in api_responses["groups"]:
                        groups = api_responses["groups"]["data"]
                        print(f"      - 소속 그룹: {len(groups)}개")
            else:
                print(f"   ⚠️ 확장 아바타 정보 없음")
        
        # OBJ 파일 확인
        obj_file = folder / "avatar.obj"
        if obj_file.exists():
            obj_size = obj_file.stat().st_size
            print(f"   📄 OBJ 파일: {obj_size:,} bytes")
            
            # 그룹 정보 간단 분석
            with open(obj_file, 'r', encoding='utf-8') as f:
                groups = []
                vertex_count = 0
                face_count = 0
                
                for line in f:
                    line = line.strip()
                    if line.startswith('g '):
                        group_name = line[2:].strip()
                        groups.append(group_name)
                    elif line.startswith('v '):
                        vertex_count += 1
                    elif line.startswith('f '):
                        face_count += 1
                
                print(f"      - 버텍스: {vertex_count:,}개")
                print(f"      - 면: {face_count:,}개")
                print(f"      - 그룹: {len(groups)}개")
                if groups:
                    print(f"      - 그룹 예시: {', '.join(groups[:5])}")
        
        # MTL 파일 확인
        mtl_file = folder / "avatar.mtl"
        if mtl_file.exists():
            with open(mtl_file, 'r', encoding='utf-8') as f:
                materials = []
                for line in f:
                    line = line.strip()
                    if line.startswith('newmtl '):
                        material_name = line[7:].strip()
                        materials.append(material_name)
            print(f"   🎨 MTL 파일: {len(materials)}개 재질")
        
        # 텍스처 파일들 확인
        texture_folder = folder / "textures"
        if texture_folder.exists():
            texture_files = list(texture_folder.glob("*.png"))
            print(f"   🖼️ 텍스처: {len(texture_files)}개")
        
        print()
    
    print("🎉 Attachment 정보 통합 분석 완료!")

def show_detailed_attachment_info():
    """상세한 attachment 정보 표시"""
    print("\n=== 발견된 Attachment 관련 정보 ===\n")
    
    # Attachment 데이터 폴더 확인
    attachment_folder = Path("attachment_data")
    if attachment_folder.exists():
        print("📁 Attachment 데이터 폴더 발견:")
        for file in attachment_folder.glob("*.json"):
            print(f"   - {file.name}")
    
    # 분석 파일들 확인
    analysis_files = [
        "obj_attachment_analysis.json",
        "obj_attachment_analysis.md"
    ]
    
    print("\n📊 분석 파일들:")
    for file_name in analysis_files:
        file_path = Path(file_name)
        if file_path.exists():
            file_size = file_path.stat().st_size
            print(f"   ✅ {file_name} ({file_size:,} bytes)")
        else:
            print(f"   ❌ {file_name} (없음)")

if __name__ == "__main__":
    test_attachment_integration()
    show_detailed_attachment_info()