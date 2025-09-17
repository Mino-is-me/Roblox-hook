#!/usr/bin/env python3
"""
Roblox Attachment 정보 수집기
아바타의 Attachment, 액세서리 부착점, 본 구조 등을 수집
"""

import requests
import json
from pathlib import Path
import time

class RobloxAttachmentExplorer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        
    def explore_attachment_apis(self, user_id: int) -> dict:
        """Attachment 관련 API들을 탐색"""
        print(f"🔍 사용자 ID {user_id}의 Attachment 관련 정보 탐색 중...")
        
        attachment_info = {
            "user_id": user_id,
            "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "attachment_data": {}
        }
        
        # 1. 아바타 상세 정보 (Attachment 정보 포함)
        print("   🎯 아바타 상세 정보...")
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/avatar")
            if response.status_code == 200:
                avatar_data = response.json()
                attachment_info["attachment_data"]["avatar_details"] = avatar_data
                
                # Assets에서 attachment 정보 추출
                if "assets" in avatar_data:
                    print(f"   ✅ {len(avatar_data['assets'])}개 아이템의 상세 정보 수집 완료")
                else:
                    print("   ✅ 아바타 상세 정보 수집 완료")
            else:
                print(f"   ❌ 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 오류: {e}")
            
        # 2. 아바타 메타데이터 (더 자세한 정보)
        print("   📊 아바타 메타데이터...")
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/avatar/metadata")
            if response.status_code == 200:
                attachment_info["attachment_data"]["avatar_metadata"] = response.json()
                print("   ✅ 아바타 메타데이터 수집 완료")
            else:
                print(f"   ⚠️ 아바타 메타데이터 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 아바타 메타데이터 오류: {e}")
            
        # 3. 착용 중인 아이템들의 상세 정보
        print("   🎽 착용 아이템 상세 정보...")
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing")
            if response.status_code == 200:
                wearing_data = response.json()
                attachment_info["attachment_data"]["currently_wearing"] = wearing_data
                
                # 각 아이템의 상세 정보 수집
                if "assetIds" in wearing_data:
                    asset_details = []
                    asset_ids = wearing_data["assetIds"][:10]  # 처음 10개만
                    
                    print(f"   📝 {len(asset_ids)}개 아이템의 상세 정보 수집 중...")
                    for asset_id in asset_ids:
                        asset_detail = self.get_asset_details(asset_id)
                        if asset_detail:
                            asset_details.append(asset_detail)
                        time.sleep(0.2)  # API 제한 방지
                    
                    attachment_info["attachment_data"]["asset_details"] = asset_details
                    print(f"   ✅ {len(asset_details)}개 아이템 상세 정보 수집 완료")
                else:
                    print("   ✅ 착용 아이템 정보 수집 완료")
            elif response.status_code == 429:
                print("   ⚠️ API 제한 (429)")
            else:
                print(f"   ❌ 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 오류: {e}")
            
        # 4. 아바타 Outfit 정보
        print("   👔 아바타 Outfit 정보...")
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/outfits?page=1&itemsPerPage=10")
            if response.status_code == 200:
                outfit_data = response.json()
                attachment_info["attachment_data"]["outfits"] = outfit_data
                print(f"   ✅ Outfit 정보 수집 완료")
            else:
                print(f"   ⚠️ Outfit 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Outfit 정보 오류: {e}")
            
        # 5. 아바타 Asset 타입별 정보
        print("   🏷️ Asset 타입 정보...")
        try:
            response = self.session.get("https://avatar.roblox.com/v1/avatar/asset-types")
            if response.status_code == 200:
                asset_types = response.json()
                attachment_info["attachment_data"]["asset_types"] = asset_types
                print(f"   ✅ Asset 타입 정보 수집 완료")
            else:
                print(f"   ⚠️ Asset 타입 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Asset 타입 오류: {e}")
            
        return attachment_info
    
    def get_asset_details(self, asset_id: int) -> dict:
        """개별 Asset의 상세 정보 수집"""
        try:
            # Asset 기본 정보
            response = self.session.get(f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}")
            if response.status_code == 200:
                asset_data = {
                    "asset_id": asset_id,
                    "delivery_data": response.json()
                }
                
                # Catalog API를 통한 추가 정보
                catalog_response = self.session.get(f"https://catalog.roblox.com/v1/catalog/items/details?items={asset_id}")
                if catalog_response.status_code == 200:
                    catalog_data = catalog_response.json()
                    asset_data["catalog_data"] = catalog_data
                
                return asset_data
            else:
                return {"asset_id": asset_id, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"asset_id": asset_id, "error": str(e)}
    
    def explore_3d_attachment_metadata(self, user_id: int) -> dict:
        """3D 모델에서 Attachment 정보 추출"""
        print(f"   🎯 3D 모델 Attachment 정보...")
        
        attachment_3d = {
            "user_id": user_id,
            "3d_attachments": {}
        }
        
        try:
            # 3D Avatar API
            response = self.session.get(f"https://thumbnails.roblox.com/v1/users/avatar-3d?userIds={user_id}&format=Obj&size=768x432")
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    avatar_3d = data["data"][0]
                    if "imageUrl" in avatar_3d:
                        # 3D 메타데이터에서 attachment 정보 파싱
                        attachment_3d["3d_attachments"]["metadata_url"] = avatar_3d["imageUrl"]
                        
                        # 메타데이터 다운로드 시도
                        meta_response = self.session.get(avatar_3d["imageUrl"])
                        if meta_response.status_code == 200:
                            meta_data = meta_response.json()
                            attachment_3d["3d_attachments"]["full_metadata"] = meta_data
                            
                            # Attachment 포인트 정보 추출
                            if "attachments" in meta_data:
                                attachment_3d["3d_attachments"]["attachment_points"] = meta_data["attachments"]
                                print(f"   ✅ {len(meta_data['attachments'])}개 Attachment 포인트 발견!")
                            
                            print("   ✅ 3D Attachment 메타데이터 수집 완료")
                        else:
                            print(f"   ⚠️ 3D 메타데이터 다운로드 실패: {meta_response.status_code}")
                else:
                    print("   ⚠️ 3D 데이터 없음")
            else:
                print(f"   ❌ 3D API 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 3D Attachment 오류: {e}")
            
        return attachment_3d
    
    def save_attachment_data(self, user_id: int, attachment_info: dict, attachment_3d: dict, output_dir: str = "attachment_data"):
        """Attachment 데이터 저장"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 사용자명 가져오기
        username = "unknown"
        if "attachment_data" in attachment_info and "avatar_details" in attachment_info["attachment_data"]:
            username = "unknown"  # 기본값 설정
        
        # 사용자 정보 API 호출
        try:
            response = self.session.get(f"https://users.roblox.com/v1/users/{user_id}")
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get("name", "unknown")
        except:
            pass
        
        # 통합 데이터
        combined_data = {
            "user_id": user_id,
            "username": username,
            "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "attachment_info": attachment_info,
            "attachment_3d": attachment_3d
        }
        
        # JSON 파일 저장
        filename = f"{username}_{user_id}_attachments.json"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
            
        print(f"📁 Attachment 데이터 저장: {filepath}")
        
        # 요약 리포트 생성
        self.generate_attachment_report(combined_data, output_path / f"{username}_{user_id}_attachment_report.md")
        
    def generate_attachment_report(self, data: dict, filepath: Path):
        """Attachment 요약 리포트 생성"""
        user_id = data["user_id"]
        username = data["username"]
        
        report = f"""# {username} (ID: {user_id}) - Attachment 정보 리포트

