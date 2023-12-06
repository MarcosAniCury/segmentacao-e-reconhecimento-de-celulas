from src.utils.os_utils import OSUtils
import numpy as np
import cv2
import os


class ImageDescriptorController:
    @staticmethod
    def descript_images(CROPPED_IMAGES_PATH):
        from src.singleton.cells_singleton import CellListSingleton
        from src.utils.image_utils import ImageUtils

        files_in_cropped_images_folder = OSUtils.get_files_in_folder(CROPPED_IMAGES_PATH)
        cells = CellListSingleton()
        for file in files_in_cropped_images_folder:
            cell_id = int(file.split('.')[0])
            cell = cells.find_cell_id(cell_id)
            cell_cvs_point = cell.nucleus_x, cell.nucleus_y
            image = cv2.imread(os.path.join(CROPPED_IMAGES_PATH, file))

            cell.chain_code = ImageDescriptorController.get_chain_code(image)
            cell.distance_nucleus = ImageUtils.calculate_euclidian_distance(cell_cvs_point, cell.centroid)

    @staticmethod
    def extract_shape_contour(binary_image):
        # Find contours
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Return the largest contour
        if contours:
            return max(contours, key=cv2.contourArea)
        return None

    @staticmethod
    def reconstruct_image_contour(contour, original_image_shape):
        # Criar uma imagem em branco
        reconstructed_image = np.zeros(original_image_shape, dtype=np.uint8)

        # Desenhar o contorno na imagem reconstruída
        cv2.drawContours(reconstructed_image, [contour], -1, (255), thickness=cv2.FILLED)

        return reconstructed_image

    @staticmethod
    def get_chain_code(image):
        # Convert the image to grayscale
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding or any segmentation method you prefer
        _, binary_image = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY)
        contour = ImageDescriptorController.extract_shape_contour(binary_image)

        if contour is not None:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            approx_list = [tuple(point[0]) for point in approx]
            chain_code = approx_list  # Use the entire list
            return chain_code

        return None

    @staticmethod
    def calculate_centroid(contour):
        # Calcular o momento do contorno
        M = cv2.moments(contour)

        if M['m00'] != 0:
            # Calcular as coordenadas do centroide
            centroid_x = int(M['m10'] / M['m00'])
            centroid_y = int(M['m01'] / M['m00'])

            return centroid_x, centroid_y
        return None
