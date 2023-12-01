from PIL import Image


class ImageUtils:
    @staticmethod
    def crop_image(image_path, center_x, center_y, crop_size=100):
        original_image = Image.open(image_path)

        left = center_x - crop_size // 2
        top = center_y - crop_size // 2
        right = left + crop_size
        bottom = top + crop_size

        cropped_image = original_image.crop((left, top, right, bottom))

        # Salva ou exibe a imagem cortada
        # cropped_image.show()

        return cropped_image