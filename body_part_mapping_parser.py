#!/usr/bin/env python3
"""
Enhanced Avatar Body Part Mapping Parser
아바타 바디 파트 매핑을 예쁘게 파싱해서 텍스트 파일로 출력
Rich metadata extraction with enhanced formatting and detailed analysis
"""

import json
from pathlib import Path
import time
from typing import Dict, List, Tuple, Optional

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
        """아바타 패키지에서 바디 파트 정보 추출 (향상된 버전)"""
        json_file = package_path / "COMPLETE_AVATAR_PACKAGE.json"
        
        if not json_file.exists():
            print(f"❌ 패키지 파일을 찾을 수 없습니다: {json_file}")
            return {}
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 기본 패키지 정보
            package_info = data.get("package_info", {})
            user_profile = data.get("user_profile", {})
            
            # attachment_information에서 obj_structure 추출
            attachment_info = data.get("attachment_information", {})
            obj_structure = attachment_info.get("obj_structure", {})
            groups = obj_structure.get("groups", [])
            
            # 확장된 아바타 데이터
            extended_avatar_data = data.get("extended_avatar_data", {})
            api_responses = extended_avatar_data.get("api_responses", {})
            avatar_config = api_responses.get("avatar_config", {})
            
            # 착용 중인 아이템 정보
            attachment_data = attachment_info.get("attachment_data", {})
            attachment_info_nested = attachment_data.get("attachment_info", {})
            avatar_details = attachment_info_nested.get("attachment_data", {}).get("avatar_details", {})
            
            return {
                # 기본 정보
                "user_id": package_info.get("user_id"),
                "username": package_info.get("username"),
                "display_name": package_info.get("display_name"),
                "created_at": package_info.get("created_at"),
                
                # 사용자 프로필
                "profile_created": user_profile.get("created"),
                "is_verified": user_profile.get("hasVerifiedBadge", False),
                "is_banned": user_profile.get("isBanned", False),
                
                # 3D 모델 정보
                "obj_path": obj_structure.get("file_path"),
                "vertices": obj_structure.get("vertices", 0),
                "faces": obj_structure.get("faces", 0),
                "groups": groups,
                
                # 아바타 구성 정보
                "avatar_type": avatar_details.get("playerAvatarType", avatar_config.get("playerAvatarType", "Unknown")),
                "body_colors": avatar_details.get("bodyColors", avatar_config.get("bodyColors", {})),
                "scales": avatar_details.get("scales", avatar_config.get("scales", {})),
                "assets": avatar_details.get("assets", avatar_config.get("assets", [])),
                "worn_asset_ids": attachment_info_nested.get("attachment_data", {}).get("currently_wearing", {}).get("assetIds", []),
                
                # 메타데이터
                "analyzed_at": attachment_info.get("analyzed_at"),
                "content_status": data.get("content_status", {})
            }
            
        except Exception as e:
            print(f"❌ 패키지 파싱 오류: {e}")
            return {}

    def get_asset_type_description(self, asset_type_name: str) -> str:
        """애셋 타입에 대한 한국어 설명 반환"""
        asset_descriptions = {
            "Hat": "모자/헬멧",
            "Hair": "헤어스타일", 
            "Face": "얼굴 데칼",
            "Torso": "상체 파츠",
            "RightArm": "오른팔 파츠",
            "LeftArm": "왼팔 파츠",
            "LeftLeg": "왼다리 파츠",
            "RightLeg": "오른다리 파츠",
            "Shirt": "셔츠",
            "Pants": "바지",
            "TShirt": "티셔츠",
            "Gear": "도구/장비",
            "Package": "패키지",
            "DynamicHead": "동적 머리",
            "MoodAnimation": "감정 애니메이션"
        }
        return asset_descriptions.get(asset_type_name, asset_type_name)

    def get_body_color_name(self, color_id: int) -> str:
        """바디 컬러 ID를 컬러명으로 변환"""
        color_names = {
            125: "밝은 노란색 (Light Orange Yellow)",
            1: "흰색 (White)",
            208: "연한 석회색 (Light Stone Grey)",
            194: "중간 석회색 (Medium Stone Grey)", 
            199: "어두운 석회색 (Dark Stone Grey)",
            26: "검은색 (Black)",
            1020: "제도용 붉은색 (Institutional White)",
            1003: "베이지 (Tan)",
            1004: "갈색 (Brown)",
            1005: "살구색 (Nougat)",
            1017: "연한 살구색 (Light Nougat)"
        }
        return color_names.get(color_id, f"컬러 ID {color_id}")
    
    def create_body_part_mapping_text(self, avatar_data: Dict, output_path: Path) -> bool:
        """바디 파트 매핑 텍스트 파일 생성 (향상된 버전)"""
        
        # 헤더 및 기본 정보
        content = f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    🎯 ENHANCED ROBLOX AVATAR BODY PART MAPPING                 ║
