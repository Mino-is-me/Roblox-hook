#!/usr/bin/env python3
"""
Body Part Mapping Examples
다양한 바디 파트 매핑 파서 사용 예제
"""

import json
from pathlib import Path
import time
from typing import Optional

def find_avatar_packages(base_dir: Path = Path(".")) -> list:
    """사용 가능한 아바타 패키지들 찾기"""
    packages = []
    
    for json_file in base_dir.rglob("COMPLETE_AVATAR_PACKAGE.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            package_info = data.get("package_info", {})
            packages.append({
                "path": json_file.parent,
                "username": package_info.get("username", "Unknown"),
                "user_id": package_info.get("user_id", "Unknown"),
                "created_at": package_info.get("created_at", "Unknown")
            })
        except Exception:
            continue
    
    return packages

def run_enhanced_parser(package_path: Path) -> bool:
    """향상된 파서 실행"""
    try:
        from body_part_mapping_parser import BodyPartMapper
        
        print("🔧 향상된 바디 파트 파서 실행 중...")
        
        mapper = BodyPartMapper()
        avatar_data = mapper.parse_avatar_package(package_path)
        
        if not avatar_data:
            print("❌ 데이터 추출 실패")
            return False
        
        output_path = package_path / "ENHANCED_BODY_PART_MAPPING.txt"
        success = mapper.create_body_part_mapping_text(avatar_data, output_path)
        
        if success:
            print(f"✅ 향상된 매핑 완료: {output_path}")
            return True
        else:
            print("❌ 향상된 매핑 실패")
            return False
            
    except Exception as e:
        print(f"❌ 향상된 파서 오류: {e}")
        return False

def run_simple_parser(package_path: Path) -> bool:
    """간단한 파서 실행"""
    try:
        from simple_body_part_mapper import SimpleBodyPartMapper
        
        print("🔧 간단한 바디 파트 파서 실행 중...")
        
        mapper = SimpleBodyPartMapper()
        data = mapper.extract_groups_from_package(package_path)
        
        if not data:
            print("❌ 데이터 추출 실패")
            return False
        
        output_path = package_path / "SIMPLE_BODY_PART_MAPPING.txt"
        success = mapper.create_simple_mapping_text(data, output_path)
        
        if success:
            print(f"✅ 간단한 매핑 완료: {output_path}")
            return True
        else:
            print("❌ 간단한 매핑 실패")
            return False
            
    except Exception as e:
        print(f"❌ 간단한 파서 오류: {e}")
        return False

def compare_outputs(package_path: Path):
    """생성된 파일들 비교"""
    print("\n📊 생성된 파일 비교:")
    
    files = {
        "원본": package_path / "BODY_PART_MAPPING.txt",
        "향상된": package_path / "ENHANCED_BODY_PART_MAPPING.txt", 
        "간단한": package_path / "SIMPLE_BODY_PART_MAPPING.txt"
    }
    
    print("┌─────────────┬──────────────┬─────────────┐")
    print("│    파일     │    크기      │   상태      │")
    print("├─────────────┼──────────────┼─────────────┤")
    
    for name, file_path in files.items():
        if file_path.exists():
            size = file_path.stat().st_size
            status = "✅ 존재"
        else:
            size = 0
            status = "❌ 없음"
        
        print(f"│ {name:<10} │ {size:>8,} 바이트 │ {status:<10} │")
    
    print("└─────────────┴──────────────┴─────────────┘")

def analyze_body_parts(package_path: Path):
    """바디 파트 분석 정보 출력"""
    json_file = package_path / "COMPLETE_AVATAR_PACKAGE.json"
    
    if not json_file.exists():
        print("❌ 패키지 파일을 찾을 수 없습니다")
        return
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        attachment_info = data.get("attachment_information", {})
        obj_structure = attachment_info.get("obj_structure", {})
        groups = obj_structure.get("groups", [])
        
        print(f"\n🎯 바디 파트 분석:")
        print(f"├─ 총 그룹: {len(groups)}개")
        print(f"├─ 버텍스: {obj_structure.get('vertices', 0):,}개")
        print(f"├─ 면: {obj_structure.get('faces', 0):,}개")
        print(f"└─ 객체: {len(obj_structure.get('objects', []))}개")
        
        print(f"\n📋 그룹 목록:")
        for i, group in enumerate(groups, 1):
            group_name = group.get('name', 'Unknown')
            line_num = group.get('line', 0)
            print(f"  {i:2d}. {group_name:<12} (라인: {line_num:>6,})")
            
    except Exception as e:
        print(f"❌ 분석 오류: {e}")

def main():
    """메인 함수 - 바디 파트 매핑 예제"""
    print("🎯 Body Part Mapping Examples")
    print("═" * 60)
    
    # 사용 가능한 패키지 찾기
    print("🔍 아바타 패키지 검색 중...")
    packages = find_avatar_packages()
    
    if not packages:
        print("❌ 사용 가능한 아바타 패키지를 찾을 수 없습니다.")
        return
    
    print(f"✅ {len(packages)}개 패키지 발견:")
    for i, pkg in enumerate(packages, 1):
        print(f"  {i}. {pkg['username']} (ID: {pkg['user_id']}) - {pkg['path']}")
    
    # 첫 번째 패키지로 예제 실행
    package_path = packages[0]["path"]
    username = packages[0]["username"]
    
    print(f"\n📂 예제 실행: {username} 패키지")
    print("─" * 50)
    
    # 바디 파트 분석
    analyze_body_parts(package_path)
    
    print(f"\n🚀 파서들 실행 중...")
    
    # 향상된 파서 실행
    enhanced_success = run_enhanced_parser(package_path)
    
    # 간단한 파서 실행  
    simple_success = run_simple_parser(package_path)
    
    # 결과 비교
    if enhanced_success or simple_success:
        compare_outputs(package_path)
    
    print(f"\n🎉 예제 실행 완료!")
    
    if enhanced_success:
        enhanced_path = package_path / "ENHANCED_BODY_PART_MAPPING.txt"
        print(f"📄 향상된 매핑: {enhanced_path}")
    
    if simple_success:
        simple_path = package_path / "SIMPLE_BODY_PART_MAPPING.txt"
        print(f"📄 간단한 매핑: {simple_path}")
    
    print(f"\n💡 사용법:")
    print(f"  🔧 향상된 파서: python body_part_mapping_parser.py")
    print(f"  🔧 간단한 파서: python simple_body_part_mapper.py")
    print(f"  🔧 예제 실행: python {Path(__file__).name}")

if __name__ == "__main__":
    main()