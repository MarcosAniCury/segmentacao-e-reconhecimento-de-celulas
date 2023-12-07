import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

def plot_confusion_matrix(cm, classes):
    # Criação da janela principal
    root = tk.Tk()
    root.title("Matriz de Confusão")

    # Função para plotar a matriz de confusão
    def plot():
        plt.figure(figsize=(6, 4))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Matriz de Confusão')
        plt.colorbar()

        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes)
        plt.yticks(tick_marks, classes)

        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], 'd'),
                         ha="center", va="center",
                         color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('Valores Verdadeiros')
        plt.xlabel('Valores Previstos')

        plt.show()

    # Botão para mostrar o gráfico
    plot_button = tk.Button(root, text="Mostrar Matriz de Confusão", command=plot)
    plot_button.pack()

    # Iniciando a interface gráfica
    root.mainloop()

# Exemplo de uso:
# Suponha que você tem sua matriz de confusão e classes
confusion_matrix = np.array([[15, 2], [3, 10]])  # Substitua pela sua matriz de confusão
class_names = ["Classe 0", "Classe 1"]  # Substitua pelos nomes de suas classes reais

# Chame a função com a matriz de confusão e os nomes das classes
plot_confusion_matrix(confusion_matrix, class_names)
