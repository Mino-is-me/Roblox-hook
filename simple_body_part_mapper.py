#!/usr/bin/env python3
"""
Simple Body Part Mapping Parser
아바타 바디 파트 매핑만 예쁘게 파싱해서 단순한 텍스트 파일로 출력
"""

import json
from pathlib import Path
import time
from typing import Dict, List

class SimpleBodyPartMapper:
    """간단한 바디 파트 매핑 클래스"""
    
    def __init__(self):
        # 알려진 Player 그룹과 바디 파트 매핑
        self.body_part_mapping = {
            "Player1": "Head/Face",
            "Player2": "Torso Front",
            "Player3": "Left Arm Upper",
            "Player4": "Right Arm Upper", 
            "Player5": "Left Arm Lower",
            "Player6": "Right Arm Lower",
            "Player7": "Left Hand",
            "Player8": "Right Hand",
            "Player9": "Torso Back",
            "Player10": "Left Leg Upper",
            "Player11": "Right Leg Upper",
            "Player12": "Left Leg Lower", 
            "Player13": "Right Leg Lower",
            "Player14": "Left Foot",
            "Player15": "Right Foot",
            "Handle1": "Accessory Handle"
        }
        
        # 바디 파트별 색상 코드 (시각적 구분)
        self.body_part_colors = {
            "Head/Face": "🟡",
            "Torso Front": "🟢",
            "Torso Back": "🟢",
            "Left Arm Upper": "🔵",
            "Right Arm Upper": "🔵", 
            "Left Arm Lower": "🔷",
            "Right Arm Lower": "🔷",
            "Left Hand": "🟦",
            "Right Hand": "🟦",
            "Left Leg Upper": "🟣",
            "Right Leg Upper": "🟣",
            "Left Leg Lower": "🟪",
            "Right Leg Lower": "🟪",
            "Left Foot": "🟫",
            "Right Foot": "🟫",
            "Accessory Handle": "⭐"
        }
    
    def extract_groups_from_package(self, package_path: Path) -> Dict:
        """패키지에서 기본 그룹 정보만 추출"""
        json_file = package_path / "COMPLETE_AVATAR_PACKAGE.json"
        
        if not json_file.exists():
            return {}
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            attachment_info = data.get("attachment_information", {})
            obj_structure = attachment_info.get("obj_structure", {})
            groups = obj_structure.get("groups", [])
            
            package_info = data.get("package_info", {})
            
            return {
                "username": package_info.get("username", "Unknown"),
                "user_id": package_info.get("user_id", "Unknown"),
                "groups": groups,
                "vertices": obj_structure.get("vertices", 0),
                "faces": obj_structure.get("faces", 0)
            }
            
        except Exception as e:
            print(f"❌ 오류: {e}")
            return {}
    
    def create_simple_mapping_text(self, data: Dict, output_path: Path) -> bool:
        """간단한 바디 파트 매핑 텍스트 생성"""
        
        groups = data.get('groups', [])
        username = data.get('username', 'Unknown')
        user_id = data.get('user_id', 'Unknown')
        
        content = f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🎯 BODY PART MAPPING - {username} (ID: {user_id})                    │
└─────────────────────────────────────────────────────────────────────────────┘

📋 Body Part Mapping ({len(groups)}개 그룹)

"""
        
        # 그룹별 정보를 바디 파트 순서대로 정렬
        sorted_groups = []
        for group in groups:
            group_name = group.get('name', '')
            line_num = group.get('line', 0)
            body_part = self.body_part_mapping.get(group_name, "Unknown")
            color = self.body_part_colors.get(body_part, "❓")
            
            # 정렬을 위한 우선순위
            priority = {
                "Head/Face": 1,
                "Torso Front": 2, "Torso Back": 3,
                "Left Arm Upper": 4, "Right Arm Upper": 5,
                "Left Arm Lower": 6, "Right Arm Lower": 7,
                "Left Hand": 8, "Right Hand": 9,
                "Left Leg Upper": 10, "Right Leg Upper": 11,
                "Left Leg Lower": 12, "Right Leg Lower": 13,
                "Left Foot": 14, "Right Foot": 15,
                "Accessory Handle": 16
            }.get(body_part, 99)
            
            sorted_groups.append({
                'group_name': group_name,
                'line_num': line_num,
                'body_part': body_part,
                'color': color,
                'priority': priority
            })
        
        # 우선순위로 정렬
        sorted_groups.sort(key=lambda x: x['priority'])
        
        # 바디 파트 매핑 출력
        for part in sorted_groups:
            content += f"{part['color']} {part['group_name']:<12} → {part['body_part']:<18} (라인: {part['line_num']:>6,})\n"
        
        content += f"""

┌─────────────────────────────────────────────────────────────────────────────┐
│                              🎨 Color Guide                                 │
└─────────────────────────────────────────────────────────────────────────────┘

🟡 Head/Face       🟢 Torso (Front/Back)    🔵🔷🟦 Arms & Hands
🟣🟪🟫 Legs & Feet   ⭐ Accessory Handle      ❓ Unknown Parts

┌─────────────────────────────────────────────────────────────────────────────┐
│                             📊 Quick Stats                                 │
└─────────────────────────────────────────────────────────────────────────────┘

총 그룹:     {len(groups):>3}개
3D 버텍스:   {data.get('vertices', 0):>6,}개  
3D 면:       {data.get('faces', 0):>6,}개

┌─────────────────────────────────────────────────────────────────────────────┐
│  Generated: {time.strftime('%Y-%m-%d %H:%M:%S')} | Simple Body Part Mapper v1.0  │
└─────────────────────────────────────────────────────────────────────────────┘
"""
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 간단한 바디 파트 매핑 파일 생성: {output_path}")
            return True
        except Exception as e:
            print(f"❌ 파일 저장 오류: {e}")
            return False

def main():
    """메인 함수"""
    print("🎯 Simple Body Part Mapping Parser")
    print("─" * 50)
    
    mapper = SimpleBodyPartMapper()
    
    # 패키지 경로
    package_path = Path("final_integrated/builderman_156")
    
    if not package_path.exists():
        print(f"❌ 패키지를 찾을 수 없습니다: {package_path}")
        return
    
    print(f"📂 패키지 분석: {package_path}")
    
    # 데이터 추출
    data = mapper.extract_groups_from_package(package_path)
    
    if not data:
        print("❌ 데이터 추출 실패")
        return
    
    print(f"✅ {data.get('username')} 아바타 - {len(data.get('groups', []))}개 그룹 발견")
    
    # 간단한 매핑 텍스트 생성
    output_path = package_path / "SIMPLE_BODY_PART_MAPPING.txt"
    
    success = mapper.create_simple_mapping_text(data, output_path)
    
    if success:
        print(f"🎉 간단한 바디 파트 매핑 완료!")
        print(f"📄 파일: {output_path}")
        print(f"📏 크기: {output_path.stat().st_size:,} 바이트")

if __name__ == "__main__":
    main()