╚════════════════════════════════════════════════════════════════════════════════╝

🎭 아바타 프로필 정보
├─ 👤 사용자: {avatar_data.get('display_name', 'N/A')} (@{avatar_data.get('username', 'N/A')})
├─ 🆔 유저 ID: {avatar_data.get('user_id', 'N/A')}
├─ 📅 계정 생성: {avatar_data.get('profile_created', 'N/A')[:10] if avatar_data.get('profile_created') else 'N/A'}
├─ ✅ 인증 배지: {'🟢 Yes' if avatar_data.get('is_verified') else '🔴 No'}
├─ 🚫 밴 상태: {'🔴 Banned' if avatar_data.get('is_banned') else '🟢 Active'}
└─ 📊 분석 시각: {avatar_data.get('created_at', 'N/A')}

🎨 아바타 구성 정보
├─ 🤖 아바타 타입: {avatar_data.get('avatar_type', 'Unknown')}"""

        # 바디 컬러 정보
        body_colors = avatar_data.get('body_colors', {})
        if body_colors:
            content += f"\n├─ 🎨 바디 컬러 구성:"
            for part, color_id in body_colors.items():
                part_name = {
                    'headColorId': '머리',
                    'torsoColorId': '몸통', 
                    'rightArmColorId': '오른팔',
                    'leftArmColorId': '왼팔',
                    'rightLegColorId': '오른다리',
                    'leftLegColorId': '왼다리'
                }.get(part, part)
                color_name = self.get_body_color_name(color_id)
                content += f"\n│  └─ {part_name}: {color_name}"

        # 스케일 정보
        scales = avatar_data.get('scales', {})
        if scales:
            content += f"\n├─ 📏 아바타 스케일:"
            for scale_type, value in scales.items():
                if value != 1.0 and value != 0.0:  # 기본값이 아닌 경우만 표시
                    content += f"\n│  └─ {scale_type.title()}: {value:.1f}"

        # 착용 중인 아이템
        assets = avatar_data.get('assets', [])
        if assets:
            content += f"\n└─ 👔 착용 중인 아이템 ({len(assets)}개):"
            for asset in assets[:5]:  # 처음 5개만 표시
                asset_name = asset.get('name', 'Unknown Item')
                asset_type = asset.get('assetType', {}).get('name', 'Unknown')
                asset_type_kr = self.get_asset_type_description(asset_type)
                content += f"\n   └─ {asset_name} ({asset_type_kr})"
            if len(assets) > 5:
                content += f"\n   └─ ... 및 {len(assets) - 5}개 추가 아이템"

        content += f"""

🏗️ 3D 모델 구조 정보
├─ 📄 OBJ 파일: {avatar_data.get('obj_path', 'N/A')}
├─ 🔺 버텍스 수: {avatar_data.get('vertices', 0):,}개
├─ 🔶 면(Face) 수: {avatar_data.get('faces', 0):,}개
└─ 🎯 바디 파트 그룹: {len(avatar_data.get('groups', []))}개

╔════════════════════════════════════════════════════════════════════════════════╗
║                          🎯 BODY PART ATTACHMENT POINTS                        ║
╚════════════════════════════════════════════════════════════════════════════════╝

"""
        
        # 그룹별 매핑 정보
        groups = avatar_data.get('groups', [])
        total_groups = len(groups)
        
        content += f"📊 발견된 바디 파트 그룹: {total_groups}개\n\n"
        
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
        
        # 향상된 바디 파트별 출력
        def format_body_region(parts: List[Dict], region_name: str, region_color: str):
            if not parts:
                return ""
            
            region_content = f"{region_color} {region_name}\n"
            region_content += "═" * 85 + "\n"
            
            for i, part in enumerate(parts):
                # 메인 라인
                region_content += f"{part['color']} [{part['group_name']:<12}] → {part['body_part']:<22} (OBJ 라인: {part['line_num']:>6,})\n"
                # 설명 라인  
                region_content += f"   💡 {part['description']}\n"
                
                if i < len(parts) - 1:  # 마지막이 아니면 구분선 추가
                    region_content += "   " + "─" * 75 + "\n"
                region_content += "\n"
            
            return region_content
        
        # 각 영역별 출력
        content += format_body_region(head_parts, "HEAD & FACE REGION", "🟡")
        content += format_body_region(torso_parts, "TORSO REGION", "🟢") 
        content += format_body_region(arm_parts, "ARM & HAND REGION", "🔵")
        content += format_body_region(leg_parts, "LEG & FOOT REGION", "🟣")
        content += format_body_region(accessory_parts, "ACCESSORY REGION", "⭐")
        content += format_body_region(unknown_parts, "UNKNOWN REGION", "❓")

        # 향상된 활용 가이드
        content += """╔════════════════════════════════════════════════════════════════════════════════╗