## 📋 기본 정보
- **수집 시간**: {data['collected_at']}
- **사용자 ID**: {user_id}
- **사용자명**: {username}

## 🎯 Attachment 포인트 정보
"""
        
        # 3D Attachment 정보
        attachment_3d = data.get("attachment_3d", {})
        if "3d_attachments" in attachment_3d and "attachment_points" in attachment_3d["3d_attachments"]:
            points = attachment_3d["3d_attachments"]["attachment_points"]
            report += f"- **발견된 Attachment 포인트**: {len(points)}개\n\n"
            
            for i, point in enumerate(points[:10]):  # 처음 10개만
                report += f"### Attachment {i+1}\n"
                if "Name" in point:
                    report += f"- **이름**: {point['Name']}\n"
                if "CFrame" in point:
                    cframe = point["CFrame"]
                    report += f"- **위치**: {cframe}\n"
                if "Visible" in point:
                    report += f"- **표시 여부**: {point['Visible']}\n"
                report += "\n"
        else:
            report += "- **Attachment 포인트**: 정보 없음\n\n"
        
        # Asset 상세 정보
        attachment_info = data.get("attachment_info", {})
        if "attachment_data" in attachment_info:
            att_data = attachment_info["attachment_data"]
            
            # Asset 타입 정보
            if "asset_types" in att_data:
                asset_types = att_data["asset_types"]
                if "data" in asset_types:
                    report += f"## 🏷️ 지원되는 Asset 타입들 ({len(asset_types['data'])}개)\n"
                    for asset_type in asset_types["data"][:15]:  # 처음 15개만
                        name = asset_type.get("name", "Unknown")
                        type_id = asset_type.get("id", "N/A")
                        report += f"- **{name}** (ID: {type_id})\n"
                    report += "\n"
            
            # 착용 아이템 상세 정보
            if "asset_details" in att_data:
                details = att_data["asset_details"]
                report += f"## 👕 착용 아이템 상세 정보 ({len(details)}개)\n"
                
                for detail in details[:5]:  # 처음 5개만
                    asset_id = detail.get("asset_id", "Unknown")
                    report += f"### Asset ID: {asset_id}\n"
                    
                    if "catalog_data" in detail:
                        catalog = detail["catalog_data"]
                        if "data" in catalog and len(catalog["data"]) > 0:
                            item = catalog["data"][0]
                            name = item.get("name", "Unknown")
                            item_type = item.get("itemType", "Unknown")
                            report += f"- **이름**: {name}\n"
                            report += f"- **타입**: {item_type}\n"
                            if "price" in item:
                                report += f"- **가격**: {item['price']} Robux\n"
                    report += "\n"
            
            # Outfit 정보
            if "outfits" in att_data:
                outfits = att_data["outfits"]
                if "data" in outfits:
                    outfit_count = len(outfits["data"])
                    report += f"## 👔 저장된 Outfit ({outfit_count}개)\n"
                    for outfit in outfits["data"][:3]:  # 처음 3개만
                        name = outfit.get("name", "Untitled Outfit")
                        is_editable = outfit.get("isEditable", False)
                        report += f"- **{name}** {'(편집 가능)' if is_editable else '(읽기 전용)'}\n"
                    report += "\n"
        
        report += f"""
