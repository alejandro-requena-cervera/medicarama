import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

c_med = '#008B8B'

def times(data):
    # Creo el dataset ordenado por Usuario y Fecha
    data_top3 = data.sort_values(by=['User ID', 'Order Date'])
    data_top3 = data_top3.reset_index(drop=True)

    # Añado la columna que indica la diferencia de días
    series_diff_fechas = data_top3.groupby('User ID')['Order Date'].diff().dt.days
    loc_col = data_top3.columns.get_loc('Order Date')
    data_top3.insert(loc_col + 1, 'Diff Days', series_diff_fechas)
    data_top3['Diff Days'] = data_top3['Diff Days'].fillna(0)
    data_top3['Diff Days'] = data_top3['Diff Days'].astype(int)

    # Elimino las filas con valores == 0
    diff_days = data_top3[data_top3['Diff Days']!=0]['Diff Days']

    # Creo dataframe del Series de Diff_Days y creo una columna decodificada con np.select
    df_diff_days = diff_days.to_frame()

    conditions = [(diff_days == 1),
                ((diff_days > 1) & (diff_days <= 7)),
                ((diff_days > 7) & (diff_days <= 30)),    # No se "chafa" con la opción de '1 semana', es decir, 'dentro de 1 mes' significa: "entre 1 semana y 1 mes"
                ((diff_days > 30) & (diff_days <= 90)),
                ((diff_days > 90) & (diff_days <= 180)),
                ((diff_days > 180) & (diff_days <= 365)),
                ((diff_days > 365) & (diff_days <= 730)),
                (diff_days > 730),
                ]
    options = ['1 día', '1 semana', 'Dentro de 1 mes', 'Entre 1 y 3 meses', 'Entre 3 y 6 meses', 'Entre 6 y 12 meses', 'Entre 1 y 2 años', 'Más de 2 años']
    df_diff_days['Range'] = np.select(conditions, options, default=0)

    # Creo la lista de los tres cursos que más han facturado
    top10_facturacion = data.groupby('Course')['Current Value'].sum()
    list_top3 = top10_facturacion.sort_values(ascending=False).head(3).index

    

    data_buy_top3 = data_top3.copy()
    # Busco qué alumnos han comprado la formación top1, top2 y top2 de facturación
    data_buy_top3['Has Bought top1'] = data_buy_top3.groupby('User ID')['Course'].transform(lambda x: list_top3[0] in x.values)
    data_buy_top3['Has Bought top2'] = data_buy_top3.groupby('User ID')['Course'].transform(lambda x: list_top3[1] in x.values)
    data_buy_top3['Has Bought top3'] = data_buy_top3.groupby('User ID')['Course'].transform(lambda x: list_top3[2] in x.values)

    # Me quedo sólo con aquellos alumnos que han comprado al menos uno de estos cursos
    condition = ((data_buy_top3['Has Bought top1']==True) | (data_buy_top3['Has Bought top2']==True) | (data_buy_top3['Has Bought top3']==True))
    data_buy_top3 = data_buy_top3[condition]
    
    # Agrupo por usuarios
    group_top_courses = data_buy_top3.groupby('User ID')[['Has Bought top1', 'Has Bought top2', 'Has Bought top3']].any()

    # Creo diferentes dataframes dependiendo del curso que han comprado
    group_top1 = group_top_courses[group_top_courses['Has Bought top1']==True]
    group_top2 = group_top_courses[group_top_courses['Has Bought top2']==True]
    group_top3 = group_top_courses[group_top_courses['Has Bought top3']==True]
    
    dict_groups = {}
    list_groups = [group_top1, group_top2, group_top3]
    for n, groups in enumerate(list_groups, start=1):
        # Creo el dataframe con aquellos usuarios que compraron el curso TOP
        users_top = data_buy_top3[data_buy_top3['User ID'].isin(groups.index)].reset_index(drop=True)
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
            
            # (si lo hay) Asignar los cursos siguientes a la compra del curso top2 a su posición
            if not course1.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_1 Course'] = course1.values[0]
                
            if not course2.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_2 Course'] = course2.values[0]
                
            if not course3.empty:
                users_top.loc[users_top['User ID'] == user_id, 'Next_3 Course'] = course3.values[0]
                
        # Añadir el curso TOP en una columna
        loc_col = users_top.columns.get_loc('Next_1 Course')
        users_top.insert(loc_col, 'Top Course', list_top3[n -1])
        
        # Filtro para obtener los cursos a partir de que se compró el curso TOP
        users_top = users_top[(users_top[f'Cum Bought top{n}']>=users_top[f'Top{n} Bought Position'])]

        # Diff1
        diff1 = users_top[(users_top[f'Cum Bought top{n}']==users_top[f'Top{n} Bought Position']) | (users_top[f'Cum Bought top{n}'] == users_top[f'Top{n} Bought Position'] + 1)]
        diff1 = diff1.groupby('User ID')['Order Date'].diff().dt.days
        loc_col = users_top.columns.get_loc('Next_1 Course')
        users_top.insert(loc_col + 1, 'Diff1', diff1)

        # Diff2
        diff2 = users_top[(users_top[f'Cum Bought top{n}']==users_top[f'Top{n} Bought Position']) | (users_top[f'Cum Bought top{n}'] == users_top[f'Top{n} Bought Position'] + 2)]
        diff2 = diff2.groupby('User ID')['Order Date'].diff().dt.days
        loc_col = users_top.columns.get_loc('Next_2 Course')
        users_top.insert(loc_col + 1, 'Diff2', diff2)

        # Diff3
        diff3 = users_top[(users_top[f'Cum Bought top{n}']==users_top[f'Top{n} Bought Position']) | (users_top[f'Cum Bought top{n}'] == users_top[f'Top{n} Bought Position'] + 3)]
        diff3 = diff3.groupby('User ID')['Order Date'].diff().dt.days
        loc_col = users_top.columns.get_loc('Next_3 Course')
        users_top.insert(loc_col + 1, 'Diff3', diff3)

        # Limpio el dataset y lo tranformo al formato de salida
        users_top = users_top.replace({'nan': np.nan}).fillna(0)
        users_top[['Diff1', 'Diff2', 'Diff3']]  = users_top[['Diff1', 'Diff2', 'Diff3']] .astype(int)
        users_top = users_top.groupby('User ID')[['Top Course', 'Next_1 Course', 'Diff1', 'Next_2 Course', 'Diff2', 'Next_3 Course', 'Diff3']].agg(lambda x: x.unique().tolist()[-1])
        
        # Añado los dataframes al diccionario
        dict_groups[f'top{n}'] = users_top
        
    fecha_top1 = dict_groups['top1']
    fecha_top2 = dict_groups['top2']
    fecha_top3 = dict_groups['top3']
        
    # return top1, top2, top3

    # Plotear los gráficos
    lista_fechas = [fecha_top1, fecha_top2, fecha_top3]
    for num, top in enumerate(lista_fechas, start=1):
        data_fecha = top[top['Next_1 Course']!=0]

        fig, axs = plt.subplots(3, 2, figsize=(12, 9), gridspec_kw={'width_ratios': [3, 3]})

        title = data_fecha['Top Course'].unique()[0]
        plt.suptitle(f'Curso TOP{num}: {title}'.title(), fontsize=24, fontweight='bold', y=1.05)

        # Gráfico 0.0
        axs[0, 0].hist(data_fecha['Diff1'], bins=250, color=c_med)
        axs[0, 0].set_yscale('log')
        axs[0, 0].set_xticks(range(0, data_fecha['Diff1'].max(), 180))
        axs[0, 0].set_xlabel('Días', labelpad=15)
        axs[0, 0].set_ylabel('Frecuencia (log)', labelpad=15)
        axs[0, 0].grid(alpha=0.25)
        axs[0, 0].set_title('Histograma con escala logarítmica (Next_1)', fontsize=12, fontweight='bold', y=1.05);
        # Gráfico 0.1
        data_fecha['Diff1'].plot(ax=axs[0, 1], kind='box', ylabel='', vert=False, color=c_med, medianprops={'color':'red'})
        axs[0, 1].set_xticks(range(0, data_fecha['Diff1'].max(), 180))
        axs[0, 1].set_xlabel('Días', labelpad=15)
        axs[0, 1].set_yticklabels([])
        axs[0, 1].grid(axis='x', alpha=0.25)
        axs[0, 1].set_title('Boxplot (Next_1)', fontsize=12, fontweight='bold', y=1.05)
        media = np.mean(data_fecha['Diff1'])
        mediana = np.median(data_fecha['Diff1'])
        moda = data_fecha['Diff1'].mode()[0]
        axs[0, 1].axvline(x=media, color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.33)
        axs[0, 1].axvline(x=moda, color='blue', linestyle=':', label=f'Moda: {moda:.2f}', alpha=0.33)
        lineas = [
            plt.Line2D([0], [0], color='red', linestyle='-', label=f'Mediana: {mediana:.2f}'),
            plt.Line2D([0], [0], color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.5),
            plt.Line2D([0], [0], color='blue', linestyle=':', label=f'Moda: {moda:.2f}', alpha=0.5)
        ]
        axs[0, 1].legend(handles=lineas);

        # Gráfico 1.0
        axs[1, 0].hist(data_fecha['Diff2'], bins=250, color=c_med)
        axs[1, 0].set_yscale('log')
        axs[1, 0].set_xticks(range(0, data_fecha['Diff2'].max(), 180))
        axs[1, 0].set_xlabel('Días', labelpad=15)
        axs[1, 0].set_ylabel('Frecuencia (log)', labelpad=15)
        axs[1, 0].grid(alpha=0.25)
        axs[1, 0].set_title('Histograma con escala logarítmica (Next_2)', fontsize=12, fontweight='bold', y=1.05);
        # Gráfico 1.1
        data_fecha['Diff2'].plot(ax=axs[1, 1], kind='box', ylabel='', vert=False, color=c_med, medianprops={'color':'red'})
        axs[1, 1].set_xticks(range(0, data_fecha['Diff2'].max(), 180))
        axs[1, 1].set_xlabel('Días', labelpad=15)
        axs[1, 1].set_yticklabels([])
        axs[1, 1].grid(axis='x', alpha=0.25)
        axs[1, 1].set_title('Boxplot (Next_2)', fontsize=12, fontweight='bold', y=1.05)
        media = np.mean(data_fecha['Diff2'])
        mediana = np.median(data_fecha['Diff2'])
        moda = data_fecha['Diff2'].mode()[0]
        axs[1, 1].axvline(x=media, color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.33)
        axs[1, 1].axvline(x=moda, color='blue', linestyle=':', label=f'Moda: {moda:.2f}', alpha=0.33)
        lineas = [
            plt.Line2D([0], [0], color='red', linestyle='-', label=f'Mediana: {mediana:.2f}'),
            plt.Line2D([0], [0], color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.5),
            plt.Line2D([0], [0], color='blue', linestyle=':', label=f'Moda: {moda:.2f}', alpha=0.5)
        ]
        axs[1, 1].legend(handles=lineas);

        # Gráfico 2.0
        axs[2, 0].hist(data_fecha['Diff3'], bins=250, color=c_med)
        axs[2, 0].set_yscale('log')
        axs[2, 0].set_xticks(range(0, data_fecha['Diff3'].max(), 180))
        axs[2, 0].set_xlabel('Días', labelpad=15)
        axs[2, 0].set_ylabel('Frecuencia (log)', labelpad=15)
        axs[2, 0].grid(alpha=0.25)
        axs[2, 0].set_title('Histograma con escala logarítmica (Next_3)', fontsize=12, fontweight='bold', y=1.05);
        # Gráfico 2.1
        data_fecha['Diff3'].plot(ax=axs[2, 1], kind='box', ylabel='', vert=False, color=c_med, medianprops={'color':'red'})
        axs[2, 1].set_xticks(range(0, data_fecha['Diff3'].max(), 180))
        axs[2, 1].set_xlabel('Días', labelpad=15)
        axs[2, 1].set_yticklabels([])
        axs[2, 1].grid(axis='x', alpha=0.25)
        axs[2, 1].set_title('Boxplot (Next_3)', fontsize=12, fontweight='bold', y=1.05)
        media = np.mean(data_fecha['Diff3'])
        mediana = np.median(data_fecha['Diff3'])
        moda = data_fecha['Diff3'].mode()[0]
        axs[2, 1].axvline(x=media, color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.33)
        axs[2, 1].axvline(x=moda, color='blue', linestyle=':', label=f'Moda: {moda:.2f}', alpha=0.33)
        lineas = [
            plt.Line2D([0], [0], color='red', linestyle='-', label=f'Mediana: {mediana:.2f}'),
            plt.Line2D([0], [0], color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.5),
            plt.Line2D([0], [0], color='blue', linestyle=':', label=f'Moda: {moda:.2f}', alpha=0.5)
        ]
        axs[2, 1].legend(handles=lineas);

        plt.tight_layout(h_pad=3);