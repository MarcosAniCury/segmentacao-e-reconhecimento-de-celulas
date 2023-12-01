from src.singleton.cells_singleton import CellListSingleton

from src.utils.image_utils import ImageUtils
from src.utils.os_utils import OSUtils

from PIL import Image


class ImagePreProcessor:
    @staticmethod
    def crop_image_per_cell():
        cells = CellListSingleton()
        for cell in cells.shared_list:
            image_path = f"assets/images/{cell.image_filename}"
            if not OSUtils.exist_file(image_path):
                continue
            folder_path = f"assets/cells_images/"
            cropped_image = ImageUtils.crop_image(image_path, cell.nucleus_x, cell.nucleus_y)
            OSUtils.mkdir(folder_path)
            cropped_image.save(f"{folder_path}/{str(cell.cell_id)}.png")

    @staticmethod
    def classification_cells():
        cells = CellListSingleton()
        folder_cells_path = f"assets/cells_images/"
        folder_cells_classification_path = f"assets/cells_classification_images/"
        OSUtils.mkdir(folder_cells_classification_path)
        images_cells_path = OSUtils.get_files_in_folder(folder_cells_path)
        for image_cell_path in images_cells_path:
            file_path = f"{folder_cells_path}/{image_cell_path}"
            cell_id = int(image_cell_path.split(".")[0])
            cell_bethesda_system = [cell_filter.bethesda_system for cell_filter in cells.shared_list
                                    if cell_filter.cell_id == cell_id][0]
            folder_cell_classification_path = f"{folder_cells_classification_path}{cell_bethesda_system.value}"
            OSUtils.mkdir(folder_cell_classification_path)
            OSUtils.mv(file_path, folder_cell_classification_path)
