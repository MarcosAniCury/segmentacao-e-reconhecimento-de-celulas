from src.controller.image_classification import ImageClassification
from src.controller.image_preprocessor import ImagePreProcessor
from src.controller.image_descriptor import ImageDescriptor
from src.controller.image_segment import ImageSegment
from src.utils.csv_utils import read_csv
from src.utils.os_utils import OSUtils
import os

# TODO: trocar essa variável pelo input
CSV_FILE_PATH = os.path.join(OSUtils.project_images_root, 'classifications.csv')
# TODO: trocar esse variável pelo input
INPUT_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'images')
SEGMENTED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'segmented_images')
CROPPED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'cropped_images')
CLASSIFIED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'classified_images')

print("Segment Image")
ImageSegment.segment_images(INPUT_IMAGES_PATH, SEGMENTED_IMAGES_PATH)

print("Read CSV")
read_csv(CSV_FILE_PATH)

print("Crop Image")
ImagePreProcessor.crop_image_per_cell(SEGMENTED_IMAGES_PATH, CROPPED_IMAGES_PATH)

print("Descript Image")
ImageDescriptor.descript_images(CROPPED_IMAGES_PATH)

print("Classification Image")
ImageClassification.classify_images(CROPPED_IMAGES_PATH, CLASSIFIED_IMAGES_PATH)
