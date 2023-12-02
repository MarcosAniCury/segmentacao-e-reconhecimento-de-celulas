from src.utils.csv_utils import read_csv
from src.controller.image_preprocessor import ImagePreProcessor
from src.controller.image_segment import ImageSegment
from src.controller.image_descriptor import ImageDescriptor
from src.utils.os_utils import OSUtils

import os
import cv2

#CSV_FILE_PATH = os.path.join(OSUtils.project_root, 'assets', 'classifications.csv')

#read_csv(CSV_FILE_PATH)

#
ImagePreProcessor.crop_image_per_cell()

#ImagePreProcessor.classification_cells()

image_path = os.path.join(OSUtils.project_root, 'assets', 'cells_classification_images', 'LSIL', '7.png')
segmented_image = ImageSegment.segment_image(image_path)
original_image = cv2.imread(image_path)

# Extraindo o contorno da forma
contour = ImageDescriptor.extract_shape_contour(segmented_image)

# Reconstruindo a imagem
reconstructed_image = ImageDescriptor.reconstruct_image_contour(contour, original_image.shape)

# Exibir a imagem original, a imagem segmentada e a imagem reconstruída
cv2.imshow("Original Image", original_image)
cv2.imshow("Segmented Image", segmented_image)
cv2.imshow("Reconstructed Image", reconstructed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()