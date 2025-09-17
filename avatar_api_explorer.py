#!/usr/bin/env python3
"""
Roblox 아바타 관련 추가 API 정보 수집기
"""

import requests
import json
from pathlib import Path
import time

class RobloxAvatarAPIExplorer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def get_user_avatar_info(self, user_id: int) -> dict:
        """사용자 아바타 전체 정보 수집"""
        print(f"🔍 사용자 ID {user_id}의 아바타 관련 정보 수집 중...")
        
        all_info = {
            "user_id": user_id,
            "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "api_responses": {}
        }
        
        # 1. 기본 사용자 정보
        print("   📋 기본 사용자 정보...")
        try:
            response = self.session.get(f"https://users.roblox.com/v1/users/{user_id}")
            if response.status_code == 200:
                all_info["api_responses"]["user_info"] = response.json()
                print(f"   ✅ 기본 정보 수집 완료")
            else:
                print(f"   ❌ 기본 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 기본 정보 오류: {e}")
            
        # 2. 아바타 구성 정보 (가장 상세한 정보)
        print("   👤 아바타 구성 정보...")
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/avatar")
            if response.status_code == 200:
                all_info["api_responses"]["avatar_config"] = response.json()
                print(f"   ✅ 아바타 구성 정보 수집 완료")
            else:
                print(f"   ❌ 아바타 구성 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 아바타 구성 오류: {e}")
            
        # 3. 현재 착용 중인 아바타 아이템들
        print("   🎽 착용 아이템 정보...")
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing")
            if response.status_code == 200:
                all_info["api_responses"]["currently_wearing"] = response.json()
                print(f"   ✅ 착용 아이템 정보 수집 완료")
            else:
                print(f"   ❌ 착용 아이템 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 착용 아이템 오류: {e}")
            
        # 4. 아바타 색상 정보
        print("   🎨 아바타 색상 정보...")
        try:
            response = self.session.get(f"https://avatar.roblox.com/v1/users/{user_id}/avatar")
            if response.status_code == 200:
                avatar_data = response.json()
                if "bodyColors" in avatar_data:
                    all_info["api_responses"]["body_colors"] = avatar_data["bodyColors"]
                    print(f"   ✅ 색상 정보 수집 완료")
        except Exception as e:
            print(f"   ❌ 색상 정보 오류: {e}")
            
        # 5. 3D 아바타 메타데이터 (기존)
        print("   🎯 3D 아바타 메타데이터...")
        try:
            response = self.session.get(f"https://thumbnails.roblox.com/v1/users/avatar-3d?userIds={user_id}&format=Obj&size=768x432")
            if response.status_code == 200:
                all_info["api_responses"]["avatar_3d"] = response.json()
                print(f"   ✅ 3D 메타데이터 수집 완료")
            else:
                print(f"   ❌ 3D 메타데이터 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 3D 메타데이터 오류: {e}")
            
        # 6. 다양한 썸네일 정보
        print("   📸 썸네일 정보...")
        thumbnail_types = [
            ("headshot", "HeadShot"),
            ("bust", "Bust"), 
            ("full_body", "FullBody")
        ]
        
        all_info["api_responses"]["thumbnails"] = {}
        for thumb_key, thumb_type in thumbnail_types:
            try:
                response = self.session.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=720x720&format=Png&isCircular=false")
                if response.status_code == 200:
                    all_info["api_responses"]["thumbnails"][thumb_key] = response.json()
                    print(f"   ✅ {thumb_type} 썸네일 수집 완료")
            except Exception as e:
                print(f"   ❌ {thumb_type} 썸네일 오류: {e}")
                
        # 7. 사용자 게임 정보 (public games)
        print("   🎮 게임 정보...")
        try:
            response = self.session.get(f"https://games.roblox.com/v2/users/{user_id}/games?accessFilter=Public&limit=10")
            if response.status_code == 200:
                all_info["api_responses"]["games"] = response.json()
                print(f"   ✅ 게임 정보 수집 완료")
            else:
                print(f"   ❌ 게임 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 게임 정보 오류: {e}")
            
        # 8. 그룹 정보
        print("   👥 그룹 정보...")
        try:
            response = self.session.get(f"https://groups.roblox.com/v2/users/{user_id}/groups/roles")
            if response.status_code == 200:
                all_info["api_responses"]["groups"] = response.json()
                print(f"   ✅ 그룹 정보 수집 완료")
            else:
                print(f"   ❌ 그룹 정보 실패: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 그룹 정보 오류: {e}")
            
        return all_info
    
    def save_extended_info(self, user_id: int, info: dict, output_dir: str = "extended_avatar_info"):
        """확장된 아바타 정보 저장"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 사용자명 가져오기
        username = "unknown"
        if "user_info" in info["api_responses"]:
            username = info["api_responses"]["user_info"].get("name", "unknown")
        
        # JSON 파일로 저장
        filename = f"{username}_{user_id}_extended_info.json"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
            
        print(f"📁 확장 정보 저장: {filepath}")
        
        # 요약 리포트 생성
        self.generate_summary_report(info, output_path / f"{username}_{user_id}_summary.md")
        
    def generate_summary_report(self, info: dict, filepath: Path):
        """요약 리포트 생성"""
        user_id = info["user_id"]
        
        # 사용자 기본 정보
        user_info = info["api_responses"].get("user_info", {})
        username = user_info.get("name", "Unknown")
        display_name = user_info.get("displayName", username)
        
        # 아바타 구성 정보
        avatar_config = info["api_responses"].get("avatar_config", {})
        
        report = f"""# {display_name} (@{username}) - 아바타 정보 리포트

