from sklearn.covariance import EllipticEnvelope
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.multiclass import OneVsRestClassifier

from src.utils.os_utils import OSUtils
import os

class MalahanobisClassifier:
    def sklearn_classify(self, data):
        X_train, Y_train, X_test, Y_test = data
        model = OneVsRestClassifier(EllipticEnvelope())
        model.fit(X_train, Y_train)

        # Calcular Mahalanobis distances para dados de treinamento e teste
        predictions_train = model.predict(X_train)
        predictions_test = model.predict(X_test)

        # Calcular acurácia
        accuracy_train = accuracy_score(Y_train, predictions_train)
        accuracy_test = accuracy_score(Y_test, predictions_test)

        # Imprimir a acurácia
        print("Training Accuracy:", accuracy_train)
        print("Testing Accuracy:", accuracy_test)

        # Calculate confusion matrix
        cm_train = confusion_matrix(Y_train, predictions_train)
        cm_test = confusion_matrix(Y_test, predictions_test)

        # Print confusion matrix
        print("Confusion Matrix - Training:")
        print(cm_train)
        print("Confusion Matrix - Testing:")
        print(cm_test)

        metrics_txt = os.path.join(OSUtils.project_images_root, 'metrics.txt')
        if not OSUtils.exist_file(metrics_txt):
            OSUtils.touch(metrics_txt)

        with open(metrics_txt, 'a') as file:
            file.write("Training Accuracy: {}\n".format(accuracy_train))
            file.write("Testing Accuracy: {}\n\n".format(accuracy_test))

            # Write confusion matrix for training
            file.write("Confusion Matrix - Training:\n")
            file.write(str(cm_train) + '\n\n')

            # Write confusion matrix for testing
            file.write("Confusion Matrix - Testing:\n")
            file.write(str(cm_test) + '\n\n')
