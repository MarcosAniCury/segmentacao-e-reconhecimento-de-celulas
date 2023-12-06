from src.singleton.cells_singleton import CellListSingleton
from src.enums.cell_enums import BethesdaSystemEnum
from src.utils.os_utils import OSUtils
import random
import os


class ImageClassificationController:

    @staticmethod
    def __create_class_folders(folder_cells_classification_path):
        OSUtils.mkdir(folder_cells_classification_path)
        for bethesda_system in BethesdaSystemEnum:
            folder_cell_classification_path = os.path.join(folder_cells_classification_path, bethesda_system.name)
            OSUtils.mkdir(folder_cell_classification_path)

    @staticmethod
    def classify_images(CROPPED_IMAGES_PATH, CLASSIFIED_IMAGES_PATH):
        cells = CellListSingleton()
        images_cells_path = OSUtils.get_files_in_folder(CROPPED_IMAGES_PATH)
        ImageClassificationController.__create_class_folders(CLASSIFIED_IMAGES_PATH)

        for image_cell_path in images_cells_path:
            file_path = os.path.join(CROPPED_IMAGES_PATH, image_cell_path)
            cell_id = int(image_cell_path.split(".")[0])
            cell_bethesda_system = [cell_filter.bethesda_system for cell_filter in cells.shared_list
                                    if cell_filter.cell_id == cell_id][0]
            folder_cell_classification_path = os.path.join(CLASSIFIED_IMAGES_PATH, cell_bethesda_system.name)
            OSUtils.mv(file_path, folder_cell_classification_path)

    @staticmethod
    def __separate_image_test_training(CLASSIFIED_IMAGES_PATH, training_path, test_path):
        for bethesda_class in BethesdaSystemEnum:
            classification_class_path = os.path.join(CLASSIFIED_IMAGES_PATH, bethesda_class.name)
            files_in_class_folder = OSUtils.get_files_in_folder(classification_class_path)

            training_percent = 0.8
            n_items_training = int(len(files_in_class_folder) * training_percent)
            random.shuffle(files_in_class_folder)

            training_set = files_in_class_folder[:n_items_training]
            test_set = files_in_class_folder[n_items_training:]

            for training_image in training_set:
                image_training_path = os.path.join(CLASSIFIED_IMAGES_PATH, bethesda_class.name, training_image)
                OSUtils.mv(image_training_path, os.path.join(training_path, bethesda_class.name))

            for test_image in test_set:
                image_test_path = os.path.join(CLASSIFIED_IMAGES_PATH, bethesda_class.name, test_image)
                OSUtils.mv(image_test_path, os.path.join(test_path, bethesda_class.name))

    @staticmethod
    def set_training_and_test(TEST_TRAINING_IMAGES_PATH, CLASSIFIED_IMAGES_PATH):
        OSUtils.mkdir(TEST_TRAINING_IMAGES_PATH)
        training_path = os.path.join(TEST_TRAINING_IMAGES_PATH, 'training')
        test_path = os.path.join(TEST_TRAINING_IMAGES_PATH, 'test')
        ImageClassificationController.__create_class_folders(training_path)
        ImageClassificationController.__create_class_folders(test_path)

        ImageClassificationController.__separate_image_test_training(CLASSIFIED_IMAGES_PATH, training_path, test_path)
