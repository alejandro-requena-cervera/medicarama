import pandas as pd
import numpy as np

def output_preds_model(model, data):
    X_test = data.iloc[:, :-1]
    probabilities_test = model.predict_proba(X_test)

    proba_class = abs(np.sort(-probabilities_test)[:, :3])
    class_names = model.classes_   # Obtengo el nombre de todas las clases del Target
    top_3_index_classes = (-probabilities_test).argsort(axis=1)[:, :3] # El método ``argsort()`` me devuelve el índice (un max de 49) en el que se encuentran las tres probabilidades más altas (por ello no es un valor negativo lo que me devuelve, sino dónde se encuentran estos números)
    top_3_class_names = class_names[top_3_index_classes]
    user_id = data['User ID']

    df = pd.DataFrame()
    for n, (id, preds) in enumerate(zip(user_id, top_3_class_names)):
        proba1 = round(proba_class[n][0], 2)
        proba2 = round(proba_class[n][1], 2)
        proba3 = round(proba_class[n][2], 2)
        df_prov = pd.DataFrame({
            'id': [id],
            'T1': [preds[0]],
            'proba_T1': [proba1],
            'T2': [preds[1]],
            'proba_T2': [proba2],
            'T3': [preds[2]],
            'proba_T3': [proba3],
            'proba_total': [proba1 + proba2 + proba3],
        })
        
        df = pd.concat((df, df_prov), axis=0).reset_index(drop=True)
    
    df = df.set_index('id')
    df = df.sort_values(by='proba_total', ascending=False)
    
    return df