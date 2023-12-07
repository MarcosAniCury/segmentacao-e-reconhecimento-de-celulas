from tkinter import filedialog
import tkinter as tk
import os


class ButtonSection:
    def __init__(self, root):
        self.button_frame = tk.Frame(root, bg="#F3F3F3")
        self.button_frame.grid(row=3, columnspan=2, pady=10)

        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.folder_button = self.create_button("Selecionar Pasta", self.select_folder_and_update_label, 0, 0)
        self.folder_button.grid(sticky="nsew")

        self.folder_label = tk.Label(self.button_frame, text="", font=("Times New Roman", 10), bg="#F3F3F3")
        self.folder_label.grid(row=1, column=0, sticky="nsew")
        self.folder_label.grid(sticky="nsew")

        self.csv_button = self.create_button("Selecionar Arquivo CSV", self.select_csv_and_update_label, 0, 1)
        self.csv_button.grid(sticky="nsew")

        self.csv_label = tk.Label(self.button_frame, text="", font=("Times New Roman", 10), bg="#F3F3F3")
        self.csv_label.grid(row=1, column=1, sticky="nsew")
        self.csv_label.grid(sticky="nsew")

        self.confirm_button = self.create_button("Confirmar Seleção", self.confirm_button_open_image, 2, None)
        self.confirm_button.grid(sticky="nsew")

    def select_folder_and_update_label(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_name = os.path.basename(folder_path)
            self.folder_label.config(text=folder_name)

    def select_csv_and_update_label(self):
        csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if csv_path:
            csv_name = os.path.basename(csv_path)
            self.csv_label.config(text=csv_name)

    def create_button(self, text, command, row, column):
        button = tk.Button(self.button_frame, text=text, command=command)
        button.configure(width=30, height=2)
        button.grid(row=row, column=column, pady=(0, 10), padx=10, sticky="ew")

        return button

    def confirm_button_open_image(self):
        if self.folder_path:
            pass

