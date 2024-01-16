import pandas as pd
import numpy as np
from functions.merge_data import merge_datasets

df_raw = merge_datasets()

def top_courses(N=3, date_DMA=None):
    data_copy = df_raw.copy()
    data_copy['Order Date'] = pd.to_datetime(data_copy['Order Date'])
    
    if date_DMA != None:
        if type(date_DMA) == str:
            data_copy = data_copy[data_copy['Order Date'] >= pd.to_datetime(date_DMA, dayfirst=True)]
        else:
            print('La fecha debe estar en formato string y debe contener esta estructura:')
            print('\tEjemplo: "31/12/2020" (Día/Mes/Año)')
            return
        
    print('Tamaño del dataframe tras el merge:', data_copy.shape)
    
    # Creo la lista con el Top-N courses
    group_topn = data_copy.groupby('Course')['Current Value'].sum()     # Agrupo por curso
    sort_group_topn = group_topn.sort_values(ascending=False)   # Ordeno descendentemente
    top_n_list = sort_group_topn.head(N).index    # Me quedo con el Top-N en formato lista
    
    # Busco qué alumnos han comprado las formaciones Top-N
    for num in range(N):
        values = data_copy.groupby('User ID')['Course'].apply(lambda x: top_n_list[num] in x.values)
        data_copy[f'Has Bought top{num+1}'] = data_copy['User ID'].map(values)
    
    # Filtro el dataframe para quedarme con las filas que contienen algún valor 'True' en las columnas 'Has Bought topN' 
    data_filtered = data_copy[data_copy.loc[:, 'Has Bought top1':].any(axis=1)]     # Filtro por aquellas filas que tengan un True en las columnas Top-N
    group_filtered = data_filtered.groupby('User ID')[data_filtered.loc[:, 'Has Bought top1':].columns].any()   # Agrupo por 'User ID' y me quedo sólo con las columnas Top-N
    
    # Segmento los diccionarios filtrando por aquellos que tiene valor True en la columan Top-N y guardo este dataframe en un diccionario
    dict_groups = {}
    for num in range(N):
        # Filtro por cada columna Top-N y me quedo con las filas que contienen el valor TRUE
        true_one_column = group_filtered[group_filtered[f'Has Bought top{num+1}']==True]
        
        # Aplico filtrados a la data
        users_top = data_filtered[data_filtered['User ID'].isin(true_one_column.index)]     # En la data principal, me quedo con los Users que tienen el valor TRUE
        users_top = users_top.sort_values(by=['User ID', 'Order Date'])
        users_top = users_top.reset_index(drop=True)
        users_top = users_top.iloc[:, :-N]
        
        # Creo una columna que cuente el cúmulo de cursos que ha comprado un usuario
        loc_col = users_top.columns.get_loc('Order Date')
        user_cum  = users_top.groupby('User ID')['Course'].cumcount()+1
        users_top.insert(loc_col + 1, f'Cum Bought top{num+1}', user_cum)

        # Me quedo con las filas de Top-N para obtener la posición en la que el usuario compró el curso TOP
        top_n_users = users_top[users_top['Course'] == top_n_list[num]]
        result = top_n_users.groupby('User ID')[f'Cum Bought top{num+1}'].max()
        top_n_id = users_top['User ID'].map(result)
        users_top.insert(loc_col + 2, f'Top{num+1} Bought Position', top_n_id)

        # Encuentro la posición (de la secuencia de compra) en el que se encuentra el curso TOP por cada alumno
        top_n_indices = users_top[users_top['Course'] == top_n_list[num]]
        top_n_indices = top_n_indices.groupby('User ID')[f'Top{num+1} Bought Position'].max()
    
        # Bucle para obtener la secuencia de compra del alumno tras comprar el curso TOP
        for user_id, quantity in top_n_indices.items():
            # Obtener los siguientes cursos tras la compra del curso TOP (si lo hay)
            course1 = users_top.loc[(users_top['User ID'] == user_id) & (users_top[f'Cum Bought top{num+1}'] == quantity + 1), 'Course']
            course2 = users_top.loc[(users_top['User ID'] == user_id) & (users_top[f'Cum Bought top{num+1}'] == quantity + 2), 'Course']
            course3 = users_top.loc[(users_top['User ID'] == user_id) & (users_top[f'Cum Bought top{num+1}'] == quantity + 3), 'Course']
            
            # Asignar la posición de la secuencia a los cursos que se compraron tras el curso top (si lo hay) 
            if not course1.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_1 Course'] = course1.values[0]
                
            if not course2.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_2 Course'] = course2.values[0]
                
            if not course3.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_3 Course'] = course3.values[0]
                
     
        # Filtro el cúmulo de compras que es igual o superior a la posición en la que se encuentra la compra del curso TOP en la secuencia
        users_top = users_top[(users_top[f'Cum Bought top{num+1}']>=users_top[f'Top{num+1} Bought Position'])]
        
        # Añado la diferencia de días entre el curso de la secuencia y el curso top
        for n in range(3):
            diff = users_top[(users_top[f'Cum Bought top{num+1}']==users_top[f'Top{num+1} Bought Position']) | (users_top[f'Cum Bought top{num+1}'] == users_top[f'Top{num+1} Bought Position'] + (n + 1))]
            diff = diff.groupby('User ID')['Order Date'].diff().dt.days
            loc_col = users_top.columns.get_loc(f'Next_{n+1} Course')
            users_top.insert(loc_col + 1, f'Diff{n+1}', diff)

        # Agrupar por << User ID >> y obtener los cursos que le corresponden a cada usuario tras comprar el curso TOP
        grouped_top = users_top.groupby('User ID')[['Next_1 Course', 'Diff1', 'Next_2 Course', 'Diff2', 'Next_3 Course', 'Diff3', 'Course']].agg(lambda x: x.unique().tolist()[-1])
        grouped_top = grouped_top.rename({'Course': 'Last Course'}, axis=1)
        grouped_top = grouped_top.replace({'nan': np.nan})
        grouped_top = grouped_top.dropna(subset='Next_1 Course')
        grouped_top[['Diff1', 'Diff2', 'Diff3']] = grouped_top[['Diff1', 'Diff2', 'Diff3']].fillna(0)
        grouped_top[['Diff1', 'Diff2', 'Diff3']] = grouped_top[['Diff1', 'Diff2', 'Diff3']].astype(int)
        grouped_top = grouped_top.reset_index()
        
        print(f'Tamaño del dataframe tras la transformación Top-{num+1}:', grouped_top.shape)

        # Añadir el curso top en una columna
        grouped_top.insert(1, 'Top Course', top_n_list[num])

        # Añadir los dataframes al diccionario
        dict_groups.setdefault(f'top{num+1}', grouped_top)
        

    return dict_groups
