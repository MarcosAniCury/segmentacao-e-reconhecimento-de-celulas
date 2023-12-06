from src.enums.cell_enums import BethesdaSystemEnum
from src.utils.image_utils import ImageUtils
from src.controller.image_descriptor import ImageDescriptor
from typing import List
import sys


class Cell:
    def __init__(self, image_id, image_filename, image_doi, cell_id,
                 bethesda_system, nucleus_x, nucleus_y):
        self.image_id = int(image_id)
        self.image_filename = image_filename
        self.image_doi = image_doi
        self.cell_id = int(cell_id)
        bethesda_system = bethesda_system.split(' ')[0].upper().replace('-', '_')

        try:
            self.bethesda_system = BethesdaSystemEnum[bethesda_system]
        except KeyError:
            raise Exception("bethesda_system is not inside possibilities class")

        self.nucleus_x = int(nucleus_x)
        self.nucleus_y = int(nucleus_y)
        self.centroid = None
        self.chain_code = None
        self.distance_nucleus = None

        if self.nucleus_x < 1 or self.nucleus_x > 1384:
            raise Exception("nucleus_x is not inside 1 and 1384 pixels")
        if self.nucleus_y < 1 or self.nucleus_y > 1384:
            raise Exception("nucleus_y is not inside 1 and 1384 pixels")

    def __str__(self):
        return (f"Cell:{self.cell_id}\nBethesda System:"
                f"{self.bethesda_system}\nNucleus X:{self.nucleus_x}\nNucleus Y:{self.nucleus_y}\n\n")

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.cell_id == other.cell_id
        else:
            return self.cell_id == other


class CellListSingleton(object):
    _instance = None
    shared_list: List[Cell] = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CellListSingleton, cls).__new__(cls)
        return cls._instance

    def append(self, cell):
        self.shared_list.append(cell)

    def find_cell_id(self, cell_id):
        return [cell for cell in self.shared_list if cell.cell_id == cell_id][0]

    def find_cells_based_in_image(self, image_name):
        return [cell for cell in self.shared_list if cell.image_filename == image_name]

    def insert_centroid_in_cell(self, contour, image_name):
        centroid_contour = ImageDescriptor.calculate_centroid(contour)
        cells_inside_image = self.find_cells_based_in_image(image_name)
        best_cell_distance_centroid = sys.float_info.max
        best_cell = None
        for cell in cells_inside_image:
            point = (cell.nucleus_x, cell.nucleus_y)
            cell_point_distance_centroid = ImageUtils.calculate_distance(point, centroid_contour)
            if cell_point_distance_centroid < best_cell_distance_centroid:
                best_cell_distance_centroid = cell_point_distance_centroid
                best_cell = cell
        if best_cell is not None:
            best_cell.centroid = centroid_contour


