from src.enums.cell_enums import BethesdaSystemEnum
from typing import List


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

        if self.nucleus_x < 1 or self.nucleus_x > 1384:
            raise Exception("nucleus_x is not inside 1 and 1384 pixels")
        if self.nucleus_y < 1 or self.nucleus_y > 1384:
            raise Exception("nucleus_y is not inside 1 and 1384 pixels")

    def __str__(self):
        return (f"Cell:{self.cell_id}\nBethesda System:"
                f"{self.bethesda_system}\nNucleus X:{self.nucleus_x}\nNucleus Y:{self.nucleus_y}\n\n")


class CellListSingleton(object):
    _instance = None
    shared_list: List[Cell] = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CellListSingleton, cls).__new__(cls)
        return cls._instance

    def append(self, cell):
        self.shared_list.append(cell)
