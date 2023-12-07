from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import os


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

        self.zoom_factor = 1.0
        self.image_loaded = False
        self.current_pil_image = None

        # Configure main window
        self.root.configure(bg="#F3F3F3")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Main frame that will contain all other frames
        self.main_frame = tk.Frame(self.root, bg="#F3F3F3", padx=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=40)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title frame and label
        self.title_label = tk.Label(self.main_frame, text="Teste Papanicolau", font=("Times New Roman", 35), pady=20, bg="#F3F3F3")
        self.title_label.grid(row=0, column=0, pady=20, sticky="ew")

        # Buttons frame for folder and CSV selection
        self.button_frame = tk.Frame(self.main_frame, bg="#f3f3f3")
        self.button_frame.grid(row=1, column=0, pady=20, sticky="ew")

        # Folder selection button and label
        self.select_folder_button = tk.Button(self.button_frame, text="Selecionar Pasta", width=button_width, height=button_height, command=self.select_folder_and_update_label)
        self.select_folder_button.grid(row=0, column=0, pady=20, sticky="ew")

        self.folder_label = tk.Label(self.button_frame, text="", bg="#F3F3F3")
        self.folder_label.grid(row=1, column=0, sticky="ew")

        # CSV selection button and label
        self.select_csv_button = tk.Button(self.button_frame, text="Selecionar Arquivo CSV", width=button_width, height=button_height, command=self.select_csv_and_update_label)
        self.select_csv_button.grid(row=0, column=1, padx=button_padx, pady=20, sticky="ew")

        self.csv_label = tk.Label(self.button_frame, text="", bg="#F3F3F3")
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
        self.carousel_frame = tk.Frame(self.main_frame, bg="#f3f3f3")
        self.carousel_frame.grid(row=2, column=0, pady=20, sticky="ew")

        self.current_index = 0
        self.image_paths = []

        self.image_container = tk.Frame(self.carousel_frame, highlightbackground="#bbb", highlightthickness=1)
        self.image_container.grid(row=0, column=0, columnspan=2)

        self.image_container.grid_rowconfigure(0, weight=1)
        self.image_container.grid_columnconfigure(0, weight=1)

        self.image_label = tk.Label(self.image_container, width=35, height=20)
        self.image_label.grid(row=0, column=0, columnspan=2)

        self.button_frame = tk.Frame(self.carousel_frame)
        self.button_frame.configure(bg="#f3f3f3")
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
        self.zoom_frame = tk.Frame(self.main_frame, bg="#F3F3F3")
        self.zoom_frame.grid(row=3, column=0, pady=20, sticky="ew")

        # Zoom label
        self.zoom_label = tk.Label(self.zoom_frame, text="Zoom", bg="#F3F3F3")
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

        self.segmentation_buttons_frame = tk.Frame(self.main_container, bg="#f3f3f3")
        self.segmentation_buttons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.active_button = None

        self.allowed_button_clicks = {
            "Segmentar": ["Cortar"],
            "Cortar": ["Descrever"],
            "Descrever": ["Classificar"],
            "Classificar": []
        }

        self.segment_buttons = {
            "Segmentar": tk.Button(self.segmentation_buttons_frame, text="Segmentar", width=button_width, height=button_height, command=self.activate_segmentar),
            "Cortar": tk.Button(self.segmentation_buttons_frame, text="Cortar", width=button_width, height=button_height, command=self.activate_cortar),
            "Descrever": tk.Button(self.segmentation_buttons_frame, text="Descrever", width=button_width, height=button_height, command=self.activate_descrever),
            "Classificar": tk.Button(self.segmentation_buttons_frame, text="Classificar", width=button_width, height=button_height, command=self.activate_classificar)
        }

        for i, (button_text, button) in enumerate(self.segment_buttons.items()):
            button.grid(row=0, column=i, padx=10, pady=10)
            button.config(state=tk.DISABLED)

        self.update_button_state()

    def run(self):
        self.root.mainloop()


    def activate_segmentar(self):
        read_csv(CSV_FILE_PATH)
        ImageSegmentController.segment_images(INPUT_IMAGES_PATH, SEGMENTED_IMAGES_PATH, CSV_CELLS_PATH)


    def activate_cortar(self):
        self.activate_button("Cortar")

    def activate_descrever(self):
        self.activate_button("Descrever")

    def activate_classificar(self):
        self.activate_button("Classificar")

    def update_button_state(self):
        for button in self.segment_buttons.values():
            button.config(state=tk.DISABLED)

        if self.csv_label.cget("text"):
            self.segment_buttons["Segmentar"].config(state=tk.NORMAL)

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
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            folder_name = os.path.basename(folder_path)
            self.folder_label.config(text=folder_name)
            self.update_images_from_folder(folder_path)

    def select_csv_and_update_label(self):
        csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if csv_path:
            csv_name = os.path.basename(csv_path)
            self.csv_label.config(text=csv_name)
            self.update_button_state()

    def create_button(self, text, command, row, column):
        button = tk.Button(self.button_frame, text=text, command=command)
        button.configure(width=30, height=2)
        button.grid(row=row, column=column, pady=(0, 10), padx=10, sticky="ew")

        return button

    def image(self, image_paths):
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
            self.image(self.image_paths)  # Chama a função que exibe a imagem atual

    def previous_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.image(self.image_paths)

    def update_images_from_folder(self, folder_path):
        self.image_paths = self.get_image_paths_from_folder(folder_path)
        self.image(self.image_paths)

    def get_image_paths_from_folder(self, folder_path):
        image_extensions = ['.jpg', '.png', '.jpeg', '.gif']
        image_paths = []

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
                    image_paths.append(file_path)

        return image_paths

    def activate_button(self, button_name):
        if not self.active_button:
            if button_name == "Segmentar":
                if self.csv_label.cget("text"):  # Verifica se o CSV foi selecionado
                    self.active_button = button_name
                    self.segment_buttons[button_name].config(state="active")
        else:
            self.check_and_activate_button(button_name)

    def check_and_activate_button(self, button_name):
        if button_name in self.allowed_button_clicks[self.active_button]:
            self.segment_buttons[self.active_button].config(state="normal")
            self.active_button = button_name
            self.segment_buttons[button_name].config(state="active")
