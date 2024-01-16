import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

c_med = '#008B8B'


def top_courses(data):
    # Creo el dataset ordenado por Usuario y Fecha
    data_top3 = data.sort_values(by=['User ID', 'Order Date'])
    data_top3 = data_top3.reset_index(drop=True)

    # Creo la lista de los tres cursos que más han facturado
    top10_facturacion = data.groupby('Course')['Current Value'].sum()
    list_top3 = top10_facturacion.sort_values(ascending=False).head(3).index

    # Busco qué alumnos han comprado la formación top1, top2 y top2 de facturación
    data_top3['Has Bought top1'] = data_top3.groupby('User ID')['Course'].transform(lambda x: list_top3[0] in x.values)
    data_top3['Has Bought top2'] = data_top3.groupby('User ID')['Course'].transform(lambda x: list_top3[1] in x.values)
    data_top3['Has Bought top3'] = data_top3.groupby('User ID')['Course'].transform(lambda x: list_top3[2] in x.values)

    # Me quedo sólo con aquellos alumnos que han comprado al menos uno de estos cursos
    condition = ((data_top3['Has Bought top1']==True) | (data_top3['Has Bought top2']==True) | (data_top3['Has Bought top3']==True))
    data_top3 = data_top3[condition]
    
    # Agrupo por usuarios
    group_top_courses = data_top3.groupby('User ID')[['Has Bought top1', 'Has Bought top2', 'Has Bought top3']].any()

    # Creo diferentes dataframes dependiendo del curso que han comprado
    group_top1 = group_top_courses[group_top_courses['Has Bought top1']==True]
    group_top2 = group_top_courses[group_top_courses['Has Bought top2']==True]
    group_top3 = group_top_courses[group_top_courses['Has Bought top3']==True]
    
    dict_groups = {}
    list_groups = [group_top1, group_top2, group_top3]
    for n, groups in enumerate(list_groups, start=1):
        # Creo el dataframe con aquellos usuarios que compraron el curso TOP
        users_top = data_top3[data_top3['User ID'].isin(groups.index)].reset_index(drop=True)
        users_top = users_top.sort_values(by=['User ID', 'Order Date'])
        users_top = users_top.iloc[:, :-3]

        # Creo una columna que cuente el cúmulo de curso que ha comprado un usuario
        loc_col = users_top.columns.get_loc('User ID')
        users_top.insert(loc_col + 1, f'Cum Bought top{n}', users_top.groupby('User ID')['Course'].cumcount()+1)

        # Me quedo con las filas de SVA para obtener la posición en la que el usuario compró el curso TOP
        sva_users = users_top[users_top['Course'] == list_top3[n - 1]]
        result = sva_users.groupby('User ID')[f'Cum Bought top{n}'].max()
        sva_id = users_top['User ID'].map(result)
        loc_col = users_top.columns.get_loc(f'Cum Bought top{n}')
        users_top.insert(loc_col + 1, f'Top{n} Bought Position', sva_id)

        # Encontrar los índices de las filas donde se encuentra el curso TOP
        sva_indices = users_top[users_top['Course'] == list_top3[n - 1]]
        sva_indices = sva_indices.groupby('User ID')[f'Top{n} Bought Position'].max()

        for user_id, num in sva_indices.items():
            # Obtener los siguientes cursos tras la compra del curso TOP (si lo hay)
            course1 = users_top.loc[(users_top['User ID'] == user_id) & (users_top[f'Cum Bought top{n}'] == num + 1), 'Course']
            course2 = users_top.loc[(users_top['User ID'] == user_id) & (users_top[f'Cum Bought top{n}'] == num + 2), 'Course']
            course3 = users_top.loc[(users_top['User ID'] == user_id) & (users_top[f'Cum Bought top{n}'] == num + 3), 'Course']
            
            # (si lo hay) Asignar la posición de los cursos siguientes a la compra del curso top 
            if not course1.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_1 Course'] = course1.values[0]
                
            if not course2.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_2 Course'] = course2.values[0]
                
            if not course3.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_3 Course'] = course3.values[0]

        # Agrupar por << User ID >> y obtener los cursos que le corresponden a cada usuario tras comprar el curso TOP
        grouped_top = users_top.groupby('User ID')[['Next_1 Course', 'Next_2 Course', 'Next_3 Course', 'Course']].agg(lambda x: x.unique().tolist()[-1])
        grouped_top = grouped_top.rename({'Course': 'Last Course'}, axis=1)
        grouped_top = grouped_top.replace({'nan': np.nan})
        grouped_top = grouped_top.reset_index()
        
        # Añadir el curso top en una columna
        grouped_top.insert(1, 'Top Course', list_top3[n -1])
        
        # Añadir los dataframes al diccionario
        dict_groups[f'top{n}'] = grouped_top
        
    top1 = dict_groups['top1']
    top2 = dict_groups['top2']
    top3 = dict_groups['top3']

    # Plotear los gráficos
    lista_top = [top1, top2, top3]
    for num, top in enumerate(lista_top, start=1):
        title = top['Top Course'].unique()[0]
        Next_1 = top[top['Next_1 Course']!=title].dropna(subset='Next_1 Course')['Next_1 Course'].value_counts(ascending=False).head(3)
        Next_2 = top[top['Next_2 Course']!=title].dropna(subset='Next_2 Course')['Next_2 Course'].value_counts(ascending=False).head(3)
        Next_3 = top[top['Next_3 Course']!=title].dropna(subset='Next_3 Course')['Next_3 Course'].value_counts(ascending=False).head(3)


        fig, axs = plt.subplots(1, 3, figsize=(18, 5))

        plt.suptitle(f'Curso TOP{num}: {title}'.title(), fontsize=24, fontweight='bold', y=1.15)

        # Gráfico1
        Next_1.plot(kind='bar', xlabel='', color=c_med, ax=axs[0])
        axs[0].set_xticks(axs[0].get_xticks())
        axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45, ha='right')
        axs[0].set_ylabel('Cuenta', labelpad=15)
        axs[0].set_title(f'Top{num} Next_1'.title(), fontweight='bold', y=1.05)
        axs[0].grid(axis='y', alpha=0.25);

        # Gráfico2
        Next_2.plot(kind='bar', xlabel='', color=c_med, ax=axs[1])
        axs[1].set_xticks(axs[1].get_xticks())
        axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45, ha='right')
        axs[1].set_ylabel('Cuenta', labelpad=15)
        axs[1].set_title(f'Top{num} Next_2'.title(), fontweight='bold', y=1.05)
        axs[1].grid(axis='y', alpha=0.25);

        # Gráfico3
        Next_3.plot(kind='bar', xlabel='', color=c_med, ax=axs[2])
        axs[2].set_xticks(axs[2].get_xticks())
        axs[2].set_xticklabels(axs[2].get_xticklabels(), rotation=45, ha='right')
        axs[2].set_ylabel('Cuenta', labelpad=15)
        axs[2].set_title(f'Top{num} Next_3'.title(), fontweight='bold', y=1.05)
        axs[2].grid(axis='y', alpha=0.25);