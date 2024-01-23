import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings("ignore")


def scores_modelos_a_pelo(X_train, y_train, X_val, y_val, **models):
    results = {}
    for model_name, model in models.items():  
        LE = LabelEncoder()
        y_train_enc = LE.fit_transform(y_train)
        y_val_enc = LE.transform(y_val)
        
        print(model_name.upper())
        model.fit(X_train, y_train_enc)
        
        # Calcular Métricas TRAIN   
        prob = model.predict(X_train)
        
        accuracy_train = accuracy_score(y_train_enc, prob)
        precision_train = precision_score(y_train_enc, prob, average='weighted', zero_division=1)
        recall_train = recall_score(y_train_enc, prob, average='weighted')
        f1_train = f1_score(y_train_enc, prob, average='weighted')
        
        # Calcular Métricas VALIDATION
        prob = model.predict(X_val)

        accuracy_val = accuracy_score(y_val_enc, prob)
        precision_val = precision_score(y_val_enc, prob, average='weighted', zero_division=1)
        recall_val = recall_score(y_val_enc, prob, average='weighted')
        f1_val = f1_score(y_val_enc, prob, average='weighted')

        # Guardar resultados en un diccionario
        results[model_name] = {
            'accuracy_train': f"{accuracy_train:.5f}",
            'accuracy_test': f"{accuracy_val:.5f}",
            
            'precision_train': f"{precision_train:.5f}",
            'precision_test': f"{precision_val:.5f}",
            
            'recall_train': f"{recall_train:.5f}",
            'recall_test': f"{recall_val:.5f}",
            
            'f1_train': f"{f1_train:.5f}",
            'f1_test': f"{f1_val:.5f}"
        }
        
    # Obtener las mejores métricas y el modelo a la que corresponde la mejor métrica (FUERA DEL BUCLE FOR, para que me lo muestre una vez haya terminado)
    best_accuracy = [0, None]
    best_precision = [0, None]
    best_recall = [0, None]
    best_f1 = [0, None]

    for model, items in results.items():
        for metric, value in items.items():
            value = float(value)
            if metric == 'accuracy_test':
                if (value) > best_accuracy[0]:
                    best_accuracy = [value, model]
                    
            if metric == 'precision_test':
                if value > best_precision[0]:
                    best_precision = [value, model]
                    
            if metric == 'recall_test':
                if value > best_recall[0]:
                    best_recall = [value, model]
                    
            if metric == 'f1_test':
                if value > best_f1[0]:
                    best_f1 = [value, model]
                    
    print()                
    print('best accuracy:', best_accuracy)
    print('best precision:', best_precision)
    print('best recall:', best_recall)
    print('best f1:', best_f1)
    
    return results