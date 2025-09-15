# Roblox Avatar Downloader

로블록스 API를 사용하여 유저의 아바타와 썸네일 이미지, **실제 3D 모델**을 다운로드하는 파이썬 스크립트입니다.

## 기능

### 🖼️ 2D 이미지 다운로드
- 🎭 **전신 아바타 다운로드**: 유저의 전체 아바타 이미지
- 👤 **헤드샷 다운로드**: 유저의 얼굴/머리 부분 이미지  
- 👔 **흉상 다운로드**: 유저의 상반신 이미지
- 📏 **다양한 크기 지원**: 30x30부터 720x720까지 다양한 해상도

### 🎯 **3D 모델 다운로드 (NEW!)**
- 📦 **실제 OBJ 파일**: Blender, Maya, Unity에서 바로 사용 가능
- 🎨 **MTL 재질 파일**: 완전한 재질 정보 포함
- 🖼️ **텍스처 파일들**: 고품질 3D 텍스처 이미지
- 🔧 **최신 API 사용**: 2024년 업데이트된 로블록스 3D Avatar API

### 👥 **일반 기능**
- 👥 **다중 유저 지원**: 여러 유저의 아바타를 한 번에 다운로드
- 📁 **자동 폴더 정리**: 유저별로 폴더를 생성하여 체계적으로 관리
- 📄 **유저 정보 저장**: 유저의 상세 정보를 JSON 파일로 저장

## 설치

1. **저장소 클론**
   ```bash
   git clone <repository-url>
   cd Roblox-hook
   ```

2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

## 사용법

### 기본 실행
```bash
python roblox_avatar_downloader.py
```

실행하면 다음과 같은 옵션을 선택할 수 있습니다:
1. 단일 유저 다운로드 (2D 이미지만)
2. 단일 유저 다운로드 (2D + 실제 3D 모델)
3. 단일 유저 다운로드 (2D + 실제 3D + 텍스처)
4. 여러 유저 다운로드
5. 예시 실행 (3D 모델 포함)

### 🎯 3D 모델 전용 다운로드
```bash
python real_3d_downloader.py
```

### 🆔 유저명으로 ID 찾기
```bash
python username_to_id.py
```

### 코드에서 직접 사용

```python
from roblox_avatar_downloader import RobloxAvatarDownloader

# 다운로더 객체 생성
downloader = RobloxAvatarDownloader("my_downloads")

# 단일 유저 다운로드
user_id = 1  # Roblox 창시자
sizes = ["150x150", "420x420", "720x720"]
downloader.download_user_avatars(user_id, sizes)

# 여러 유저 다운로드
user_ids = [1, 2, 3, 156]
downloader.download_multiple_users(user_ids, sizes)
```

## 지원하는 이미지 크기

- `30x30`
- `48x48` 
- `60x60`
- `75x75`
- `100x100`
- `110x110`
- `140x140`
- `150x150`
- `180x180`
- `352x352`
- `420x420`
- `720x720`

## 다운로드 폴더 구조

### 2D + 3D 통합 다운로드
```
downloads/
├── username_12345/
│   ├── user_info.json           # 유저 상세 정보
│   ├── avatar_150x150.png       # 전신 아바타 (150x150)
│   ├── avatar_420x420.png       # 전신 아바타 (420x420)
│   ├── headshot_150x150.png     # 헤드샷 (150x150)
│   ├── headshot_420x420.png     # 헤드샷 (420x420)
│   ├── bust_150x150.png         # 흉상 (150x150)
│   ├── bust_420x420.png         # 흉상 (420x420)
│   └── username_12345_3D/       # 3D 모델 폴더
│       ├── avatar.obj           # 3D 메시 파일
│       ├── avatar.mtl           # 재질 정보
│       ├── textures/            # 텍스처 이미지들
│       │   ├── texture_001.png
│       │   └── texture_002.png
│       ├── metadata.json        # 3D 메타데이터
│       └── README.md            # 3D 사용법
└── another_user_67890/
    └── ...
```

### 3D 전용 다운로드
```
real_3d_avatars/
├── username_12345_3D/
│   ├── avatar.obj               # 3D 메시 파일 (Wavefront OBJ)
│   ├── avatar.mtl               # 재질 정보 파일
│   ├── textures/                # 텍스처 이미지들
│   │   ├── texture_001.png
│   │   ├── texture_002.png
│   │   └── ...
│   ├── metadata.json            # 전체 메타데이터
│   └── README.md                # 사용법 안내
└── ...
```

## 주요 클래스와 메서드

### RobloxAvatarDownloader

#### 초기화
```python
RobloxAvatarDownloader(download_folder="downloads")
```

#### 주요 메서드

- `get_user_info(user_id)`: 유저 정보 가져오기
- `get_user_avatar_thumbnails(user_id, size)`: 전신 아바타 썸네일 URL 가져오기
- `get_user_headshot_thumbnails(user_id, size)`: 헤드샷 썸네일 URL 가져오기  
- `get_user_bust_thumbnails(user_id, size)`: 흉상 썸네일 URL 가져오기
- `download_user_avatars(user_id, sizes)`: 단일 유저의 모든 아바타 다운로드
- `download_multiple_users(user_ids, sizes)`: 여러 유저의 아바타 다운로드

## 유저 ID 찾는 방법

1. **웹사이트에서**: 로블록스 프로필 URL에서 숫자 부분
   - 예: `https://www.roblox.com/users/12345/profile` → ID는 `12345`

2. **API로**: 유저명으로 ID 찾기
   ```bash
   curl "https://users.roblox.com/v1/usernames/users" -X POST -H "Content-Type: application/json" -d '{"usernames":["username"]}'
   ```

## 예시

### 유명한 로블록스 유저들
- ID 1: Roblox (창시자)
- ID 2: John 
- ID 3: Jane
- ID 156: builderman

### 사용 예시
```python
# 고해상도로 여러 유저 다운로드
downloader = RobloxAvatarDownloader("high_quality_avatars")
user_ids = [1, 156]  # Roblox, builderman
sizes = ["420x420", "720x720"]
downloader.download_multiple_users(user_ids, sizes)
```

## 주의사항

- API 요청 제한을 피하기 위해 요청 간에 짧은 지연이 있습니다
- 일부 유저의 아바타가 비공개일 수 있습니다
- 네트워크 연결이 필요합니다
- 대용량 다운로드 시 충분한 저장 공간을 확보하세요

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요!
