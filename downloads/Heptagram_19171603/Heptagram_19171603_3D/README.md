# 3D 아바타 모델 사용법

## 📁 다운로드된 파일들
- `avatar.obj`: 3D 메시 파일 (Wavefront OBJ 형식)
- `avatar.mtl`: 재질 정보 파일
- `textures/`: 텍스처 이미지들
- `metadata.json`: 전체 메타데이터
- `README.md`: 이 사용법 파일

## 🎮 유저 정보
- **이름**: Heptagram (@Heptagram)
- **유저 ID**: 19171603
- **가입일**: 2011-08-13T12:13:48.247Z
- **다운로드 시간**: 2025-09-17 12:00:45

## 📐 모델 정보
- **카메라 위치**: {'x': -2.45812, 'y': 105.191, 'z': -5.06441}
- **카메라 FOV**: 70.0
- **바운딩 박스**: {'x': -2.0, 'y': 100.01, 'z': -0.984416} ~ {'x': 2.0, 'y': 105.482, 'z': 0.654225}

## 🛠️ 사용 방법

### Blender에서 사용하기
1. Blender를 실행합니다
2. File > Import > Wavefront (.obj) 선택
3. `avatar.obj` 파일을 선택하여 임포트
4. 재질이 자동으로 적용됩니다

### Unity에서 사용하기
1. Unity 프로젝트의 Assets 폴더에 모든 파일을 복사
2. `avatar.obj` 파일을 씬에 드래그
3. 필요시 텍스처를 수동으로 재질에 적용

### Maya에서 사용하기
1. Maya를 실행합니다
2. File > Import > 선택하고 OBJ 형식 설정
3. `avatar.obj` 파일을 임포트

### Three.js/Web에서 사용하기
```javascript
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader.js';

const mtlLoader = new MTLLoader();
mtlLoader.load('avatar.mtl', (materials) => {
    materials.preload();
    
    const objLoader = new OBJLoader();
    objLoader.setMaterials(materials);
    objLoader.load('avatar.obj', (object) => {
        scene.add(object);
    });
});
```

## ⚠️ 주의사항
- 이 모델은 로블록스의 R15 또는 R6 형식입니다
- 상업적 사용 시 로블록스 이용약관을 준수해야 합니다
- 텍스처가 투명하게 보일 경우 알파 채널을 비활성화하세요

## 🔧 문제 해결
- **텍스처가 안 보임**: MTL 파일에서 텍스처 경로를 확인하세요
- **모델이 투명함**: 재질의 투명도 설정을 확인하세요
- **크기가 이상함**: 로블록스는 스터드 단위를 사용합니다 (1 스터드 ≈ 0.28m)

다운로드 도구: Roblox Avatar 3D Downloader
