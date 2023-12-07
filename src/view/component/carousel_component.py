from PIL import Image, ImageTk
from pathlib import Path
import tkinter as tk
import os
import src.assets.default_images as images


class Carousel:
    def __init__(self, root, custom_image_directory=None):
        self.root = root
        self.current_index = 0
        self.current_image = None

        if custom_image_directory is None:
            default_image_directory = os.path.join(Path(images.__path__[0]), "default_images")
            self.image_paths = self.get_image_paths(default_image_directory)
        else:
            self.image_paths = self.get_image_paths(custom_image_directory)

        self.image_container = tk.Frame(self.carousel_frame, bg="#f5f5f5", highlightbackground="#bbb", highlightthickness=1)
        self.image_container.pack()

        self.image_label = tk.Label(self.image_container, width=500, height=364)
        self.image_label.pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.configure(bg="#f5f5f5")
        self.button_frame.pack()

        button_width = 30
        button_height = 2

        self.prev_button = tk.Button(self.button_frame, text="Anterior", width=button_width, height=button_height, command=self.previous_image)
        self.prev_button.pack(side=tk.LEFT, padx=(0, 33), pady=25)

        self.next_button = tk.Button(self.button_frame, text="Próxima", width=button_width, height=button_height, command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=(33, 0), pady=25)

        self.image()

    def image(self):
        if self.image_paths and 0 <= self.current_index < len(self.image_paths):
            img = Image.open(self.image_paths[self.current_index])

            img.thumbnail((500, 500), Image.LANCZOS)

            photo_img = ImageTk.PhotoImage(img)
            self.current_image = photo_img

            self.image_label.configure(image=photo_img)
            self.image_label.image = photo_img

    def next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.image()

    def previous_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.image()

    def get_image_paths(self, image_directory):
        image_paths_set = set()

        if os.path.exists(image_directory):
            files = os.listdir(image_directory)

            image_name_files = [name_file for name_file in files if name_file.endswith(".jpg") or name_file.endswith(".png")]

            for name_file in image_name_files:
                full_file_path = os.path.join(image_directory, name_file)
                image_paths_set.add(full_file_path)

        sorted_image_paths_list = sorted(list(image_paths_set))
        return sorted_image_paths_list
