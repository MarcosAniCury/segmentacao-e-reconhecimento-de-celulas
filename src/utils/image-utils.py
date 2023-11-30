from PIL import Image

class ImageUtils:
    def crop_image(self, image_path, nucleus_x, nucleus_y, crop_size=100):
        original_image = Image.open(image_path)

        # Calcula as coordenadas para o corte
        left = nucleus_x - crop_size // 2
        top = nucleus_y - crop_size // 2
        right = left + crop_size
        bottom = top + crop_size

        # Corta a imagem
        cropped_image = original_image.crop((left, top, right, bottom))

        # Salva ou exibe a imagem cortada
        cropped_image.show()

ImageUtils.crop_image("../assets/")