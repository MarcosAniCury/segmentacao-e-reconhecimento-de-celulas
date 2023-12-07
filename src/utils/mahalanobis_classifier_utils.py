from src.enums.cell_enums import BethesdaSystemEnum
from src.utils.os_utils import OSUtils
from PIL import Image
import os.path
import numpy


def __get_label(folder_class, is_binary):
    label = 0
    for i, bethesda in enumerate(BethesdaSystemEnum):
        if bethesda == folder_class:
            label = i
            break

    if is_binary and label >= 1:
        label = 1

    return label


def __get_images_from_folder(TEST_TRAINING_IMAGES_PATH, is_binary):
    folders_test_train = OSUtils.get_files_in_folder(TEST_TRAINING_IMAGES_PATH)
    files = {}
    for folder_type in folders_test_train:
        files[folder_type] = {}
        files[folder_type]['images'] = []
        files[folder_type]['labels'] = []
        folders_type_path = os.path.join(TEST_TRAINING_IMAGES_PATH, folder_type)
        folders_class = OSUtils.get_files_in_folder(folders_type_path)
        for folder_class in folders_class:
            label = __get_label(folder_class, is_binary)

            folder_class_path = os.path.join(folders_type_path, folder_class)
            folders_class_files = OSUtils.get_files_in_folder(folder_class_path)
            for image in folders_class_files:
                image_path = os.path.join(folder_class_path, image)
                img = Image.open(image_path)
                img_array = numpy.array(img).flatten()
                files[folder_type]['images'].append(img_array)
                files[folder_type]['labels'].append(label)

        files[folder_type]['images'] = numpy.array(files[folder_type]['images'])
        files[folder_type]['labels'] = numpy.array(files[folder_type]['labels'])

    return files


def prepare_data_to_train(TEST_TRAINING_IMAGES_PATH, is_binary=True):
    files = __get_images_from_folder(TEST_TRAINING_IMAGES_PATH, is_binary)

    X_train = files['training']['images']
    Y_train = files['training']['labels']

    X_test = files['test']['images']
    Y_test = files['test']['labels']

    return X_train, Y_train, X_test, Y_test
