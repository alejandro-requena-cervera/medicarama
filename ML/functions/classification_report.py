import numpy as np
import pandas as pd
from sklearn.metrics import classification_report


def best_classification_report(model, X_test, y_test):
    pred = model.predict(X_test)
    cr = classification_report(y_test, pred, zero_division=0.0, output_dict=True)

    predice_mal = []
    predice_bien = {}

    for classes, columns in cr.items():
        if type(columns) != dict:
            continue
        
        precision = columns['precision']
        recall = columns['recall']
        f1_score = columns['f1-score']
        support = columns['support']

        if (precision==0.0) & (recall==0.0) & (f1_score==0.0):
            predice_mal.append(classes)
            continue
        
        predice_bien[classes] = {
            'Precision': round(precision, 2),
            'Recall': round(recall, 2),
            'F1-Score': round(f1_score, 2),
            'Support': int(support)
        }
        
    df = pd.DataFrame(predice_bien).T
    
    return predice_mal, df



def acierto_3probs_mas_altas(model, X_test, y_test):
    clase_target = model.classes_
    pred = model.predict_proba(X_test)
    index_target = (-pred).argsort(axis=1)[:, :3]
    pred_target = clase_target[index_target]

    dict_target = {
        'acierto': {
            'cantidad': 0,
            'primera_pos': 0,
            'segunda_pos': 0,
            'tercera_pos': 0
        },
        'error': 0,
        'total': 0
    }

    for prob, target in zip(pred_target, y_test):
        dict_target['total'] += 1
        # Verifica si el target está presente en el array prob
        if np.any(prob == target):
            dict_target['acierto']['cantidad'] += 1
            
            # Encuentra los índices donde el target coincide con el array prob
            indices = np.where(prob == target)[0]
            
            # Actualiza los conteos de posición si se encuentra el índice
            if len(indices) > 0:
                indice = indices[0]
                if indice == 0:
                    dict_target['acierto']['primera_pos'] += 1
                elif indice == 1:
                    dict_target['acierto']['segunda_pos'] += 1
                elif indice == 2:
                    dict_target['acierto']['tercera_pos'] += 1
        else:
            dict_target['error'] += 1
            
    dict_target['%acierto'] = round(dict_target['acierto']['cantidad'] / dict_target['total'], 2)

    return dict_target