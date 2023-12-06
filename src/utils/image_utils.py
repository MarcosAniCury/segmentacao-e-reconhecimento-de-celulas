from src.utils.os_utils import OSUtils
from PIL import Image
import numpy
import cv2
import os


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
    def calculate_euclidian_distance(point_one, point_two):
        if not point_one or not point_two:
            return None
        point_one_x, point_one_y = point_one
        point_two_x, point_two_y = point_two
        distance = numpy.sqrt((point_one_x - point_two_x) ** 2 + (point_one_y - point_two_y) ** 2)
        return distance

    @staticmethod
    def calculate_eccentricity(contour):
        # Calculate the moments of the contour
        moments = cv2.moments(contour)

        # Calculate the second order central moments
        mu20 = moments['mu20']
        mu02 = moments['mu02']
        mu11 = moments['mu11']

        # Calculate the major and minor axes
        a = numpy.sqrt(0.5 * (mu20 + mu02 + numpy.sqrt((mu20 - mu02) ** 2 + 4 * mu11 ** 2)))
        b = numpy.sqrt(0.5 * (mu20 + mu02 - numpy.sqrt((mu20 - mu02) ** 2 + 4 * mu11 ** 2)))

        # Calculate eccentricity
        eccentricity = numpy.sqrt(1 - (b ** 2 / a ** 2)) if a != 0 else 0

        return eccentricity

