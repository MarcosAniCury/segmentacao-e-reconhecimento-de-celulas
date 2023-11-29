import os
import shutil

# Função para copiar uma imagem para o diretório de destino


def copy_image(source, destination):
    os.makedirs(destination, exist_ok=True)
    shutil.copy2(source, destination)

# Retorna um index que indentifica para qual pasta a imagem será salva


def select_image_class(character, is_binary_class=False):
    if is_binary_class:
        if character == 'd' or character == 'e':
            return 0
        elif character == 'f' or character == 'g':
            return 1
    else:
        if character == 'd':
            return 0
        elif character == 'e':
            return 1
        elif character == 'f':
            return 2
        elif character == 'g':
            return 3


def delete_folder(train_dir, test_dir):
    shutil.rmtree(train_dir)
    shutil.rmtree(test_dir)

# Separa as imagens de treino e de teste


def folder_separate_image(is_binarie_class):
    # Caminhos dos diretórios para as imagens de treino e teste
    train_dir = "treino"
    test_dir = "teste"

    delete_folder(train_dir, test_dir)

    class_dir = []

    if is_binarie_class:
        class_dir = ["BIRADS_1_2", "BIRADS_3_4"]
    else:
        class_dir = ["BIRADS_1", "BIRADS_2", "BIRADS_3", "BIRADS_4"]

    # Diretório principal onde estão localizadas as imagens de mamografias
    image_dir = "mamografias"

    # Percorrer todas as pastas dentro do diretório de mamografias
    for dirpath, dirnames, filenames in os.walk(image_dir):
        for arquive in filenames:
            if arquive.endswith(".png") or arquive.endswith(".jpg") or arquive.endswith(".jpeg"):
                filename, extension = os.path.splitext(arquive)
                # Extrair o número entre parênteses
                number = filename.split("(")[-1].split(")")[0]
                caracter = filename[0]
                index_folder_class = select_image_class(
                    caracter, is_binarie_class)
                if number.isdigit():
                    number = int(number)
                    origin_image = os.path.join(dirpath, arquive)
                    if number % 4 == 0:
                        copy_image(origin_image, os.path.join(
                            test_dir, class_dir[index_folder_class]))
                    else:
                        copy_image(origin_image, os.path.join(
                            train_dir, class_dir[index_folder_class]))


def file_write(arquive_name, execution_time, metrics, is_binarie_class=False):
    # Abra o arquive no modo de escrita
    arquive = open(f"resultados/{arquive_name}.txt", 'w')

    if is_binarie_class:
        arquive.write(f"Tempo de execucao do codigo: {execution_time}\n")
        arquive.write(f"Sensitivity Recall: {metrics['recall']}\n")
        arquive.write(f"Specificity Specificity: {metrics['specificity']}\n")
        arquive.write(f"Specificity Precision: {metrics['precision']}\n")
        arquive.write(f"Acurracy: {metrics['accuracy']}\n")
        arquive.write(f"F1-Score: {metrics['f1-score']}\n")

    else:
        # Escreva algumas linhas no arquive
        arquive.write(f"Tempo de execucao do codigo: {execution_time}\n")
        arquive.write(f"Sensitivity Recall: {metrics['recall']}\n")
        arquive.write(f"Specificity Specificity: {metrics['specificity']}\n")
        arquive.write(f"Matrix Confusion: {metrics['matrix']}\n")

    # Feche o arquive
    arquive.close()
