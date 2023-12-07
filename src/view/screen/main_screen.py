import tkinter as tk
from src.view.component.button_selection import ButtonSection
from src.view.component.carousel_component import Carousel


class TitleSection:
    def __init__(self, root):
        self.title_label = tk.Label(root, text="Teste Papanicolau", font=("Times New Roman", 35), pady=20, fg="black")
        self.title_label.configure(bg="#F3F3F3")
        self.title_label.grid(row=0, column=0, columnspan=2)


class MainScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Segmentação e Reconhecimento de Células em Exames de Papanicolau")
        self.root.configure(bg="#F3F3F3")
        self.configure_main()

        title_section = TitleSection(self.root)
        title_section.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        button_section = ButtonSection(self.root)
        button_section.button_frame.grid(row=1, column=0, columnspan=2, pady=20)

        carousel_section = Carousel(self.root)
        button_section.button_frame.grid(row=3, column=0, columnspan=2, pady=20)

    def configure_main(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.root.grid_columnconfigure(0, weight=1)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainScreen()
    app.run()
