from tkinter import *
import subprocess


def windowing_screen():
    global window
    # Função a ser executada quando o botão "Contraste e Zoom" for clicado
    window.grab_set()  # Desabilitar a interação com a janela principal
    subprocess.Popen(["python", "ScreenWindowing.py"])
    window.wait_window()  # Aguardar até que a nova janela seja fechada
    window.grab_release()  # Reativar a interação com a janela principal


def cnn_screen():
    global window
    # Função a ser executada quando o botão "Contraste e Zoom" for clicado
    window.grab_set()  # Desabilitar a interação com a janela principal
    subprocess.Popen(["python", "ScreenCnn.py"])
    window.wait_window()  # Aguardar até que a nova janela seja fechada
    window.grab_release()  # Reativar a interação com a janela principal


# Criação da janela principal
window = Tk()

# Configuração da janela
window.title("Processamento e Análise de Mama")
window.geometry("500x300")
window.resizable(False, False)
window.configure(background="white")

# Criação do título centralizado
title = Label(window, text="Processamento e Análise de Mama",
              font=("Helvetica", 20, "bold"))
title.grid(row=0, column=0, columnspan=3, pady=20)
title.configure(background="white")

# Criação dos botões
button_windowing = Button(window, text="Contraste e Zoom",
                          command=windowing_screen, height=2, font=("Helvetica", 14))
button_windowing.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")
button_cnn = Button(window, text="CNN", command=cnn_screen,
                    height=2, font=("Helvetica", 14))
button_cnn.grid(row=1, column=2, padx=(10, 20), pady=10, sticky="ew")

# Criação do footer
footer = Label(window, text="", font=("Helvetica", 12))
footer.grid(row=2, column=0, columnspan=3, pady=20)

# Configurar o alinhamento dos itens na grade
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Iniciar o loop principal da janela
window.mainloop()
