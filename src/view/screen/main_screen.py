from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import os
from src.controller.image_classification_controller import ImageClassificationController
from src.controller.image_preprocessor_controller import ImagePreProcessorController
from src.controller.image_descriptor_controller import ImageDescriptorController
from src.utils.mahalanobis_classifier_utils import prepare_data_to_train
from src.utils.scatterplot_utils import format_items_to_scatterplot_pattern
from src.controller.image_segment_controller import ImageSegmentController
from src.classifiers.malahnobis_classifier import MalahanobisClassifier
from src.controller.scatterplot_controller import ScatterplotController
from src.classifiers.resnet50_classifier import Restnet50Classifier
from src.utils.resnet_classifier_utils import setup_binary_classification_structure
from src.utils.csv_utils import read_csv
from src.utils.os_utils import OSUtils
import os
import matplotlib.pyplot as plt

SCATTERPLOT_PATH = os.path.join(OSUtils.project_images_root, 'scatterplot.png')
CSV_CELLS_PATH = os.path.join(OSUtils.project_images_root, 'cells_characteristics.csv')
SEGMENTED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'segmented_images')
CROPPED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'cropped_images')
CLASSIFIED_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'classified_images')
TEST_TRAINING_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'test_training_images')
TEST_TRAINING_BINARY_IMAGES_PATH = os.path.join(OSUtils.project_images_root, 'test_training_images_binary')



class MainScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Segmentação e Reconhecimento de Células em Exames de Papanicolau")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width)
        self.root.geometry(f"{width}x{screen_height}")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=3, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame_in_canvas = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_in_canvas, anchor="nw")

        self.main_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        button_width = 20
        button_height = 2
        button_padx = 20
        self.csv_path = None
        self.folder_path = None

        self.zoom_factor = 1.0
        self.image_loaded = False
        self.current_pil_image = None

        # Configure main window
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Main frame that will contain all other frames
        self.main_frame = tk.Frame(self.root, padx=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=40)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title frame and label
        self.title_label = tk.Label(self.main_frame, text="Teste Papanicolau", font=("Times New Roman", 35), pady=20 )
        self.title_label.grid(row=0, column=0, pady=5, sticky="ew")

        # Buttons frame for folder and CSV selection
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, pady=5, sticky="ew")

        # Folder selection button and label
        self.select_folder_button = tk.Button(self.button_frame, text="Selecionar Pasta", width=button_width, height=button_height, command=self.select_folder_and_update_label)
        self.select_folder_button.grid(row=0, column=0, pady=20, sticky="ew")

        self.folder_label = tk.Label(self.button_frame, text="")
        self.folder_label.grid(row=1, column=0, sticky="ew")

        # CSV selection button and label
        self.select_csv_button = tk.Button(self.button_frame, text="Selecionar Arquivo CSV", width=button_width, height=button_height, command=self.select_csv_and_update_label)
        self.select_csv_button.grid(row=0, column=1, padx=button_padx, pady=20, sticky="ew")

        self.csv_label = tk.Label(self.button_frame, text="")
        self.csv_label.grid(row=1, column=1, padx=button_padx, pady=5, sticky="ew")

        # Center frame child
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.select_folder_button.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.folder_label.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        self.select_csv_button.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.csv_label.grid(row=1, column=1, padx=20, pady=5, sticky="nsew")

        # Carousel frame for image display
        self.carousel_frame = tk.Frame(self.main_frame)
        self.carousel_frame.grid(row=2, column=0, pady=5, sticky="ew")

        self.current_index = 0
        self.image_paths = []

        self.image_container = tk.Frame(self.carousel_frame, highlightbackground="#bbb", highlightthickness=1)
        self.image_container.grid(row=0, column=0, columnspan=2)

        self.image_container.grid_rowconfigure(0, weight=1)
        self.image_container.grid_columnconfigure(0, weight=1)

        self.image_label = tk.Label(self.image_container, width=35, height=20)
        self.image_label.grid(row=0, column=0, columnspan=2)

        self.button_frame = tk.Frame(self.carousel_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2)

        self.prev_button = tk.Button(self.button_frame, text="Anterior", width=button_width, height=button_height, command=self.previous_image)
        self.prev_button.grid(row=0, column=0, padx=button_padx, pady=25, sticky="ew")

        self.next_button = tk.Button(self.button_frame, text="Próxima", width=button_width, height=button_height, command=self.next_image)
        self.next_button.grid(row=0, column=1, padx=button_padx, pady=25, sticky="ew")

        # Center frame child
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.carousel_frame.grid_rowconfigure(0, weight=1)
        self.carousel_frame.grid_rowconfigure(1, weight=0)
        self.carousel_frame.grid_columnconfigure(0, weight=1)
        self.carousel_frame.grid_columnconfigure(1, weight=1)

        self.image_container.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.prev_button.grid(row=0, column=0, padx=(0, 33), pady=25, sticky="ew")
        self.next_button.grid(row=0, column=1, padx=(33, 0), pady=25, sticky="ew")

        # Zoom controls frame
        self.zoom_frame = tk.Frame(self.main_frame)
        self.zoom_frame.grid(row=3, column=0, pady=5, sticky="ew")

        # Zoom label
        self.zoom_label = tk.Label(self.zoom_frame, text="Zoom")
        self.zoom_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=20)

        # Zoom in and out buttons
        self.zoom_in_button = tk.Button(self.zoom_frame, text="+", width=button_width, height=button_height, command=self.zoom_in)
        self.zoom_in_button.grid(row=1, column=1, sticky="ew", padx=25)

        self.zoom_out_button = tk.Button(self.zoom_frame, text="-", width=button_width, height=button_height, command=self.zoom_out)
        self.zoom_out_button.grid(row=1, column=0, sticky="ew", padx=25)

        self.zoom_frame.grid_columnconfigure(0, weight=1)
        self.zoom_frame.grid_columnconfigure(1, weight=1)
        self.zoom_label.grid(sticky="nsew", pady=10)

        self.main_container = tk.Frame(self.root)
        self.main_container.grid(row=0, column=1, columnspan=2, sticky="nsew")

        self.main_container.grid_columnconfigure(0, weight=0)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.segmentation_buttons_frame = tk.Frame(self.main_container)
        self.segmentation_buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.active_button = None

        self.allowed_button_clicks = {
            "Segmentar": ["Cortar"],
            "Cortar": ["Descrever"],
            "Descrever": ["Classificar"],
            "Classificar": []
        }

        self.segment_buttons = {
            "Segmentar": tk.Button(self.segmentation_buttons_frame, text="Segmentar", width=button_width, height=button_height, command=self.activate_segment),
            "Cortar": tk.Button(self.segmentation_buttons_frame, text="Cortar", width=button_width, height=button_height, command=self.activate_crop),
            "Descrever": tk.Button(self.segmentation_buttons_frame, text="Descrever", width=button_width, height=button_height, command=self.activate_description),
            "Classificar": tk.Button(self.segmentation_buttons_frame, text="Classificar", width=button_width, height=button_height, command=self.activate_classify)

        }

        for i, (button_text, button) in enumerate(self.segment_buttons.items()):
            button.grid(row=0, column=i, padx=10, pady=10)
            button.config(state=tk.DISABLED)

        self.scatterplot_button = tk.Button(self.segmentation_buttons_frame, text="Scatterplot", width=button_width, height=button_height, command=self.generate_scatterplot)
        self.scatterplot_button.grid(row=1, column=0, padx=10, pady=10)
        self.scatterplot_button.config(state=tk.DISABLED)

         # Carousel frame for image display
        self.carousel_frame_images = tk.Frame(self.main_container)
        self.carousel_frame_images.grid(row=2, column=0, pady=5, sticky="ew")

        self.carousel_frame_images_current_index = 0
        self.carousel_frame_images_image_paths = []

        self.carousel_frame_images_container = tk.Frame(self.carousel_frame_images, highlightbackground="#bbb", highlightthickness=1)
        self.carousel_frame_images_container.grid(row=1, column=0, columnspan=2)

        self.carousel_frame_images_container.grid_rowconfigure(0, weight=1)
        self.carousel_frame_images_container.grid_columnconfigure(0, weight=1)

        self.carousel_frame_image_label = tk.Label(self.carousel_frame_images_container, width=35, height=20)
        self.carousel_frame_image_label.grid(row=0, column=0, columnspan=2)

        self.carousel_frame_button_frame = tk.Frame(self.carousel_frame_images)
        self.carousel_frame_button_frame.grid(row=2, column=0, columnspan=2)

        self.carousel_frame_prev_button = tk.Button(self.carousel_frame_button_frame, text="Anterior", width=button_width, height=button_height, command=self.previous_image_container)
        self.carousel_frame_prev_button.grid(row=0, column=0, padx=button_padx, pady=25, sticky="ew")

        self.carousel_frame_next_button = tk.Button(self.carousel_frame_button_frame, text="Próxima", width=button_width, height=button_height, command=self.next_image_container)
        self.carousel_frame_next_button.grid(row=0, column=0, padx=button_padx, pady=25, sticky="ew")

        # Center frame child
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.carousel_frame_images.grid_rowconfigure(0, weight=1)
        self.carousel_frame_images.grid_rowconfigure(1, weight=0)
        self.carousel_frame_images.grid_columnconfigure(0, weight=1)
        self.carousel_frame_images.grid_columnconfigure(1, weight=1)

        self.carousel_frame_images_container.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.carousel_frame_button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        self.carousel_frame_button_frame.grid_columnconfigure(0, weight=1)
        self.carousel_frame_button_frame.grid_columnconfigure(1, weight=1)

        self.carousel_frame_prev_button.grid(row=0, column=0, padx=(0, 33), pady=25, sticky="ew")
        self.carousel_frame_next_button.grid(row=0, column=1, padx=(33, 0), pady=25, sticky="ew")

        self.image_container_change(self.carousel_frame_images_image_paths)

    def run(self):
        self.root.mainloop()

    def activate_segment(self):
        if self.segment_buttons["Segmentar"].cget('state') == tk.NORMAL:
            self.segment_buttons["Cortar"].config(state=tk.NORMAL)
            self.segment_buttons["Segmentar"].config(state=tk.DISABLED)
            print("Read CSV")
            read_csv(self.csv_path)

            print("Segment Image")
            ImageSegmentController.segment_images(self.folder_path, SEGMENTED_IMAGES_PATH, CSV_CELLS_PATH)

            print("Create Scatterplot")
            ScatterplotController.generate_scatterplot(format_items_to_scatterplot_pattern(CSV_CELLS_PATH), SCATTERPLOT_PATH)
            self.scatterplot_button.config(state=tk.NORMAL)
            self.update_segmented_images_from_folder()

    def generate_scatterplot(self):
        plt.show()


    def activate_crop(self):
        if self.segment_buttons["Cortar"].cget('state') == tk.NORMAL:
            self.segment_buttons["Descrever"].config(state=tk.NORMAL)
            self.segment_buttons["Cortar"].config(state=tk.DISABLED)
            print("Crop Image")
            ImagePreProcessorController.crop_image_per_cell(SEGMENTED_IMAGES_PATH, CROPPED_IMAGES_PATH)

            print("Crop Image")
            ImagePreProcessorController.crop_image_per_cell(SEGMENTED_IMAGES_PATH, CROPPED_IMAGES_PATH)

            self.update_croped_images_from_folder()
    def activate_description(self):
        if self.segment_buttons["Descrever"].cget('state') == tk.NORMAL:
            self.segment_buttons["Classificar"].config(state=tk.NORMAL)
            self.segment_buttons["Descrever"].config(state=tk.DISABLED)
            print("Descript Image")
            ImageDescriptorController.descript_images(CROPPED_IMAGES_PATH)

            print("Descript Image")
            ImageDescriptorController.descript_images(CROPPED_IMAGES_PATH)

    def change_image(self):
        self.segment_buttons["Cortar"].config(state=tk.DISABLED)
        self.segment_buttons["Descrever"].config(state=tk.DISABLED)
        self.segment_buttons["Classificar"].config(state=tk.DISABLED)
        self.segment_buttons["Segmentar"].config(state=tk.NORMAL)

    def activate_classify(self):
        if self.segment_buttons["Classificar"].cget('state') == tk.NORMAL:
            self.segment_buttons["Segmentar"].config(state=tk.NORMAL)
            print("Classification Image")
            ImageClassificationController.classify_images(CROPPED_IMAGES_PATH, CLASSIFIED_IMAGES_PATH)

            print("Separate in test and training")
            ImageClassificationController.set_training_and_test(TEST_TRAINING_IMAGES_PATH, CLASSIFIED_IMAGES_PATH)

    def update_button_state(self):
        for button in self.segment_buttons.values():
            button.config(state=tk.DISABLED)

    def zoom_in(self):
        if self.image_loaded and self.current_pil_image:
            self.zoom_factor *= 1.2
            self.update_image_with_zoom()

    def zoom_out(self):
        if self.image_loaded and self.current_pil_image:
            self.zoom_factor /= 1.2
            self.update_image_with_zoom()

    def update_image_with_zoom(self):
        if self.image_loaded and self.current_pil_image:
            img = self.current_pil_image
            width = int(img.width * self.zoom_factor)
            height = int(img.height * self.zoom_factor)

            img_resized = img.resize((width, height), Image.LANCZOS)
            photo_img = ImageTk.PhotoImage(img_resized)

            self.image_label.configure(image=photo_img)
            self.image_label.image = photo_img

    def select_folder_and_update_label(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.folder_path = self.folder_path
            folder_name = os.path.basename(self.folder_path)
            self.folder_label.config(text=folder_name)
            self.update_images_from_folder()

    def select_csv_and_update_label(self):
        self.csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.csv_path:
            self.csv_name = os.path.basename(self.csv_path)
            self.csv_label.config(text=self.csv_name)
            self.update_button_state()
            if self.image_paths[self.current_index]:
                self.segment_buttons["Segmentar"].config(state=tk.NORMAL)

    def create_button(self, text, command, row, column):
        button = tk.Button(self.button_frame, text=text, command=command)
        button.configure(width=30, height=2)
        button.grid(row=row, column=column, pady=(0, 10), padx=10, sticky="ew")

        return button

    def image(self, image_paths):
        if self.csv_path:
            self.change_image()

        if image_paths:
            img = Image.open(image_paths[self.current_index])
            width, height = img.size
            new_width = int(width * 0.3)
            new_height = int(height * 0.3)

            img = img.resize((new_width, new_height), Image.LANCZOS)

            photo_img = ImageTk.PhotoImage(img)
            self.current_image = photo_img

            self.image_label.config(width=width, height=height)
            self.image_label.configure(width=new_width, height=new_height)

            self.image_label.configure(image=photo_img)
            self.image_label.image = photo_img

            self.current_pil_image = Image.open(image_paths[self.current_index])
            self.image_loaded = True

            self.image_label.update_idletasks()

    def next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.image(self.image_paths)

    def previous_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.image(self.image_paths)

    def image_container_change(self, image_paths):
        if image_paths:
            img = Image.open(image_paths[self.carousel_frame_images_current_index])
            width, height = img.size
            new_width = int(width * 0.3)
            new_height = int(height * 0.3)

            img = img.resize((new_width, new_height), Image.LANCZOS)

            photo_img = ImageTk.PhotoImage(img)
            self.current_image = photo_img

            self.carousel_frame_image_label.config(width=width, height=height)
            self.carousel_frame_image_label.configure(width=new_width, height=new_height)

            self.carousel_frame_image_label.configure(image=photo_img)
            self.carousel_frame_image_label.image = photo_img

            self.current_pil_image = Image.open(image_paths[self.carousel_frame_images_current_index])
            self.image_loaded = True

            self.image_label.update_idletasks()

    def image_container_change_crop(self, image_paths):
        if image_paths:
            img = Image.open(image_paths[self.carousel_frame_images_current_index])
            width, height = img.size
            new_width = int(width*2)
            new_height = int(height*2)

            img = img.resize((new_width, new_height), Image.LANCZOS)

            photo_img = ImageTk.PhotoImage(img)
            self.current_image = photo_img

            self.carousel_frame_image_label.config(width=width, height=height)
            self.carousel_frame_image_label.configure(width=new_width, height=new_height)

            self.carousel_frame_image_label.configure(image=photo_img)
            self.carousel_frame_image_label.image = photo_img

            self.current_pil_image = Image.open(image_paths[self.carousel_frame_images_current_index])
            self.image_loaded = True

            self.image_label.update_idletasks()

    def next_image_container(self):
        if self.carousel_frame_images_image_paths:
            self.carousel_frame_images_current_index = (self.carousel_frame_images_current_index + 1) % len(self.carousel_frame_images_image_paths)
            self.image_container_change(self.carousel_frame_images_image_paths)

    def previous_image_container(self):
        if self.carousel_frame_images_image_paths:
            self.carousel_frame_images_current_index = (self.carousel_frame_images_current_index - 1) % len(self.carousel_frame_images_image_paths)
            self.image_container_change(self.carousel_frame_images_image_paths)

    def next_image_container(self):
        if self.carousel_frame_images_image_paths:
            self.carousel_frame_images_current_index = (self.carousel_frame_images_current_index + 1) % len(self.carousel_frame_images_image_paths)
            self.image_container_change_crop(self.carousel_frame_images_image_paths)

    def previous_image_container(self):
        if self.carousel_frame_images_image_paths:
            self.carousel_frame_images_current_index = (self.carousel_frame_images_current_index - 1) % len(self.carousel_frame_images_image_paths)
            self.image_container_change_crop(self.carousel_frame_images_image_paths)

    def update_images_from_folder(self):
        self.image_paths = self.get_image_paths_from_folder()
        self.image(self.image_paths)

    def get_image_paths_from_folder(self):
        image_extensions = ['.jpg', '.png', '.jpeg', '.gif']
        image_paths = []

        if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
            for file in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, file)
                if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
                    image_paths.append(file_path)

        return image_paths

    def update_segmented_images_from_folder(self):
        self.carousel_frame_images_image_paths = self.get_segmented_image_paths_from_folder()
        self.image_container_change(self.carousel_frame_images_image_paths)

    def get_segmented_image_paths_from_folder(self):
        image_extensions = ['.jpg', '.png', '.jpeg', '.gif']
        carousel_frame_images_image_paths = []

        if os.path.exists(SEGMENTED_IMAGES_PATH) and os.path.isdir(SEGMENTED_IMAGES_PATH):
            for file in os.listdir(SEGMENTED_IMAGES_PATH):
                file_path = os.path.join(SEGMENTED_IMAGES_PATH, file)
                if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
                    carousel_frame_images_image_paths.append(file_path)

        return carousel_frame_images_image_paths

    def update_croped_images_from_folder(self):
        self.carousel_frame_images_image_paths = self.get_croped_image_paths_from_folder()
        self.image_container_change_crop(self.carousel_frame_images_image_paths)

    def get_croped_image_paths_from_folder(self):
        image_extensions = ['.jpg', '.png', '.jpeg', '.gif']
        carousel_frame_images_image_paths = []

        if os.path.exists(CROPPED_IMAGES_PATH) and os.path.isdir(CROPPED_IMAGES_PATH):
            for file in os.listdir(CROPPED_IMAGES_PATH):
                file_path = os.path.join(CROPPED_IMAGES_PATH, file)
                if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
                    carousel_frame_images_image_paths.append(file_path)

        return carousel_frame_images_image_paths

    def activate_button(self, button_name):
        if not self.active_button:
            if button_name == "Segmentar":
                if self.csv_label.cget("text"):
                    self.active_button = button_name
                    self.segment_buttons[button_name].config(state="active")
        else:
            self.check_and_activate_button(button_name)

    def check_and_activate_button(self, button_name):
        if button_name in self.allowed_button_clicks[self.active_button]:
            self.segment_buttons[self.active_button].config(state="normal")
            self.active_button = button_name
            self.segment_buttons[button_name].config(state="active")

