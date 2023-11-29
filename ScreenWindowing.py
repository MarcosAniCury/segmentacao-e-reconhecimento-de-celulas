import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image


def open_explorer():
    # Abrir o explorador de arquivos
    initial_path = "C:\\Users\\letic\\Documents\\GitHub\\Analise-de-mama\\mamografias"
    filename = filedialog.askopenfilename(initialdir=initial_path, title="Selecione uma imagem", filetypes=(
        ("Arquivos de imagem", "*.jpg;*.jpeg;*.png"), ("Todos os arquivos", "*.*")))

    if filename:
        # Atualizar a imagem exibida
        load_image(filename)


def update_image_windowing(*args):
    global image_current_resize, image_current_photo, n_zooms, image_original_gray

    # Obtém os valores da barra deslizante
    min_value = min_slider.get()
    max_value = max_slider.get()

    # Aplica o janelamento
    imagem_ndarray = np.asanyarray(image_original_gray)
    output_img = np.zeros_like(imagem_ndarray)
    output_img = np.where(imagem_ndarray <= min_value, 0, output_img)
    output_img = np.where(imagem_ndarray > max_value, 255, output_img)
    output_img = np.where((imagem_ndarray > min_value) & (imagem_ndarray <= max_value),
                          ((imagem_ndarray - min_value) /
                           (max_value - min_value)) * 255,
                          output_img)

    # Converte a imagem para o formato PIL para mostrar na janela
    image_current_resize = Image.fromarray(
        output_img).resize((300, 400), Image.LANCZOS)
    image_current_photo = ImageTk.PhotoImage(image_current_resize)

    # Atualiza a imagem na janela
    label_image.configure(image=image_current_photo)
    label_image.image = image_current_photo

    n_zooms_temp = n_zooms

    if n_zooms > 0:
        type_zoom = zoom_in
    else:
        type_zoom = zoom_out

    n_zooms = 0

    for i in range(abs(n_zooms_temp)):
        type_zoom()


def zoom_in():
    global image_current_resize, image_current_photo, n_zooms

    n_zooms = n_zooms + 1

    # Obtém as dimensões atuais da imagem redimensionada
    width, height = image_current_resize.size

    # Calcula as novas dimensões para o zoom
    new_width = int(width * 1.1)
    new_height = int(height * 1.1)

    # Redimensiona a imagem atual para o zoom
    image_current_resize = image_current_resize.resize(
        (new_width, new_height), Image.LANCZOS)

    # Atualiza a imagem atual e a imagem exibida
    image_current_photo = ImageTk.PhotoImage(image_current_resize)
    label_image.configure(image=image_current_photo)
    label_image.image = image_current_photo


def zoom_out():
    global image_current_resize, image_current_photo, n_zooms

    n_zooms = n_zooms - 1

    # Obtém as dimensões atuais da imagem redimensionada
    width, height = image_current_resize.size

    # Calcula as novas dimensões para o zoom
    new_width = int(width / 1.1)
    new_height = int(height / 1.1)

    # Redimensiona a imagem atual para o zoom
    image_current_resize = image_current_resize.resize(
        (new_width, new_height), Image.LANCZOS)

    # Atualiza a imagem atual e a imagem exibida
    image_current_photo = ImageTk.PhotoImage(image_current_resize)
    label_image.configure(image=image_current_photo)
    label_image.image = image_current_photo


def load_image(image):
    global image_original, image_original_gray, image_original_resize, image_original_photo, image_current_resize, image_current_photo, n_zooms, label_image
    # carrega a imagem
    image_original = Image.open(image)
    image_original_gray = image_original.convert(
        'L')  # converte para escala de cinza
    image_original_resize = image_original_gray.resize(
        (300, 400), Image.LANCZOS)
    image_original_photo = ImageTk.PhotoImage(image_original_resize)

    image_current_resize = image_original_resize
    image_current_photo = image_original_photo

    n_zooms = 0

    # Atualizar o Label com a nova imagem
    label_image.configure(image=image_original_photo)
    # Atualiza a referência da imagem no Label]
    label_image.image = image_original_photo


# Variáveis globais
image_original = None
image_original_gray = None
image_original_resize = None
image_original_photo = None
image_current_resize = None
image_current_photo = None
n_zooms = 0

# cria uma janela
window = Tk()
window.title("Contraste e Zoom")
window.geometry("800x700")
window.resizable(False, False)
window.configure(background="white")

# Cria um widget Label e exibe a imagem na janela
label_image = Label(window, width=800, height=600)
label_image.configure(background="white")
label_image.grid(row=0, column=0, padx=10, pady=10)

load_image("mamografias\DleftCC\d_left_cc (1).png")

# Cria um frame para os botões
frame_buttons = Frame(window)
frame_buttons.configure(background="white")
frame_buttons.grid(row=1, column=0, padx=10, pady=10)

# Cria os controles
button_select = Button(
    frame_buttons, text="Trocar Imagem", command=open_explorer)
button_select.grid(row=0, column=0, padx=5)

min_slider = Scale(frame_buttons, from_=1, to=255,
                   orient='horizontal', label='Valor mínimo')
min_slider.configure(background="white")
min_slider.grid(row=0, column=1, padx=5)

max_slider = Scale(frame_buttons, from_=1, to=255,
                   orient='horizontal', label='Valor máximo')
max_slider.configure(background="white")
max_slider.grid(row=0, column=2, padx=5)

button_windowing = Button(
    frame_buttons, text="Janelamento", command=update_image_windowing)
button_windowing.grid(row=0, column=3, padx=5)

button_zoom_in = Button(frame_buttons, text="Zoom In", command=zoom_in)
button_zoom_in.grid(row=0, column=4, padx=5)

button_zoom_out = Button(frame_buttons, text="Zoom Out", command=zoom_out)
button_zoom_out.grid(row=0, column=5, padx=5)

# Configura a coluna 0 do grid para expandir
window.grid_columnconfigure(0, weight=1)

# Exibe a janela
window.mainloop()