║                               🛠️ 활용 가이드                                   ║
╚════════════════════════════════════════════════════════════════════════════════╝

1. 🎨 3D 모델링 소프트웨어 활용
   ┌─ Blender 활용법:
   │  • OBJ 파일을 Import 할 때 각 그룹이 개별 오브젝트로 분리됨
   │  • 그룹별로 다른 머티리얼과 텍스처 적용 가능
   │  • 특정 바디 파트만 선택하여 편집/애니메이션 가능
   │
   └─ Maya/3ds Max 활용법:
      • 그룹 이름으로 특정 바디 파트 빠르게 선택 가능
      • 바디 파트별로 UV 매핑 최적화
      • 리깅 시 본(Bone) 구조 참고 자료로 활용

2. 🎮 게임 개발 엔진 활용
   ┌─ Unity 활용법:
   │  • 바디 파트별 콜라이더 설정으로 정밀한 히트박스 구현
   │  • 의상 시스템 개발 시 부착점(Attachment Point) 활용
   │  • Asset ID를 통한 원본 Roblox 아이템 추적
   │
   └─ Unreal Engine 활용법:
      • 스켈레탈 메시로 변환 시 바디 파트 기반 본 구조 생성
      • 머티리얼 인스턴스를 통한 바디 컬러 동적 변경
      • 액세서리 소켓 포인트로 Handle1 활용

3. 🔧 프로그래밍 활용
   ┌─ Python/JavaScript:
   │  • JSON 메타데이터와 OBJ 그룹 정보 조합한 자동화 스크립트
   │  • 바디 파트별 텍스처 자동 적용 도구 개발
   │  • 아바타 커스터마이징 시스템 백엔드 구현
   │
   └─ 웹 개발:
      • Three.js에서 그룹별 인터랙션 구현
      • WebGL 기반 아바타 뷰어 개발
      • 실시간 아바타 편집 웹 애플리케이션

4. 🎯 커스터마이징 및 모딩
   • 특정 바디 파트만 수정하여 개인화된 아바타 생성
   • 액세서리 부착점(Handle1) 활용한 도구/무기 시스템
   • 바디 컬러 정보를 통한 스킨톤 매칭 시스템
   • 아바타 타입(R15) 기반 호환성 검증 시스템

"""

        # 향상된 통계 섹션
        content += """╔════════════════════════════════════════════════════════════════════════════════╗
║                                📊 상세 분석 통계                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

"""
        
        # 바디 파트별 통계
        stats = {
            "🟡 머리/얼굴": len(head_parts),
            "🟢 몸통": len(torso_parts), 
            "🔵 팔/손": len(arm_parts),
            "🟣 다리/발": len(leg_parts),
            "⭐ 액세서리": len(accessory_parts),
            "❓ 미분류": len(unknown_parts)
        }
        
        content += "📈 바디 파트별 분포:\n"
        total_classified = sum(count for name, count in stats.items() if "미분류" not in name)
        
        for part_type, count in stats.items():
            if count > 0:
                percentage = (count / total_groups * 100) if total_groups > 0 else 0
                bar = "█" * min(int(percentage / 5), 20)  # 최대 20자의 바
                content += f"├─ {part_type:<12}: {count:>2}개 [{percentage:>5.1f}%] {bar}\n"
        
        content += f"""
📊 3D 메시 복잡도 분석:
├─ 버텍스 밀도: {avatar_data.get('vertices', 0) / max(total_groups, 1):.0f} 버텍스/그룹
├─ 면 밀도: {avatar_data.get('faces', 0) / max(total_groups, 1):.0f} 면/그룹
├─ 폴리곤 구성: {'고해상도' if avatar_data.get('vertices', 0) > 2000 else '표준해상도'}
└─ 최적화 수준: {'매우 상세' if avatar_data.get('faces', 0) > 3000 else '게임 최적화'}

🎭 아바타 특성 분석:
├─ 아바타 세대: {avatar_data.get('avatar_type', 'Unknown')} {'(최신)' if avatar_data.get('avatar_type') == 'R15' else '(레거시)'}
├─ 커스터마이징 수준: {'높음' if len(avatar_data.get('assets', [])) > 5 else '보통'}
├─ 바디 컬러 통일성: {'단일 컬러' if len(set(avatar_data.get('body_colors', {}).values())) <= 1 else '다중 컬러'}
└─ 프리미엄 아이템: {'포함됨' if avatar_data.get('is_verified') else '확인 불가'}

