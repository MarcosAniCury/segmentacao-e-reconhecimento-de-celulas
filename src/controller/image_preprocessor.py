from src.singleton.cells_singleton import CellListSingleton
from src.utils.image_utils import ImageUtils
from src.utils.os_utils import OSUtils
from src.enums.cell_enums import BethesdaSystemEnum

import os


class ImagePreProcessor:
    @staticmethod
    def crop_image_per_cell():
        cells = CellListSingleton()
        folder_path = os.path.join(OSUtils.project_root, 'assets', 'cells_images')
        OSUtils.mkdir(folder_path)
        for cell in cells.shared_list:
            image_path = os.path.join('assets', 'images', cell.image_filename)
            if not OSUtils.exist_file(image_path):
                continue
            cropped_image = ImageUtils.crop_image(image_path, cell.nucleus_x, cell.nucleus_y)
            cropped_image.save(os.path.join(folder_path, f"{str(cell.cell_id)}.png"))

    @staticmethod
    def __create_folders(folder_cells_classification_path):
        OSUtils.mkdir(folder_cells_classification_path)
        for bethesda_system in BethesdaSystemEnum:
            folder_cell_classification_path = os.path.join(folder_cells_classification_path, bethesda_system.name)
            OSUtils.mkdir(folder_cell_classification_path)

    @staticmethod
    def classification_cells():
        cells = CellListSingleton()
        folder_cells_path = os.path.join('assets', 'cells_images')
        folder_cells_classification_path = os.path.join(OSUtils.project_root, 'assets', 'cells_classification_images')
        images_cells_path = OSUtils.get_files_in_folder(folder_cells_path)
        ImagePreProcessor.__create_folders(folder_cells_classification_path)

        for image_cell_path in images_cells_path:
            file_path = os.path.join(folder_cells_path, image_cell_path)
            cell_id = int(image_cell_path.split(".")[0])
            cell_bethesda_system = [cell_filter.bethesda_system for cell_filter in cells.shared_list
                                    if cell_filter.cell_id == cell_id][0]
            folder_cell_classification_path = os.path.join(folder_cells_classification_path, cell_bethesda_system.name)
            OSUtils.mv(file_path, folder_cell_classification_path)