## 📋 기본 정보
- **사용자 ID**: {user_id}
- **사용자명**: {username}
- **표시명**: {display_name}
- **생성일**: {user_info.get('created', 'N/A')}
- **인증 배지**: {'✅' if user_info.get('hasVerifiedBadge') else '❌'}
- **밴 상태**: {'⚠️ 밴됨' if user_info.get('isBanned') else '✅ 정상'}

## 👤 아바타 구성
"""
        
        if avatar_config:
            # 바디 타입
            if "playerAvatarType" in avatar_config:
                avatar_type = avatar_config["playerAvatarType"]
                report += f"- **아바타 타입**: {avatar_type}\n"
                
            # 스케일 정보
            if "scales" in avatar_config:
                scales = avatar_config["scales"]
                report += f"- **스케일**:\n"
                for scale_type, value in scales.items():
                    report += f"  - {scale_type}: {value}\n"
                    
            # 바디 색상
            if "bodyColors" in avatar_config:
                colors = avatar_config["bodyColors"]
                report += f"- **바디 색상**:\n"
                for part, color_id in colors.items():
                    report += f"  - {part}: {color_id}\n"
        
        # 착용 아이템
        wearing = info["api_responses"].get("currently_wearing", {})
        if wearing and "assetIds" in wearing:
            items = wearing["assetIds"]
            report += f"\n## 🎽 착용 아이템 ({len(items)}개)\n"
            for item_id in items[:10]:  # 처음 10개만
                report += f"- Asset ID: {item_id}\n"
            if len(items) > 10:
                report += f"- ... 그리고 {len(items) - 10}개 더\n"
        
        # 3D 정보
        avatar_3d = info["api_responses"].get("avatar_3d", {})
        if avatar_3d and "data" in avatar_3d:
            report += f"\n## 🎯 3D 모델 정보\n"
            for data in avatar_3d["data"]:
                if "imageUrl" in data:
                    report += f"- **3D 모델 URL**: {data['imageUrl']}\n"
        
        # 게임 정보
        games = info["api_responses"].get("games", {})
        if games and "data" in games:
            game_count = len(games["data"])
            report += f"\n## 🎮 공개 게임 ({game_count}개)\n"
            for game in games["data"][:5]:  # 처음 5개만
                name = game.get("name", "Untitled")
                plays = game.get("placeVisits", 0)
                report += f"- **{name}**: {plays:,} 플레이\n"
        
        # 그룹 정보
        groups = info["api_responses"].get("groups", {})
        if groups and "data" in groups:
            group_count = len(groups["data"])
            report += f"\n## 👥 소속 그룹 ({group_count}개)\n"
            for group_data in groups["data"][:5]:  # 처음 5개만
                group = group_data.get("group", {})
                role = group_data.get("role", {})
                group_name = group.get("name", "Unknown Group")
                role_name = role.get("name", "Member")
                report += f"- **{group_name}**: {role_name}\n"
        
        report += f"\n---\n*리포트 생성 시간: {info['collected_at']}*\n"
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"📄 요약 리포트 생성: {filepath}")

def main():
    print("=== Roblox 아바타 확장 정보 수집기 ===\n")
    
    explorer = RobloxAvatarAPIExplorer()
    
    # 테스트할 사용자들
    test_users = [
        ("ddotty", 48232800),  # 현재 보고 있는 사용자
        ("Roblox", 1),         # 로블록스 공식 계정
        ("builderman", 156)    # 빌더맨
    ]
    
    for username, user_id in test_users:
        print(f"\n{'='*50}")
        print(f"🎯 {username} (ID: {user_id}) 정보 수집 시작")
        print(f"{'='*50}")
        
        # 정보 수집
        extended_info = explorer.get_user_avatar_info(user_id)
        
        # 저장
        explorer.save_extended_info(user_id, extended_info)
        
        print(f"✅ {username} 정보 수집 완료!\n")
        
        # API 제한 방지
        time.sleep(2)
    
    print("🎉 모든 사용자 확장 정보 수집 완료!")

if __name__ == "__main__":
    main()