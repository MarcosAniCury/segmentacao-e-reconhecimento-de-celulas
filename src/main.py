from src.controller.image_classification_controller import ImageClassificationController
from src.controller.image_preprocessor_controller import ImagePreProcessorController
from src.controller.image_descriptor_controller import ImageDescriptorController
from src.controller.image_segment_controller import ImageSegmentController
from src.controller.scatterplot_controller import ScatterplotController
from src.utils.scatterplot_utils import format_items_to_scatterplot_pattern
from src.utils.csv_utils import read_csv
from src.utils.os_utils import OSUtils
import os

# TODO: trocar essa variável pelo input
CSV_FILE_PATH = os.path.join(OSUtils.project_images_root, 'classifications.csv')
# TODO: trocar esse variável pelo input
INPUT_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'images')
SCATTERPLOT_PATH = os.path.join(OSUtils.project_images_root, 'scatterplot.png')
CSV_CELLS_PATH = os.path.join(OSUtils.project_images_root, 'cells_characteristics.csv')
SEGMENTED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'segmented_images')
CROPPED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'cropped_images')
CLASSIFIED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'classified_images')

print("Read CSV")
read_csv(CSV_FILE_PATH)

print("Segment Image")
ImageSegmentController.segment_images(INPUT_IMAGES_PATH, SEGMENTED_IMAGES_PATH, CSV_CELLS_PATH)

print("Create Scatterplot")
ScatterplotController.generate_scatterplot(format_items_to_scatterplot_pattern(CSV_CELLS_PATH), SCATTERPLOT_PATH)

print("Crop Image")
ImagePreProcessorController.crop_image_per_cell(SEGMENTED_IMAGES_PATH, CROPPED_IMAGES_PATH)

print("Descript Image")
ImageDescriptorController.descript_images(CROPPED_IMAGES_PATH)

print("Classification Image")
ImageClassificationController.classify_images(CROPPED_IMAGES_PATH, CLASSIFIED_IMAGES_PATH)
