from src.utils.csv_utils import read_csv
from src.controller.image_preprocessor import ImagePreProcessor

CSV_FILE_PATH = "assets/classifications.csv"

read_csv(CSV_FILE_PATH)

ImagePreProcessor.divide_cell_per_calls()




