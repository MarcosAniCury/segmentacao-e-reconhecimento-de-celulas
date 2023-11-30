from src.singleton.cells_singleton import CellListSingleton

from src.utils.image_utils import ImageUtils
from src.utils.os_utils import OSUtils

from PIL import Image


class ImagePreProcessor:

    @staticmethod
    def divide_cell_per_calls():
        cells = CellListSingleton()
        for cell in cells.shared_list:
            image_path = f"assets/images/{cell.image_filename}"
            if not OSUtils.exist_file(image_path):
                continue
            folder_path = f"assets/cropped_images/{cell.bethesda_system.value}"
            cropped_image = ImageUtils.crop_image(image_path, cell.nucleus_x, cell.nucleus_y)
            OSUtils.mkdir(folder_path)
            cropped_image.save(f"{folder_path}/{str(cell.cell_id)}.png")
