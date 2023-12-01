import os
import shutil


class OSUtils:
    project_root = f"{os.path.abspath('')}/"

    @staticmethod
    def mkdir(folder_path):
        if not os.path.exists(f"{OSUtils.project_root}{folder_path}"):
            os.makedirs(folder_path)

    @staticmethod
    def mv(file_path, folder_destiny_path):
        shutil.move(f"{OSUtils.project_root}{file_path}", f"{OSUtils.project_root}{folder_destiny_path}")

    @staticmethod
    def rm(folder_path):
        os.remove(f"{OSUtils.project_root}{folder_path}")

    @staticmethod
    def exist_file(file_path):
        return os.path.exists(f"{OSUtils.project_root}{file_path}")

    @staticmethod
    def get_files_in_folder(folder_path):
        return os.listdir(f"{OSUtils.project_root}{folder_path}")
