from src.utils.csv_utils import read_csv
from src.controller.image_preprocessor import ImagePreProcessor
from src.utils.os_utils import OSUtils

import os

CSV_FILE_PATH = os.path.join(OSUtils.project_root, 'assets', 'classifications.csv')

read_csv(CSV_FILE_PATH)

ImagePreProcessor.classification_cells()




