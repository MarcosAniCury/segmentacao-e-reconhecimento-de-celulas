from tkinter import ttk, Tk, Frame, Label, Button, StringVar
from CodeExecute import runCnn
import os


def show_unsegmented_binary_text():
    global label_text, switch_var
    arquive_name = 'binarie_no_segment'
    # Testar novamente
    if switch_var.get() == "Sim":
        runCnn(True, True, False, arquive_name)
    # Função para exibir o texto não segmentado binário
    text = read_file(f"resultados/{arquive_name}.txt")
    label_text.configure(text=text)


def show_segmented_binary_text():
    global label_text, switch_var
    arquive_name = 'binarie_segment'
    # Testar novamente
    if switch_var.get() == "Sim":
        runCnn(True, True, True, arquive_name)
    # Função para exibir o texto segmentado binário
    text = read_file(f"resultados/{arquive_name}.txt")
    label_text.configure(text=text)


def show_unsegmented_multiclass_text():
    global label_text, switch_var
    arquive_name = 'mult_class_no_segment'
    # Testar novamente
    if switch_var.get() == "Sim":
        runCnn(False, True, False, arquive_name)
    # Função para exibir o texto não segmentado multiclasse
    text = read_file(f"resultados/{arquive_name}.txt")
    label_text.configure(text=text)


def show_segmented_multiclass_text():
    global label_text, switch_var
    arquive_name = 'mult_class_segment'
    # Testar novamente
    if switch_var.get() == "Sim":
        runCnn(False, True, True, arquive_name)
    # Função para exibir o texto segmentado multiclasse
    text = read_file(f"resultados/{arquive_name}.txt")
    label_text.configure(text=text)


def read_file(file_path):
    # Função para ler o conteúdo de um arquivo
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return ""


window = Tk()

window.title("Tela CNN")
window.geometry("600x500")
window.resizable(False, False)
window.configure(background="white")

frame_text = Frame(window, width=500, height=200)
frame_text.configure(background="white")
frame_text.grid(row=1, column=0, pady=10)

label_text = Label(frame_text, text="", font=("Arial", 14))
label_text.configure(background="white")
label_text.grid(row=0, column=0, pady=10)

frame_buttons = Frame(window, width=500, height=100)
frame_buttons.configure(background="white")
frame_buttons.grid(row=0, column=0, pady=10)

button_unsegmented_binary = Button(
    frame_buttons, text="Binário Não Segmentado", command=show_unsegmented_binary_text)
button_unsegmented_binary.grid(row=0, column=0, padx=5)

button_segmented_binary = Button(
    frame_buttons, text="Binário Segmentado", command=show_segmented_binary_text)
button_segmented_binary.grid(row=0, column=1, padx=5)

button_unsegmented_multiclass = Button(
    frame_buttons, text="Multiclasse Não Segmentado", command=show_unsegmented_multiclass_text)
button_unsegmented_multiclass.grid(row=0, column=2, padx=5)

button_segmented_multiclass = Button(
    frame_buttons, text="Multiclasse Segmentado", command=show_segmented_multiclass_text)
button_segmented_multiclass.grid(row=0, column=3, padx=5)

frame_buttons.grid_rowconfigure(0, weight=1)
frame_buttons.grid_columnconfigure(0, weight=1)
frame_buttons.grid_columnconfigure(1, weight=1)
frame_buttons.grid_columnconfigure(2, weight=1)
frame_buttons.grid_columnconfigure(3, weight=1)

frame_switch = Frame(window, width=500, height=50)
frame_switch.configure(background="white")
frame_switch.grid(row=2, column=0, pady=10)

label_switch = Label(frame_switch, text="Testar treino?:", font=("Arial", 14))
label_switch.configure(background="white")
label_switch.grid(row=0, column=0, padx=5, sticky="e")

switch_var = StringVar(value="Não")
switch = ttk.Combobox(frame_switch, textvariable=switch_var, values=[
                      "Não", "Sim"], state="readonly")
switch.grid(row=0, column=1, padx=5, sticky="w")

window.mainloop()
