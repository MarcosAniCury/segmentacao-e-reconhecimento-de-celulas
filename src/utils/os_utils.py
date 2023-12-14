import os
import shutil


class OSUtils:
    project_root = os.path.join(os.path.abspath('src'))
    project_images_root = os.path.join(project_root, 'assets')

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

    @staticmethod
    def touch(file_path):
        open(file_path, 'w').close()

    @staticmethod
    def write_row_in_file(file_path, row):
        with open(file_path, 'a') as file:
            file.write(row + '\n')
