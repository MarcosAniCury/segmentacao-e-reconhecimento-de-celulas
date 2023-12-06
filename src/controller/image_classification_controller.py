from src.singleton.cells_singleton import CellListSingleton
from src.enums.cell_enums import BethesdaSystemEnum
from src.utils.os_utils import OSUtils
import os


class ImageClassificationController:

    @staticmethod
    def __create_folders(folder_cells_classification_path):
        OSUtils.mkdir(folder_cells_classification_path)
        for bethesda_system in BethesdaSystemEnum:
            folder_cell_classification_path = os.path.join(folder_cells_classification_path, bethesda_system.name)
            OSUtils.mkdir(folder_cell_classification_path)

    @staticmethod
    def classify_images(CROPPED_IMAGES_PATH, CLASSIFIED_IMAGES_PATH):
        cells = CellListSingleton()
        images_cells_path = OSUtils.get_files_in_folder(CROPPED_IMAGES_PATH)
        ImageClassificationController.__create_folders(CLASSIFIED_IMAGES_PATH)

        for image_cell_path in images_cells_path:
            file_path = os.path.join(CROPPED_IMAGES_PATH, image_cell_path)
            cell_id = int(image_cell_path.split(".")[0])
            cell_bethesda_system = [cell_filter.bethesda_system for cell_filter in cells.shared_list
                                    if cell_filter.cell_id == cell_id][0]
            folder_cell_classification_path = os.path.join(CLASSIFIED_IMAGES_PATH, cell_bethesda_system.name)
            OSUtils.mv(file_path, folder_cell_classification_path)
