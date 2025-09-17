#!/usr/bin/env python3
"""
Avatar Body Part Mapping Parser
아바타 바디 파트 매핑을 예쁘게 파싱해서 텍스트 파일로 출력
"""

import json
from pathlib import Path
import time
from typing import Dict, List, Tuple

class BodyPartMapper:
    """바디 파트 매핑 클래스"""
    
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
        
        # 바디 파트별 설명
        self.body_part_descriptions = {
            "Head/Face": "머리 및 얼굴 영역 (헬멧, 모자, 안경 등 착용 가능)",
            "Torso Front": "상체 앞면 (셔츠, 재킷 등의 전면 디자인)",
            "Torso Back": "상체 뒷면 (등 장식, 가방, 날개 등 착용 가능)",
            "Left Arm Upper": "왼쪽 팔뚝 상단 (소매 디자인)",
            "Right Arm Upper": "오른쪽 팔뚝 상단 (소매 디자인)",
            "Left Arm Lower": "왼쪽 팔뚝 하단 (팔찌, 장갑 연결부)",
            "Right Arm Lower": "오른쪽 팔뚝 하단 (팔찌, 장갑 연결부)",
            "Left Hand": "왼손 (장갑, 반지 등)",
            "Right Hand": "오른손 (장갑, 반지 등)",
            "Left Leg Upper": "왼쪽 허벅지 (바지 상단 부분)",
            "Right Leg Upper": "오른쪽 허벅지 (바지 상단 부분)",
            "Left Leg Lower": "왼쪽 정강이 (바지 하단, 양말 상단)",
            "Right Leg Lower": "오른쪽 정강이 (바지 하단, 양말 상단)",
            "Left Foot": "왼발 (신발, 양말)",
            "Right Foot": "오른발 (신발, 양말)",
            "Accessory Handle": "액세서리 핸들 (도구, 무기 등의 부착점)"
        }
    
    def parse_avatar_package(self, package_path: Path) -> Dict:
        """아바타 패키지에서 바디 파트 정보 추출"""
        json_file = package_path / "COMPLETE_AVATAR_PACKAGE.json"
        
        if not json_file.exists():
            print(f"❌ 패키지 파일을 찾을 수 없습니다: {json_file}")
            return {}
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # attachment_information에서 obj_structure 추출
            attachment_info = data.get("attachment_information", {})
            obj_structure = attachment_info.get("obj_structure", {})
            groups = obj_structure.get("groups", [])
            
            # 사용자 정보
            package_info = data.get("package_info", {})
            
            return {
                "user_id": package_info.get("user_id"),
                "username": package_info.get("username"),
                "display_name": package_info.get("display_name"),
                "created_at": package_info.get("created_at"),
                "obj_path": obj_structure.get("file_path"),
                "vertices": obj_structure.get("vertices", 0),
                "faces": obj_structure.get("faces", 0),
                "groups": groups
            }
            
        except Exception as e:
            print(f"❌ 패키지 파싱 오류: {e}")
            return {}
    
    def create_body_part_mapping_text(self, avatar_data: Dict, output_path: Path):
        """바디 파트 매핑 텍스트 파일 생성"""
        
        content = f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                           🎯 ROBLOX AVATAR BODY PART MAPPING                   ║
╚════════════════════════════════════════════════════════════════════════════════╝

📋 아바타 정보
├─ 사용자: {avatar_data.get('display_name')} (@{avatar_data.get('username')})
├─ 유저 ID: {avatar_data.get('user_id')}
├─ 생성일: {avatar_data.get('created_at')}
├─ 3D 모델: {avatar_data.get('vertices'):,} 버텍스, {avatar_data.get('faces'):,} 면
└─ OBJ 파일: {avatar_data.get('obj_path', 'N/A')}

═══════════════════════════════════════════════════════════════════════════════════

🎯 BODY PART ATTACHMENT POINTS (OBJ 그룹별)

