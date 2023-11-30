import os


class OSUtils:
    project_root = f"{os.path.abspath('')}/"

    @staticmethod
    def mkdir(folder_path):
        if not os.path.exists(f"{OSUtils.project_root}{folder_path}"):
            os.makedirs(folder_path)

    @staticmethod
    def exist_file(file_path):
        return os.path.exists(f"{OSUtils.project_root}{file_path}")