"""

        # 파일 정보 및 생성 정보
        content += f"""╔════════════════════════════════════════════════════════════════════════════════╗
║                                  📄 파일 정보                                   ║
╚════════════════════════════════════════════════════════════════════════════════╝

📁 생성된 파일 구조:
├─ 📋 {output_path.name} (이 파일)
├─ 📊 COMPLETE_AVATAR_PACKAGE.json (원본 데이터)
├─ 📷 2D 썸네일 이미지들 (avatar_*.png, headshot_*.png, bust_*.png)
├─ 🎯 3D_Model/avatar.obj (3D 메시 파일)
├─ 🎨 3D_Model/avatar.mtl (머티리얼 파일)
└─ 🖼️ 3D_Model/textures/ (텍스처 파일들)

💾 데이터 무결성:
├─ 원본 아바타 ID: {avatar_data.get('user_id')}
├─ 추출 시각: {avatar_data.get('analyzed_at')}
├─ 패키지 생성: {avatar_data.get('created_at')}
└─ 파서 버전: Enhanced Body Part Mapping Parser v2.0

═══════════════════════════════════════════════════════════════════════════════════

🕒 Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
🔧 Source: Enhanced Roblox Avatar Body Part Mapping Parser v2.0
🏠 Repository: https://github.com/Mino-is-me/Roblox-hook
📧 Issues: https://github.com/Mino-is-me/Roblox-hook/issues

═══════════════════════════════════════════════════════════════════════════════════
"""
        
        try:
            # 파일 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 향상된 바디 파트 매핑 파일 생성: {output_path}")
            print(f"   📊 {total_groups}개 그룹 상세 분석 완료")
            print(f"   📄 파일 크기: {len(content):,} 문자")
            print(f"   🎯 {len(assets)}개 착용 아이템 정보 포함")
            
            return True
            
        except Exception as e:
            print(f"❌ 파일 저장 오류: {e}")
            return False

def main():
    """메인 함수 - 향상된 바디 파트 매핑 파서"""
    print("🎯 Enhanced Avatar Body Part Mapping Parser v2.0")
    print("═" * 65)
    
    mapper = BodyPartMapper()
    
    # 패키지 경로 확인
    package_path = Path("final_integrated/builderman_156")
    
    if not package_path.exists():
        print(f"❌ 패키지 폴더를 찾을 수 없습니다: {package_path}")
        print("💡 다른 패키지 경로를 시도해보겠습니다...")
        
        # 다른 패키지들 찾아보기
        potential_paths = list(Path(".").rglob("COMPLETE_AVATAR_PACKAGE.json"))
        if potential_paths:
            package_path = potential_paths[0].parent
            print(f"✅ 대체 패키지 발견: {package_path}")
        else:
            print("❌ 사용 가능한 아바타 패키지를 찾을 수 없습니다.")
            return
    
    print(f"📂 패키지 분석 중: {package_path}")
    print("⏳ 데이터 추출 및 분석 중...")
    
    # 아바타 데이터 추출
    avatar_data = mapper.parse_avatar_package(package_path)
    
    if not avatar_data:
        print("❌ 아바타 데이터 추출 실패")
        return
    
    print(f"✅ 데이터 추출 완료:")
    print(f"   👤 사용자: {avatar_data.get('display_name')} (@{avatar_data.get('username')})")
    print(f"   🎭 아바타 타입: {avatar_data.get('avatar_type', 'Unknown')}")
    print(f"   📊 바디 파트: {len(avatar_data.get('groups', []))}개 그룹")
    print(f"   🎨 착용 아이템: {len(avatar_data.get('assets', []))}개")
    
    # 향상된 바디 파트 매핑 텍스트 생성
    output_path = package_path / "ENHANCED_BODY_PART_MAPPING.txt"
    
    print(f"\n📝 향상된 바디 파트 매핑 생성 중...")
    success = mapper.create_body_part_mapping_text(avatar_data, output_path)
    
    if success:
        print("\n🎉 향상된 바디 파트 매핑 생성 완료!")
        print(f"📄 파일 위치: {output_path}")
        print(f"📁 파일 크기: {output_path.stat().st_size:,} 바이트")
        
        # 기존 파일과의 비교
        old_path = package_path / "BODY_PART_MAPPING.txt"
        if old_path.exists():
            old_size = old_path.stat().st_size
            new_size = output_path.stat().st_size
            improvement = ((new_size - old_size) / old_size * 100) if old_size > 0 else 0
            print(f"📈 기존 파일 대비 {improvement:+.1f}% 향상 ({new_size - old_size:+,} 바이트)")
            
    else:
        print("\n❌ 향상된 바디 파트 매핑 생성 실패")

if __name__ == "__main__":
    main()