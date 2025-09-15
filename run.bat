@echo off
chcp 65001 > nul
echo ================================
echo    로블록스 아바타 다운로더
echo ================================
echo.

echo 사용할 프로그램을 선택하세요:
echo 1. 메인 다운로더 (2D + 3D 통합)
echo 2. 3D 모델 전용 다운로더
echo 3. 유저명 → ID 변환기
echo 4. 사용 예시 실행
echo 5. 테스트 실행
echo.

set /p choice="선택 (1-5): "

if "%choice%"=="1" (
    echo.
    echo 메인 다운로더를 실행합니다...
    python roblox_avatar_downloader.py
) else if "%choice%"=="2" (
    echo.
    echo 3D 모델 전용 다운로더를 실행합니다...
    python real_3d_downloader.py
) else if "%choice%"=="3" (
    echo.
    echo 유저명 → ID 변환기를 실행합니다...
    python username_to_id.py
) else if "%choice%"=="4" (
    echo.
    echo 사용 예시를 실행합니다...
    python examples.py
) else if "%choice%"=="5" (
    echo.
    echo 테스트를 실행합니다...
    python test_real_3d.py
) else (
    echo 잘못된 선택입니다.
)

echo.
pause
