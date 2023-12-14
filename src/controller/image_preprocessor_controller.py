from src.singleton.cells_singleton import CellListSingleton
from src.utils.image_utils import ImageUtils
from src.utils.os_utils import OSUtils
import os


class ImagePreProcessorController:
    @staticmethod
    def crop_image_per_cell(folder_path, folder_destiny, crop_size = 100):
        cells = CellListSingleton()
        OSUtils.mkdir(folder_destiny)
        for cell in cells.shared_list:
            image_path = os.path.join(folder_path, cell.image_filename)
            if not OSUtils.exist_file(image_path):
                continue
            cropped_image = ImageUtils.crop_image(image_path, cell.nucleus_x, cell.nucleus_y, crop_size)
            cropped_image.save(os.path.join(folder_destiny, f"{str(cell.cell_id)}.png"))