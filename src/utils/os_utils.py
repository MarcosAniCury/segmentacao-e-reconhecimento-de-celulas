import os
import shutil


class OSUtils:
    project_root = os.path.join(os.path.abspath(''), 'src')

    @staticmethod
    def mkdir(folder_path):
        if not os.path.exists(os.path.join(OSUtils.project_root, folder_path)):
            os.makedirs(folder_path)

    @staticmethod
    def mv(file_path, folder_destiny_path):
        shutil.move(os.path.join(OSUtils.project_root, file_path),
                    os.path.join(OSUtils.project_root, folder_destiny_path))

    @staticmethod
    def exist_file(file_path):
        return os.path.exists(os.path.join(OSUtils.project_root, file_path))

    @staticmethod
    def get_files_in_folder(folder_path):
        return os.listdir(os.path.join(OSUtils.project_root, folder_path))
