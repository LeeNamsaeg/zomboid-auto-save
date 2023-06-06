import os
import shutil
import zipfile
import time

def validate_folder_path(folder_path):
    if not os.path.exists(folder_path):
        print("폴더가 존재하지 않습니다.")

        return False

    if not os.path.isdir(folder_path):
        print("폴더가 아닙니다.")

        return False

    if not os.access(folder_path, os.R_OK):
        print("읽기 권한이 없습니다")

        return False

    return True

def save_folder_path_to_file(folder_path):
    if not validate_folder_path(folder_path):
        return False

    with open('save_file.txt', 'w') as file:
        file.write(folder_path)

    return True

def get_save_folder_path_from_file():
    with open('save_file.txt', 'r') as file:
        contents = file.read()

        return contents

def zip_folder(folder_path):
    with zipfile.ZipFile('Saves.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    print("세이브 파일을 복제하였습니다.")

def extract_zip_file(folder_path):
    with zipfile.ZipFile(folder_path + '.zip', 'r') as zip_ref:
        zip_ref.extractall(folder_path)

    os.remove(folder_path + '.zip')

def auto_save_mode():
    save_folder_path = get_save_folder_path_from_file()

    if save_folder_path == '':
        while True:
            print("""
                세이브 파일을 먼저 입력해주세요 : 
            """)

            folder_path = input()

            if validate_folder_path(folder_path):
                save_folder_path_to_file(folder_path)

                break

    while True:
        zip_folder(save_folder_path)

        time.sleep(60)

def replace_save_folder(folder_path):
    if not validate_folder_path(folder_path):
        return False

    shutil.rmtree(folder_path)

    shutil.copy2('Saves.zip', folder_path[:-5])

def load_save_file():
    save_folder_path = get_save_folder_path_from_file()

    if save_folder_path == '':
        return False

    replace_save_folder(save_folder_path)

    extract_zip_file(save_folder_path)

while True:
    print("""
        좀보이드 세이브 파일 자동 복제기입니다.
        
        1. 자동 복제기 시작
        2. 세이브 파일 로드 (!주의 - 좀보이드 메인화면으로 나와서 해주세요)
        => 
    """)

    cmd = input()

    if cmd == '1':
        auto_save_mode()

    elif cmd == '2':
        load_save_file()

    else:
        continue