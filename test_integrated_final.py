#!/usr/bin/env python3
"""
통합 3D 다운로더 자동 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from integrated_3d_downloader import RobloxAvatar3DDownloaderIntegrated

def test_integrated_downloader():
    print("=== 통합 3D 다운로더 자동 테스트 ===\n")
    
    downloader = RobloxAvatar3DDownloaderIntegrated("test_integrated_final")
    
    # 테스트할 사용자
    test_username = "builderman"
    
    print(f"🎯 '{test_username}' 통합 다운로드 테스트...")
    
    # 유저 입력 처리
    user_id = downloader.resolve_user_input(test_username)
    
    if user_id:
        # 3D 다운로드 (모든 정보 통합)
        success = downloader.download_avatar_3d_complete(user_id, include_textures=True)
        
        if success:
            print(f"\n🎉 '{test_username}' 통합 다운로드 성공!")
            print("📁 생성된 파일들:")
            print("   ✅ avatar.obj, avatar.mtl (3D 파일)")
            print("   ✅ textures/ (텍스처들)")
            print("   ✅ metadata.json (통합 메타데이터 + Attachment 정보)")
            print("   ✅ README.md (상세한 사용법과 Attachment 가이드)")
            
            print(f"\n📊 통합된 기능들:")
            print("   🎯 3D 모델 다운로드")
            print("   📊 확장 아바타 정보 (API 기반)")
            print("   🎽 착용 아이템 정보")
            print("   🎨 바디 색상 정보")
            print("   🎮 게임 정보")
            print("   👥 그룹 정보")
            print("   📐 OBJ 구조 분석 (Attachment Points)")
            print("   🏷️ 바디 파트 분류")
            print("   📋 통합 메타데이터")
            print("   📖 상세 README (활용법 포함)")
            
        else:
            print(f"❌ '{test_username}' 다운로드 실패")
    else:
        print(f"❌ '{test_username}' 유저를 찾을 수 없습니다")

if __name__ == "__main__":
    test_integrated_downloader()