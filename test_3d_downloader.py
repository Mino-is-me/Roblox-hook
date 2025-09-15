#!/usr/bin/env python3
"""
3D 모델 다운로드 테스트 스크립트
"""

from roblox_3d_downloader import Roblox3DDownloader

def test_3d_download():
    """3D 모델 다운로드 테스트"""
    print("=== 3D 모델 다운로드 테스트 ===\n")
    
    downloader = Roblox3DDownloader("test_3d")
    
    # 로블록스 창시자 (ID: 1) 테스트
    user_id = 1
    
    print(f"유저 ID {user_id}의 3D 아바타 다운로드 테스트...")
    
    # 유저 정보 확인
    user_info = downloader.get_user_info(user_id)
    if user_info:
        print(f"✅ 유저 정보: {user_info.get('displayName')} (@{user_info.get('name')})")
    else:
        print("❌ 유저 정보를 가져올 수 없습니다.")
        return
    
    # 아바타 데이터 확인
    avatar_data = downloader.get_avatar_data(user_id)
    if avatar_data:
        print(f"✅ 아바타 데이터 확인")
        assets = avatar_data.get("assets", [])
        print(f"   착용 아이템 수: {len(assets)}개")
        
        for i, asset in enumerate(assets[:3], 1):  # 처음 3개만 표시
            asset_name = asset.get("name", "Unknown")
            asset_type = asset.get("assetType", {}).get("name", "Unknown")
            print(f"   {i}. {asset_name} ({asset_type})")
        
        if len(assets) > 3:
            print(f"   ... 및 {len(assets) - 3}개 더")
    else:
        print("❌ 아바타 데이터를 가져올 수 없습니다.")
        return
    
    # 실제 다운로드 테스트 진행
    print(f"\n3D 모델 다운로드를 자동으로 진행합니다...")
    success = downloader.download_3d_avatar(user_id, include_textures=True)
    
    if success:
        print("✅ 3D 모델 다운로드 테스트 성공!")
    else:
        print("❌ 3D 모델 다운로드 테스트 실패!")

if __name__ == "__main__":
    test_3d_download()
