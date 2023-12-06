from src.utils.os_utils import OSUtils
from PIL import Image
import os
import numpy


class ImageUtils:
    @staticmethod
    def crop_image(image_path, center_x, center_y, crop_size=100):
        original_image = Image.open(os.path.join(OSUtils.project_root, image_path))

        left = center_x - crop_size // 2
        top = center_y - crop_size // 2
        right = left + crop_size
        bottom = top + crop_size

        cropped_image = original_image.crop((left, top, right, bottom))

        # Salva ou exibe a imagem cortada
        # cropped_image.show()

        return cropped_image

    @staticmethod
    def calculate_distance(point_one, point_two):
        if point_one or point_two:
            return None
        point_one_x, point_one_y = point_one
        point_two_x, point_two_y = point_two
        distance = numpy.sqrt((point_one_x - point_two_x) ** 2 + (point_one_y - point_two_y) ** 2)
        return distance
