from src.singleton.cells_singleton import CellListSingleton
from src.controller.csv_controller import CSVController
from src.utils.image_utils import ImageUtils
from src.utils.os_utils import OSUtils
from PIL import Image
import numpy as np
import cv2
import os


class ImageSegmentController:

    @staticmethod
    def segment_images(INPUT_IMAGES_PATH, SEGMENTED_IMAGES_PATH, CSV_CELLS_PATH):
        files_in_folder = OSUtils.get_files_in_folder(INPUT_IMAGES_PATH)
        OSUtils.mkdir(SEGMENTED_IMAGES_PATH)
        csv_cells = CSVController()
        csv_cells.open_csv(CSV_CELLS_PATH)
        for file in files_in_folder:
            segmented_image = ImageSegmentController.segment_image(os.path.join(INPUT_IMAGES_PATH, file), file, csv_cells)
            segmented_image.save(os.path.join(SEGMENTED_IMAGES_PATH, file))
        csv_cells.close_csv()

    @staticmethod
    def segment_image(image_path, image_name, csv_cells):
        cells = CellListSingleton()

        # Leitura da imagem
        image = cv2.imread(image_path)

        # Convertendo para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplicar limiarização para segmentar as células
        _, binary_image = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY_INV)

        # Aplicar uma operação de abertura para remover detalhes pequenos
        kernel = np.ones((5, 5), np.uint8)
        opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

        # Encontrar contornos
        contours, _ = cv2.findContours(opened_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filtrar contornos com área semelhante à de um círculo
        filtered_contours = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)

            # Verificar se o perímetro é zero antes de calcular a circularidade
            if perimeter != 0:
                area = cv2.contourArea(contour)
                circularity = 4 * np.pi * area / (perimeter * perimeter)

                # Ajuste o valor de circularity conforme necessário
                if circularity > 0.5:
                    compactness = area / (perimeter * perimeter)
                    eccentricity = ImageUtils.calculate_eccentricity(contour)

                    filtered_contours.append(contour)
                    cell = cells.insert_centroid_in_cell(contour, image_name)
                    if cell:
                        csv_cells_data = [str(cell.cell_id), str(area), str(compactness), str(eccentricity)]
                        csv_cells.insert_row(csv_cells_data)

        # Criar máscara para os contornos filtrados
        cells_mask = np.zeros_like(gray)
        cv2.drawContours(cells_mask, filtered_contours,
                         -1, (255), thickness=cv2.FILLED)

        image = Image.fromarray(cells_mask)

        return image
