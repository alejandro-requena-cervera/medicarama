import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings("ignore")



def train_test_score(model, X_trainset, X_testset, y_trainset, y_testset, validation=False, baseline_accuracy=None):
    """
    Entrena un modelo y evalúa sus métricas de rendimiento en los conjuntos de entrenamiento y prueba.

    Parameters:
    - model: Modelo de clasificación entrenado.
    - X_trainset: Conjunto de características de entrenamiento.
    - X_testset: Conjunto de características de prueba.
    - y_trainset: Etiquetas de clase correspondientes al conjunto de entrenamiento.
    - y_testset: Etiquetas de clase correspondientes al conjunto de prueba.
    - validation (bool): Indica si se está realizando una evaluación en un conjunto de validación.
    - baseline_accuracy (float): Precisión de referencia para comparar con la precisión del modelo.

    Returns:
    - dict: Diccionario que contiene las probabilidades y clases de las tres clases más probables para cada muestra en el conjunto de prueba.
    - float: Precisión del modelo en el conjunto de prueba.

    Note: It is not necessary to return the trained model within the function because it is already trained within the function.
    When calling the model again, it will be trained even if it is not returned from the function.
    """
    
    model.fit(X_trainset, y_trainset)
    
    # Calcular Métricas TRAIN
    probabilities_train = model.predict_proba(X_trainset)
    predicted_index_classes = probabilities_train.argmax(axis=1)
    predicted_classes = model.classes_[predicted_index_classes]

    accuracy_train = accuracy_score(y_trainset, predicted_classes)
    precision_train = precision_score(y_trainset, predicted_classes, average='weighted', zero_division=1)
    recall_train = recall_score(y_trainset, predicted_classes, average='weighted')
    f1_train = f1_score(y_trainset, predicted_classes, average='weighted')
    
    # Calcular Métricas TEST
    probabilities_test = model.predict_proba(X_testset)
    predicted_index_classes = probabilities_test.argmax(axis=1)
    predicted_classes = model.classes_[predicted_index_classes]

    accuracy_test = accuracy_score(y_testset, predicted_classes)
    precision_test = precision_score(y_testset, predicted_classes, average='weighted', zero_division=1)
    recall_test = recall_score(y_testset, predicted_classes, average='weighted')
    f1_test = f1_score(y_testset, predicted_classes, average='weighted')

    # Imprimir por pantalla las métricas
    if validation is not False:
        text = 'VALIDATION'
    else:
        text = 'TEST'
    
    if baseline_accuracy is not None:
        print(f"Accuracy {text} -- Modelo Anterior: {baseline_accuracy}")
    
    print(f"Accuracy TRAIN: {accuracy_train:.5f}")
    print(f"Accuracy {text}: {accuracy_test:.5f}", end='\n\n')
    print(f"Precision TRAIN: {precision_train:.5f}")
    print(f"Precision {text}: {precision_test:.5f}", end='\n\n')
    print(f"Recall TRAIN: {recall_train:.5f}")
    print(f"Recall {text}: {recall_test:.5f}", end='\n\n')
    print(f"F1-score TRAIN: {f1_train:.5f}")
    print(f"F1-score {text}: {f1_test:.5f}", end='\n\n')
    
    # Obtener las probabilidades más altas de TEST
    top_3_probabilities = abs(np.sort((-probabilities_test), axis=1)[:, :3])  # negativo para ordenar ""descendentemente"" (ordena ascendentemente, solo que me convierte el valor a negativo) -- Me devuelve el valor de las tres probabilidades más altas (no el índice)

    # Obtener las clases correspondientes de las probabilidades más altas de TEST
    class_names = model.classes_   # Obtengo el nombre de todas las clases del Target
    top_3_index_classes = (-probabilities_test).argsort(axis=1)[:, :3] # El método ``argsort()`` me devuelve el índice (un max de 49) en el que se encuentran las tres probabilidades más altas (por ello no es un valor negativo lo que me devuelve, sino dónde se encuentran estos números)
    top_3_class_names = class_names[top_3_index_classes]  # ``top_3_classes`` es un array... con los índices (un max de 49 porque es el número de clases en target), lo que me encuentra la clase correspondiente

    # Mostrar las clases y sus probabilidades correspondientes para las tres clases más altas de TEST
    dict_model_proba = {}
    for i in range(len(top_3_probabilities)):
        dict_model_proba[f'Muestra {i + 1}'] = {
            'Top_1': {
                'Clase': top_3_class_names[i][0],
                'Proba': top_3_probabilities[i][0],
            },
            'Top_2': {
                'Clase': top_3_class_names[i][1],
                'Proba': top_3_probabilities[i][1],
            },
            'Top_3': {
                'Clase': top_3_class_names[i][2],
                'Proba': top_3_probabilities[i][2],
            },
        }
        
    return dict_model_proba, round(accuracy_test, 5)


if __name__ == '__main__':
    pass