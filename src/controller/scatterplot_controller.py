import matplotlib.pyplot as plt

class ScatterplotController:
    @staticmethod
    def generate_scatterplot(class_data, SCATTERPLOT_PATH):
        colors = ['black', 'blue', 'red', 'green', 'orange', 'purple']
        plt.figure(figsize=(10, 6))
        for i, class_value in enumerate(class_data):
            plt.scatter(class_data[class_value]['areas'], class_data[class_value]['eccentricity'], label=class_value, color=colors[i])

        plt.xlabel('Área')
        plt.ylabel('Excentricidade')
        plt.title('Gráfico de Dispersão de Área x Excentricidade')
        plt.legend()

        plt.savefig(SCATTERPLOT_PATH)

        # Exiba o gráfico
        # plt.show()
