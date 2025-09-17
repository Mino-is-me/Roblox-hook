#!/usr/bin/env python3
"""
OBJ 파일에서 Attachment 정보 추출기
3D 모델 파일에서 attachment point, bone structure 등을 파싱
"""

import re
from pathlib import Path
import json
import time

class OBJAttachmentParser:
    def __init__(self):
        self.attachment_patterns = [
            r'# Attachment\s+(\w+)',
            r'# Attach\s+(\w+)',
            r'o\s+(\w*[Aa]ttach\w*)',
            r'g\s+(\w*[Aa]ttach\w*)',
            r'# Bone\s+(\w+)',
            r'o\s+(\w*[Bb]one\w*)',
            r'g\s+(\w*[Bb]one\w*)',
        ]
    
    def parse_obj_file(self, obj_path: Path) -> dict:
        """OBJ 파일에서 attachment 정보 파싱"""
        print(f"🔍 OBJ 파일 분석: {obj_path.name}")
        
        attachment_data = {
            "file_path": str(obj_path),
            "parsed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "attachments": [],
            "bones": [],
            "objects": [],
            "groups": [],
            "comments": [],
            "vertices": 0,
            "faces": 0,
            "materials": []
        }
        
        if not obj_path.exists():
            print(f"   ❌ 파일 없음: {obj_path}")
            return attachment_data
        
        try:
            with open(obj_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print(f"   📄 {len(lines):,}라인 분석 중...")
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # 빈 라인 건너뛰기
                if not line:
                    continue
                
                # 버텍스 카운트
                if line.startswith('v '):
                    attachment_data["vertices"] += 1
                
                # 면 카운트
                elif line.startswith('f '):
                    attachment_data["faces"] += 1
                
                # 오브젝트
                elif line.startswith('o '):
                    obj_name = line[2:].strip()
                    attachment_data["objects"].append({
                        "line": line_num,
                        "name": obj_name
                    })
                    
                    # Attachment 관련 오브젝트 찾기
                    if 'attach' in obj_name.lower() or 'bone' in obj_name.lower():
                        attachment_data["attachments"].append({
                            "type": "object",
                            "line": line_num,
                            "name": obj_name,
                            "source": line
                        })
                
                # 그룹
                elif line.startswith('g '):
                    group_name = line[2:].strip()
                    attachment_data["groups"].append({
                        "line": line_num,
                        "name": group_name
                    })
                    
                    # Attachment 관련 그룹 찾기
                    if 'attach' in group_name.lower() or 'bone' in group_name.lower():
                        attachment_data["attachments"].append({
                            "type": "group",
                            "line": line_num,
                            "name": group_name,
                            "source": line
                        })
                
                # 코멘트 (Attachment 정보가 있을 수 있음)
                elif line.startswith('#'):
                    comment = line[1:].strip()
                    
                    # 중요한 코멘트만 저장
                    if any(keyword in comment.lower() for keyword in ['attach', 'bone', 'joint', 'bind', 'rig']):
                        attachment_data["comments"].append({
                            "line": line_num,
                            "content": comment,
                            "source": line
                        })
                        
                        # 패턴 매칭
                        for pattern in self.attachment_patterns:
                            match = re.search(pattern, line, re.IGNORECASE)
                            if match:
                                attachment_data["attachments"].append({
                                    "type": "comment",
                                    "line": line_num,
                                    "name": match.group(1),
                                    "pattern": pattern,
                                    "source": line
                                })
                
                # 재질 라이브러리
                elif line.startswith('mtllib '):
                    mtl_file = line[7:].strip()
                    attachment_data["materials"].append(mtl_file)
            
            # 결과 출력
            print(f"   ✅ 분석 완료:")
            print(f"      - 버텍스: {attachment_data['vertices']:,}개")
            print(f"      - 면: {attachment_data['faces']:,}개")
            print(f"      - 오브젝트: {len(attachment_data['objects'])}개")
            print(f"      - 그룹: {len(attachment_data['groups'])}개")
            print(f"      - Attachment 관련: {len(attachment_data['attachments'])}개")
            print(f"      - 중요 코멘트: {len(attachment_data['comments'])}개")
            
        except Exception as e:
            print(f"   ❌ 파일 읽기 오류: {e}")
            attachment_data["error"] = str(e)
        
        return attachment_data
    
    def parse_mtl_file(self, mtl_path: Path) -> dict:
        """MTL 파일에서 재질 정보 파싱"""
        print(f"🎨 MTL 파일 분석: {mtl_path.name}")
        
        material_data = {
            "file_path": str(mtl_path),
            "parsed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "materials": [],
            "textures": []
        }
        
        if not mtl_path.exists():
            print(f"   ❌ 파일 없음: {mtl_path}")
            return material_data
        
        try:
            with open(mtl_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            current_material = None
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue
                
                # 새 재질 시작
                if line.startswith('newmtl '):
                    if current_material:
                        material_data["materials"].append(current_material)
                    
                    mat_name = line[7:].strip()
                    current_material = {
                        "name": mat_name,
                        "line": line_num,
                        "properties": {}
                    }
                
                # 재질 속성들
                elif current_material:
                    parts = line.split()
                    if len(parts) >= 2:
                        prop_name = parts[0]
                        prop_value = ' '.join(parts[1:])
                        current_material["properties"][prop_name] = prop_value
                        
                        # 텍스처 파일 찾기
                        if prop_name.startswith('map_') or prop_name in ['bump', 'norm']:
                            material_data["textures"].append({
                                "material": current_material["name"],
                                "property": prop_name,
                                "texture_file": prop_value,
                                "line": line_num
                            })
            
            # 마지막 재질 추가
            if current_material:
                material_data["materials"].append(current_material)
            
            print(f"   ✅ 재질 {len(material_data['materials'])}개, 텍스처 {len(material_data['textures'])}개 발견")
            
        except Exception as e:
            print(f"   ❌ MTL 파일 읽기 오류: {e}")
            material_data["error"] = str(e)
        
        return material_data
    
    def scan_avatar_folders(self, base_folder: str = ".") -> dict:
        """아바타 폴더들을 스캔하여 모든 OBJ/MTL 파일 분석"""
        print(f"🔍 '{base_folder}' 폴더에서 3D 아바타 파일들 스캔...")
        
        base_path = Path(base_folder)
        scan_results = {
            "scanned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "base_folder": str(base_path.absolute()),
            "avatar_folders": []
        }
        
        # 3D 폴더들 찾기
        avatar_folders = []
        for folder_pattern in ["*_3D", "*3d*", "avatar_*", "*avatar*"]:
            avatar_folders.extend(base_path.glob(f"**/{folder_pattern}"))
        
        # 중복 제거
        avatar_folders = list(set(avatar_folders))
        avatar_folders = [f for f in avatar_folders if f.is_dir()]
        
        print(f"   📁 {len(avatar_folders)}개 아바타 폴더 발견")
        
        for folder in avatar_folders:
            print(f"\n📂 폴더 분석: {folder.name}")
            
            folder_data = {
                "folder_path": str(folder),
                "folder_name": folder.name,
                "obj_files": [],
                "mtl_files": [],
                "texture_files": []
            }
            
            # OBJ 파일들 찾기
            obj_files = list(folder.glob("*.obj"))
            for obj_file in obj_files:
                obj_data = self.parse_obj_file(obj_file)
                folder_data["obj_files"].append(obj_data)
            
            # MTL 파일들 찾기
            mtl_files = list(folder.glob("*.mtl"))
            for mtl_file in mtl_files:
                mtl_data = self.parse_mtl_file(mtl_file)
                folder_data["mtl_files"].append(mtl_data)
            
            # 텍스처 파일들 찾기
            texture_extensions = ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tga"]
            for ext in texture_extensions:
                folder_data["texture_files"].extend([
                    {"file": str(f), "name": f.name, "size": f.stat().st_size}
                    for f in folder.glob(ext)
                ])
            
            scan_results["avatar_folders"].append(folder_data)
        
        return scan_results
    
    def save_attachment_analysis(self, scan_results: dict, output_file: str = "attachment_analysis.json"):
        """분석 결과 저장"""
        output_path = Path(output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scan_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 Attachment 분석 결과 저장: {output_path}")
        
        # 요약 리포트도 생성
        self.generate_analysis_report(scan_results, output_path.with_suffix('.md'))
    
    def generate_analysis_report(self, scan_results: dict, report_path: Path):
        """분석 요약 리포트 생성"""
        report = f"""# 3D 아바타 Attachment 분석 리포트

## 📋 분석 개요
- **분석 시간**: {scan_results['scanned_at']}
- **기준 폴더**: {scan_results['base_folder']}
- **발견된 아바타 폴더**: {len(scan_results['avatar_folders'])}개

## 📊 분석 결과
"""
        
        total_attachments = 0
        total_objects = 0
        total_vertices = 0
        total_faces = 0
        
        for folder_data in scan_results["avatar_folders"]:
            folder_name = folder_data["folder_name"]
            obj_count = len(folder_data["obj_files"])
            mtl_count = len(folder_data["mtl_files"])
            texture_count = len(folder_data["texture_files"])
            
            report += f"\n### 📂 {folder_name}\n"
            report += f"- **OBJ 파일**: {obj_count}개\n"
            report += f"- **MTL 파일**: {mtl_count}개\n"
            report += f"- **텍스처 파일**: {texture_count}개\n"
            
            # OBJ 파일 상세 정보
            for obj_data in folder_data["obj_files"]:
                if "error" not in obj_data:
                    vertices = obj_data.get("vertices", 0)
                    faces = obj_data.get("faces", 0)
                    objects = len(obj_data.get("objects", []))
                    attachments = len(obj_data.get("attachments", []))
                    
                    total_vertices += vertices
                    total_faces += faces
                    total_objects += objects
                    total_attachments += attachments
                    
                    report += f"  - **{Path(obj_data['file_path']).name}**:\n"
                    report += f"    - 버텍스: {vertices:,}개\n"
                    report += f"    - 면: {faces:,}개\n"
                    report += f"    - 오브젝트: {objects}개\n"
                    report += f"    - Attachment 관련: {attachments}개\n"
                    
                    # 발견된 Attachment들
                    if attachments > 0:
                        report += f"    - **발견된 Attachment들**:\n"
                        for att in obj_data.get("attachments", [])[:5]:  # 처음 5개만
                            att_name = att.get("name", "Unknown")
                            att_type = att.get("type", "unknown")
                            report += f"      - {att_name} ({att_type})\n"
        
        # 전체 통계
        report += f"\n## 🎯 전체 통계\n"
        report += f"- **총 버텍스**: {total_vertices:,}개\n"
        report += f"- **총 면**: {total_faces:,}개\n"
        report += f"- **총 오브젝트**: {total_objects}개\n"
        report += f"- **총 Attachment 관련**: {total_attachments}개\n"
        
        report += f"\n---\n*리포트 생성 시간: {scan_results['scanned_at']}*\n"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 분석 리포트 생성: {report_path}")

def main():
    print("=== OBJ 파일 Attachment 분석기 ===\n")
    
    parser = OBJAttachmentParser()
    
    # 현재 폴더에서 모든 3D 아바타 파일들 스캔
    scan_results = parser.scan_avatar_folders(".")
    
    # 결과 저장
    parser.save_attachment_analysis(scan_results, "obj_attachment_analysis.json")
    
    print(f"\n🎉 Attachment 분석 완료!")
    print("📁 생성된 파일들:")
    print("   - obj_attachment_analysis.json (상세 데이터)")
    print("   - obj_attachment_analysis.md (요약 리포트)")

if __name__ == "__main__":
    main()