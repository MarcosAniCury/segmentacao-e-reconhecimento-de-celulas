from utils import folder_separate_image, file_write
from ImageSegment import treat_image
from ImageAugment import augument
from Cnn import GoogLenNet
import time


def runCnn(is_binarie_class, already_trained, is_segment_image, arquive_name):
    start_time = time.time()
    folder_separate_image(is_binarie_class)
    if not already_trained:
        if is_segment_image:
            treat_image()
        augument(is_binarie_class)
    metrict = GoogLenNet(arquive_name, already_trained, is_binarie_class)
    end_time = time.time()
    execution_time = end_time - start_time
    file_write(arquive_name, execution_time,
               metrict, is_binarie_class)
