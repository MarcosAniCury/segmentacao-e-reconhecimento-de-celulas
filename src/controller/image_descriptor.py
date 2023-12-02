import cv2
import numpy as np

class ImageDescriptor:
    @staticmethod
    def extract_shape_contour(segmented_image):
        # Encontrar contornos na imagem segmentada
        contours, _ = cv2.findContours(segmented_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Selecionar o maior contorno (assumindo que é a célula)
        largest_contour = max(contours, key=cv2.contourArea)

        return largest_contour

    @staticmethod
    def reconstruct_image_contour(contour, original_image_shape):
        # Criar uma imagem em branco
        reconstructed_image = np.zeros(original_image_shape, dtype=np.uint8)

        # Desenhar o contorno na imagem reconstruída
        cv2.drawContours(reconstructed_image, [contour], -1, (255), thickness=cv2.FILLED)

        return reconstructed_image
