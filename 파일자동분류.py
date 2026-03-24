import os
import shutil
from pathlib import Path

# 다운로드 폴더 경로
DOWNLOAD_FOLDER = r"C:\Users\student\Downloads"

# 파일 분류 규칙: {폴더명: [확장자들]}
FILE_CATEGORIES = {
    "images": [".jpg", ".jpeg"],
    "data": [".csv", ".xlsx"],
    "docs": [".txt", ".doc", ".pdf"],
    "archive": [".zip"]
}

def create_folders(base_path):
    """분류 폴더가 없으면 생성"""
    for folder_name in FILE_CATEGORIES.keys():
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"📁 폴더 생성: {folder_path}")

def get_category_folder(file_extension):
    """파일 확장자에 맞는 폴더명 반환"""
    file_extension = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    return None

def move_files_by_category(source_folder):
    """다운로드 폴더의 파일을 카테고리별로 이동"""
    if not os.path.exists(source_folder):
        print(f"❌ 폴더를 찾을 수 없습니다: {source_folder}")
        return
    
    # 먼저 필요한 폴더 생성
    create_folders(source_folder)
    
    moved_count = 0
    
    # 다운로드 폴더의 모든 파일 순회
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        
        # 폴더는 제외
        if os.path.isdir(file_path):
            continue
        
        # 파일 확장자 추출
        file_extension = os.path.splitext(filename)[1]
        
        # 분류 폴더 찾기
        category = get_category_folder(file_extension)
        
        if category:
            # 목표 폴더 경로
            destination_folder = os.path.join(source_folder, category)
            destination_path = os.path.join(destination_folder, filename)
            
            try:
                # 파일 이동
                shutil.move(file_path, destination_path)
                print(f"✓ 이동: {filename} → {category}/")
                moved_count += 1
            except Exception as e:
                print(f"✗ 오류: {filename} 이동 실패 - {e}")
        else:
            print(f"⚠ 미분류: {filename} (지원하지 않는 확장자)")
    
    print(f"\n✅ 총 {moved_count}개 파일이 이동되었습니다.")

if __name__ == "__main__":
    print(f"📂 다운로드 폴더 자동 분류 시작: {DOWNLOAD_FOLDER}\n")
    move_files_by_category(DOWNLOAD_FOLDER)
    print("\n분류 완료!")
