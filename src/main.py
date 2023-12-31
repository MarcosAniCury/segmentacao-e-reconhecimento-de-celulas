from src.controller.image_classification_controller import ImageClassificationController
from src.controller.image_preprocessor_controller import ImagePreProcessorController
from src.controller.image_descriptor_controller import ImageDescriptorController
from src.utils.mahalanobis_classifier_utils import prepare_data_to_train
from src.utils.scatterplot_utils import format_items_to_scatterplot_pattern
from src.controller.image_segment_controller import ImageSegmentController
from src.classifiers.malahnobis_classifier import MalahanobisClassifier
from src.controller.scatterplot_controller import ScatterplotController
from src.classifiers.resnet50_classifier import Restnet50Classifier
from src.utils.resnet_classifier_utils import setup_binary_classification_structure
from src.utils.csv_utils import read_csv
from src.utils.os_utils import OSUtils
import os

from src.view.screen.main_screen import MainScreen

# TODO: trocar essa variável pelo input
CSV_FILE_PATH = os.path.join(OSUtils.project_images_root, 'classifications.csv')
# TODO: trocar esse variável pelo input
INPUT_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'images')
SCATTERPLOT_PATH = os.path.join(OSUtils.project_images_root, 'scatterplot.png')
CSV_CELLS_PATH = os.path.join(OSUtils.project_images_root, 'cells_characteristics.csv')
SEGMENTED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'segmented_images')
CROPPED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'cropped_images')
CLASSIFIED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'classified_images')
TEST_TRAINING_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'test_training_images')
TEST_TRAINING_BINARY_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'test_training_images_binary')

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

print("Separate in test and training")
ImageClassificationController.set_training_and_test(TEST_TRAINING_IMAGES_PATH, CLASSIFIED_IMAGES_PATH)

malahanobis_classifier = MalahanobisClassifier()

print("Mahalanobis Distancie Classify Binary")
malahanobis_classifier.sklearn_classify(prepare_data_to_train(TEST_TRAINING_IMAGES_PATH))

print("Mahalanobis Distancie Classify Multiclass")
malahanobis_classifier.sklearn_classify(prepare_data_to_train(TEST_TRAINING_IMAGES_PATH, False))

# Instanciar a classe Restnet50Classifier
classifier_binary = Restnet50Classifier(train_data_path=os.path.join(TEST_TRAINING_BINARY_IMAGES_PATH, 'training'),
                                 test_data_path=os.path.join(TEST_TRAINING_BINARY_IMAGES_PATH, 'test'))

classifier_multiclass = Restnet50Classifier(train_data_path=os.path.join(TEST_TRAINING_IMAGES_PATH, 'training'),
                                 test_data_path=os.path.join(TEST_TRAINING_IMAGES_PATH, 'test'))

# Construir os modelos de rede neural
binary_model = classifier_binary.build_binary_model()
multiclass_model = classifier_multiclass.build_multiclass_model(num_classes=6)  # Assumindo que temos 6 classes

setup_binary_classification_structure(OSUtils.project_images_root, 'test_training_images', 'test_training_images_binary')

# Treinar os modelos e avaliar
print("Training Binary Model")
history_binary, cm_test_binary, accuracy_test_binary = classifier_binary.train_model(binary_model, class_mode='binary')

print("Training Multiclass Model")
history_multiclass, cm_test_multiclass, accuracy_test_multiclass = classifier_multiclass.train_model(multiclass_model, class_mode='categorical')

# app = MainScreen()
# app.run()