---
*리포트 생성 시간: {data['collected_at']}*
*API 데이터 소스: Roblox Avatar, Asset Delivery, Catalog APIs*
"""
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"📄 Attachment 리포트 생성: {filepath}")

def main():
    print("=== Roblox Attachment 정보 수집기 ===\n")
    
    explorer = RobloxAttachmentExplorer()
    
    # 테스트할 사용자들
    test_users = [
        ("builderman", 156),   # 많은 아이템을 가진 사용자
        ("Roblox", 1),         # 로블록스 공식 계정
        ("ddotty", 48232800)   # 현재 보고 있던 사용자
    ]
    
    for username, user_id in test_users:
        print(f"\n{'='*50}")
        print(f"🎯 {username} (ID: {user_id}) Attachment 정보 수집")
        print(f"{'='*50}")
        
        # Attachment 정보 수집
        attachment_info = explorer.explore_attachment_apis(user_id)
        attachment_3d = explorer.explore_3d_attachment_metadata(user_id)
        
        # 저장
        explorer.save_attachment_data(user_id, attachment_info, attachment_3d)
        
        print(f"✅ {username} Attachment 정보 수집 완료!\n")
        
        # API 제한 방지
        time.sleep(2)
    
    print("🎉 모든 사용자 Attachment 정보 수집 완료!")

if __name__ == "__main__":
    main()