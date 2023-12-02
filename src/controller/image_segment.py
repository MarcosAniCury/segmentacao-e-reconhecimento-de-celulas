import cv2
import numpy as np


class ImageSegment:
    @staticmethod
    def segment_image(image_path):
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
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)

            # Verificar se o perímetro é zero antes de calcular a circularidade
            if perimeter != 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)

                # Ajuste o valor de circularity conforme necessário
                if circularity > 0.5:
                    filtered_contours.append(contour)

        # Criar máscara para os contornos filtrados
        cells_mask = np.zeros_like(gray)
        cv2.drawContours(cells_mask, filtered_contours, -1, (255), thickness=cv2.FILLED)

        return cells_mask
