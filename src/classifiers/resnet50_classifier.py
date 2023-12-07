from keras.applications.resnet50 import ResNet50
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, accuracy_score
from src.utils.os_utils import OSUtils
import os
import numpy as np

class Restnet50Classifier:
    def __init__(self, train_data_path, test_data_path):
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path

    def build_binary_model(self):
        base_model = ResNet50(weights='imagenet', include_top=False)
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        predictions = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        return model

    def build_multiclass_model(self, num_classes):
        base_model = ResNet50(weights='imagenet', include_top=False)
        y = base_model.output
        y = GlobalAveragePooling2D()(y)
        y = Dense(1024, activation='relu')(y)
        predictions = Dense(num_classes, activation='softmax')(y)
        model = Model(inputs=base_model.input, outputs=predictions)
        return model

    def train_model(self, model, class_mode, batch_size=32, epochs=10):
        train_datagen = ImageDataGenerator(rescale=1./255)
        validation_datagen = ImageDataGenerator(rescale=1./255)

        train_generator = train_datagen.flow_from_directory(
            self.train_data_path,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode=class_mode
        )

        validation_generator = validation_datagen.flow_from_directory(
            self.test_data_path,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode=class_mode
        )

        model.compile(optimizer='adam', loss='binary_crossentropy' if class_mode == 'binary' else 'categorical_crossentropy', metrics=['accuracy'])
        history = model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // batch_size
        )

        validation_generator.reset()  # Resetar o gerador
        predictions = model.predict(validation_generator, steps=validation_generator.samples // batch_size)

        # Para classificação binária
        if class_mode == 'binary':
            predicted_labels = (predictions > 0.5).astype(int)
            true_labels = validation_generator.classes
        # Para classificação multiclasse
        else:
            predicted_labels = np.argmax(predictions, axis=1)
            true_labels = validation_generator.classes

        # Calculando a Matriz de Confusão e Acurácia
        conf_matrix = confusion_matrix(true_labels, predicted_labels)
        accuracy = accuracy_score(true_labels, predicted_labels)

        # Exibindo os resultados
        print("Matriz de Confusão:")
        print(conf_matrix)
        print(f"Acurácia: {accuracy * 100:.2f}%")

        metrics_txt = os.path.join(OSUtils.project_images_root, 'metrics.txt')
        if not OSUtils.exist_file(metrics_txt):
            OSUtils.touch(metrics_txt)

        with open(metrics_txt, 'a') as file:
            file.write(f"Resnet50 - {class_mode}")
            file.write("Testing Accuracy: {}\n\n".format(accuracy))
            file.write("Confusion Matrix - Testing:\n")
            file.write(str(conf_matrix) + '\n\n')

        return history, conf_matrix, accuracy
