import cv2
import numpy as np
import os

def remove_image_variation_color(image):
    # Converter a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar um filtro de suavização para reduzir o ruído
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplicar a segmentação baseada em limiar adaptativo de Otsu
    _, thresholded = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Realizar uma operação de fechamento para preencher as regiões
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)

    # Encontrar os contornos dos objetos na imagem segmentada
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar uma máscara preta do mesmo tamanho da imagem original
    mask = np.zeros_like(image)

    # Desenhar os contornos dos objetos na máscara
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Aplicar a máscara na imagem original
    segmented_image = cv2.bitwise_and(image, mask)

    return segmented_image

def remove_small_items(image, threshold_area):
    # Converter a imagem para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar uma limiarização para obter uma imagem binária
    _, thresholded = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Encontrar os contornos dos objetos na imagem binária
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Criar uma máscara preta do mesmo tamanho da imagem original
    mask = np.zeros_like(image)

    # Percorrer todos os contornos encontrados
    for contour in contours:
        # Calcular a área do contorno
        area = cv2.contourArea(contour)

        # Se a área do contorno for maior que o limite, desenhar o contorno na máscara
        if area > threshold_area:
            cv2.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    # Aplicar a máscara na imagem original
    result_image = cv2.bitwise_and(image, mask)

    return result_image

def treat_image():
    training_dir = "treino"
    # Percorrer todas as pastas dentro do diretório de treino
    for dirpath, dirnames, filenames in os.walk(training_dir):
        for dirpath_class, dirnames_class, filenames_class in os.walk(dirpath):
            # Percorre todos os arquivos
            for arquive in filenames_class:
                # Pega apenas os arquivos de imagem
                if arquive.endswith(".png") or arquive.endswith(".jpg") or arquive.endswith(".jpeg"):
                    path_image = os.path.join(dirpath_class, arquive)
                    image = cv2.imread(path_image)
                    # Remove variacoes de cores da imagem
                    result_image = remove_image_variation_color(image)

                    # Área mínima para considerar um contorno como elemento principal
                    threshold_area = 10000  
                    # Remove objetos menores que o threshold_area
                    result_image = remove_small_items(result_image, threshold_area)
                    # Sobre escreve imagens anteriores pelas pré-processadas
                    cv2.imwrite(path_image, result_image)