"""
        
        # 그룹별 매핑 정보
        groups = avatar_data.get('groups', [])
        total_groups = len(groups)
        
        content += f"📊 발견된 그룹: {total_groups}개\n\n"
        
        # 바디 파트별로 분류
        head_parts = []
        torso_parts = []
        arm_parts = []
        leg_parts = []
        accessory_parts = []
        unknown_parts = []
        
        for group in groups:
            group_name = group.get('name', '')
            line_num = group.get('line', 0)
            body_part = self.body_part_mapping.get(group_name, "Unknown")
            color = self.body_part_colors.get(body_part, "❓")
            description = self.body_part_descriptions.get(body_part, "알 수 없는 부위")
            
            part_info = {
                'group_name': group_name,
                'line_num': line_num,
                'body_part': body_part,
                'color': color,
                'description': description
            }
            
            if "Head" in body_part or "Face" in body_part:
                head_parts.append(part_info)
            elif "Torso" in body_part:
                torso_parts.append(part_info)
            elif "Arm" in body_part or "Hand" in body_part:
                arm_parts.append(part_info)
            elif "Leg" in body_part or "Foot" in body_part:
                leg_parts.append(part_info)
            elif "Handle" in body_part or "Accessory" in body_part:
                accessory_parts.append(part_info)
            else:
                unknown_parts.append(part_info)
        
        # 바디 파트별 출력
        if head_parts:
            content += "🟡 HEAD & FACE REGION\n"
            content += "─" * 80 + "\n"
            for part in head_parts:
                content += f"{part['color']} {part['group_name']:<12} → {part['body_part']:<20} (라인: {part['line_num']:,})\n"
                content += f"   💡 {part['description']}\n\n"
        
        if torso_parts:
            content += "🟢 TORSO REGION\n"
            content += "─" * 80 + "\n"
            for part in torso_parts:
                content += f"{part['color']} {part['group_name']:<12} → {part['body_part']:<20} (라인: {part['line_num']:,})\n"
                content += f"   💡 {part['description']}\n\n"
        
        if arm_parts:
            content += "🔵 ARM & HAND REGION\n"
            content += "─" * 80 + "\n"
            for part in arm_parts:
                content += f"{part['color']} {part['group_name']:<12} → {part['body_part']:<20} (라인: {part['line_num']:,})\n"
                content += f"   💡 {part['description']}\n\n"
        
        if leg_parts:
            content += "🟣 LEG & FOOT REGION\n"
            content += "─" * 80 + "\n"
            for part in leg_parts:
                content += f"{part['color']} {part['group_name']:<12} → {part['body_part']:<20} (라인: {part['line_num']:,})\n"
                content += f"   💡 {part['description']}\n\n"
        
        if accessory_parts:
            content += "⭐ ACCESSORY REGION\n"
            content += "─" * 80 + "\n"
            for part in accessory_parts:
                content += f"{part['color']} {part['group_name']:<12} → {part['body_part']:<20} (라인: {part['line_num']:,})\n"
                content += f"   💡 {part['description']}\n\n"
        
        if unknown_parts:
            content += "❓ UNKNOWN REGION\n"
            content += "─" * 80 + "\n"
            for part in unknown_parts:
                content += f"{part['color']} {part['group_name']:<12} → {part['body_part']:<20} (라인: {part['line_num']:,})\n"
                content += f"   💡 {part['description']}\n\n"
        
        content += """
═══════════════════════════════════════════════════════════════════════════════════

🛠️ 활용 가이드

1. 📋 OBJ 파일 구조 이해
   - 각 Player 그룹은 아바타의 특정 바디 파트를 나타냄
   - 라인 번호로 OBJ 파일 내에서 해당 그룹의 위치 확인 가능

2. 🎨 3D 모델링 활용
   - Blender, Maya 등에서 그룹별로 다른 머티리얼 적용 가능
   - 바디 파트별로 텍스처 매핑 최적화

3. 🎮 게임 개발 활용
   - Unity, Unreal Engine에서 바디 파트별 콜라이더 설정
   - 의상 시스템 개발 시 부착점으로 활용

4. 🔧 커스터마이징
   - 특정 바디 파트만 수정하여 개인화된 아바타 생성
   - 액세서리 부착점(Handle) 활용한 도구/무기 장착

═══════════════════════════════════════════════════════════════════════════════════

📊 요약 통계
├─ 총 그룹 수: """ + f"{total_groups}개\n"
        
        # 바디 파트별 통계
        stats = {
            "머리/얼굴": len(head_parts),
            "상체": len(torso_parts), 
            "팔/손": len(arm_parts),
            "다리/발": len(leg_parts),
            "액세서리": len(accessory_parts),
            "미분류": len(unknown_parts)
        }
        
        for part_type, count in stats.items():
            if count > 0:
                content += f"├─ {part_type}: {count}개\n"
        
        content += f"""└─ 3D 메시 복잡도: {avatar_data.get('vertices', 0):,} 버텍스

═══════════════════════════════════════════════════════════════════════════════════

Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
Source: Roblox Avatar Body Part Mapping Parser v1.0
"""
        
        # 파일 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 바디 파트 매핑 파일 생성: {output_path}")
        print(f"   📊 {total_groups}개 그룹 분석 완료")
        
        return True

def main():
    """메인 함수"""
    print("🎯 Avatar Body Part Mapping Parser")
    print("="*60)
    
    mapper = BodyPartMapper()
    
    # builderman 패키지 경로
    package_path = Path("final_integrated/builderman_156")
    
    if not package_path.exists():
        print(f"❌ 패키지 폴더를 찾을 수 없습니다: {package_path}")
        return
    
    print(f"📂 패키지 분석: {package_path}")
    
    # 아바타 데이터 추출
    avatar_data = mapper.parse_avatar_package(package_path)
    
    if not avatar_data:
        print("❌ 아바타 데이터 추출 실패")
        return
    
    # 바디 파트 매핑 텍스트 생성
    output_path = package_path / "BODY_PART_MAPPING.txt"
    
    success = mapper.create_body_part_mapping_text(avatar_data, output_path)
    
    if success:
        print("\n🎉 바디 파트 매핑 파싱 완료!")
        print(f"📄 파일 위치: {output_path}")
    else:
        print("\n❌ 바디 파트 매핑 파싱 실패")

if __name__ == "__main__":
    main()