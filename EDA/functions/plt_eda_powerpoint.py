import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

c_med = '#008B8B'


def pw_packs(data):
    # Crear dataframe sólo con Packs
    packs = data[data['Course']=='Pack']

    fig, axs = plt.subplots(1, 2, figsize=(12, 7))

    # Gráfico Izquierda
    packs.value_counts(subset='Product').plot(kind='bar', color=c_med, ax=axs[0], xlabel='')
    axs[0].set_xticks(axs[0].get_xticks())
    axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45, ha='right')
    axs[0].set_ylabel('Cantidad', labelpad=15)
    axs[0].grid(axis='y', alpha=0.25)
    axs[0].set_title('Total de cursos de la categoría Packs'.title(), fontweight='bold', y=1.05);

    # Gráfico Derecha
    sizes = packs.groupby(['Product', 'Current Value']).transform('size')
    scatter = axs[1].scatter(x=packs['Product'], y=packs['Current Value'], c=c_med, s=sizes/10)
    axs[1].set_xticks(axs[1].get_xticks())
    axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45, ha='right')
    axs[1].set_ylabel('Precio', labelpad=15)
    axs[1].set_title('Cantidad de Packs vendidos dependiendo de su Precio'.title(), fontweight='bold', y=1.05)

    # Personalizar la leyenda para mostrar círculos en lugar de rectángulos
    handles = [
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=2, alpha=0.75, markerfacecolor=c_med, label=f"Mínimo: {sizes.min()}"),
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=5, alpha=0.75, markerfacecolor=c_med, label=f"Media: {int(sizes.mean())}"),
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=10, alpha=0.75, markerfacecolor=c_med, label=f"Máximo: {sizes.max()}"),
    ]
    axs[1].legend(handles=handles, title='Cantidad')

    plt.tight_layout()


def pw_top_ventas(data):
    # Crear dataframe top3 ventas (sin Packs)
    lista_top3 = data['Course'].value_counts().head(3).index
    top3_ventas = data[data['Course'].isin(lista_top3)]

    fig, axs = plt.subplots(1, 2, figsize=(12, 8))

    # Gráfico Izquierda: top10
    data.value_counts('Course').head(10).plot(kind='bar', xlabel='', color=c_med, ax=axs[0])
    axs[0].set_xticks(axs[0].get_xticks())
    axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45, ha='right')
    axs[0].set_ylabel('Cantidad', labelpad=15)
    axs[0].grid(axis='y', alpha=0.25)
    axs[0].set_title('Top10 cursos más vendidos'.title(), fontweight='bold', y=1.05)

    # Gráfico Derecha: top3
    sizes = top3_ventas.groupby(['Course', 'Current Value']).transform('size')
    scatter = axs[1].scatter(x=top3_ventas['Course'], y=top3_ventas['Current Value'], c=c_med, s=sizes/10)
    axs[1].set_xticks(axs[1].get_xticks())
    axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45, ha='center')
    axs[1].set_ylabel('Precio', labelpad=15)
    axs[1].grid(axis='y', alpha=0.25)
    axs[1].set_title('Ventas del Top3 más vendidos \ndependiendo de su precio'.title(), fontweight='bold', y=1.05)

    # Personalizar la leyenda para mostrar círculos en lugar de rectángulos
    handles = [
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=2, alpha=0.75, markerfacecolor=c_med, label=f"Mínimo: {sizes.min()}"),
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=5, alpha=0.75, markerfacecolor=c_med, label=f"Media: {int(sizes.mean())}"),
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=10, alpha=0.75, markerfacecolor=c_med, label=f"Máximo: {sizes.max()}"),
    ]
    axs[1].legend(handles=handles, title='Cantidad ventas')

    plt.tight_layout()



def pw_top_facturacion(data):
    # Crear Series top10 facturación (sin Packs)
    top10_facturacion = data.groupby('Course')['Current Value'].sum()
    top10_facturacion = top10_facturacion.sort_values(ascending=False).head(10)

    # Crear Dataframe top3 facturación (sin Packs)
    lista_top3_facturacion = top10_facturacion.head(3).index
    top3_facturacion = data[data['Course'].isin(lista_top3_facturacion)]

    fig, axs = plt.subplots(1, 2, figsize=(12, 8))

    # Gráfico Izquierda: top10
    top10_facturacion.plot(kind='bar', xlabel='', color=c_med, ax=axs[0])
    axs[0].set_xticks(axs[0].get_xticks())
    axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45, ha='right')
    axs[0].set_ylabel('Facturación', labelpad=15)
    axs[0].grid(axis='y', alpha=0.25)
    axs[0].set_title('Top10 cursos que más han facturado'.title(), fontweight='bold', y=1.05);

    # Gráfico Derecha: top3
    sizes = top3_facturacion.groupby(['Course', 'Current Value']).transform('size')
    scatter = axs[1].scatter(x=top3_facturacion['Course'], y=top3_facturacion['Current Value'], c=c_med, s=sizes/10)
    axs[1].set_xticks(axs[1].get_xticks())
    axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=45, ha='right')
    axs[1].set_ylabel('Precio', labelpad=15)
    axs[1].grid(axis='y', alpha=0.25)
    axs[1].set_title('Ventas del Top10 que más ha facturado \ndependiendo de su precio'.title(), fontweight='bold', y=1.05)

    # Personalizar la leyenda para mostrar círculos en lugar de rectángulos
    handles = [
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=2, alpha=0.75, markerfacecolor=c_med, label=f"Mínimo: {sizes.min()}"),
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=5, alpha=0.75, markerfacecolor=c_med, label=f"Media: {int(sizes.mean())}"),
        plt.Line2D([0], [0], linestyle='', marker='o', markersize=10, alpha=0.75, markerfacecolor=c_med, label=f"Máximo: {sizes.max()}"),
    ]
    axs[1].legend(handles=handles, title='Cantidad ventas')

    plt.tight_layout()


def pw_diff_fechas(data):
    # Voy a ordenar el histórico por usuario y fechas
    data_users = data.sort_values(by=['User ID', 'Order Date'])
    data_users = data_users.reset_index(drop=True)

    # Añado la columna que indica la diferencia de días
    series_diff_fechas = data_users.groupby('User ID')['Order Date'].diff().dt.days
    loc_col = data_users.columns.get_loc('Order Date')
    data_users.insert(loc_col + 1, 'Diff Days', series_diff_fechas)
    data_users['Diff Days'] = data_users['Diff Days'].fillna(0)
    data_users['Diff Days'] = data_users['Diff Days'].astype(int)

    # Elimino las filas con valores == 0
    diff_days = data_users[data_users['Diff Days']!=0]['Diff Days']
    diff_days

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

    mode_diff = diff_days.mode().values[0]
    mediana_diff = np.median(diff_days)
    media_diff = np.mean(diff_days)

    # Defino el gráfico
    fig, axs = plt.subplots(2, 1, figsize=(18, 12))

    # Gráfico Arriba
    diff_days.hist(bins=100, color=c_med, ax=axs[0])
    axs[0].set_yscale('log')
    axs[0].set_xticks(range(0, data_users['Diff Days'].max() + 180, 180))
    axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=0)
    axs[0].set_ylabel('Recuento (log)', labelpad=15)
    axs[0].grid(axis='x', alpha=0.25)
    axs[0].grid(axis='y', alpha=0.25)
    axs[0].set_title('Distribución de la diferencia de días en que un mismo usuario vuelve a realizar una compra'.title(), fontsize=15, fontweight='bold', y=1.05);

    # Agregar líneas verticales para la media y la mediana
    axs[0].axvline(mode_diff, color='gray', linestyle='dashed', linewidth=2, label=f'Moda: {mode_diff:.0f} días')
    axs[0].axvline(mediana_diff, color='blue', linestyle='dashed', linewidth=2, label=f'Mediana: {mediana_diff:.0f} días')
    axs[0].axvline(media_diff, color='red', linestyle='dashed', linewidth=2, label=f'Media: {media_diff:.0f} días')

    # Agregar leyenda
    axs[0].legend()

    # Gráfico Abajo
    diff_plot = df_diff_days.value_counts(subset='Range')
    diff_plot = diff_plot.reindex(options)
    diff_plot.plot(kind='bar', xlabel='', color=c_med, ax=axs[1])
    axs[1].set_xticks(axs[1].get_xticks())
    axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation=0)
    axs[1].set_ylabel('Recuento', labelpad=15)
    axs[1].grid(axis='y', alpha=0.25)
    axs[1].set_title('¿Cuánto tiempo suele tardar un mismo usuario en realizar una nueva compra?'.title(), fontsize=15, fontweight='bold', y=1.05);

    plt.tight_layout(h_pad=5);


def pw_facturacion_anual(data):
    import calendar
    cal_months = list(calendar.month_name)[1:]
    data_sort = data.sort_values(by='Order Date')

    min_year = list(data_sort['Order Date'].dt.year)[0]
    max_year = list(data_sort['Order Date'].dt.year)[-1]
    anios = range(min_year, max_year+1)

    fig, axs = plt.subplots(len(anios), 1, figsize=(12, 25))

    for n, ano in enumerate(anios):
        data_months = data_sort[data_sort['Order Date'].dt.year==int(ano)]
        data_months = data_months.groupby(data_months['Order Date'].dt.month_name())['Current Value'].sum()
        data_months = data_months.reindex(cal_months)
        data_months.plot(kind='bar', ax=axs[n], xlabel='', ylabel='Facturación', color=c_med, legend=None)
        axs[n].set_xticks(axs[n].get_xticks())
        axs[n].set_xticklabels(axs[n].get_xticklabels(), rotation=45)
        axs[n].set_ylim(0, 80_000)
        axs[n].grid(axis='y', alpha=0.25)
        axs[n].set_title(f'Facturación por mes del año {ano}'.title(), fontsize=18, fontweight='bold', y=1.05)
        
        media = np.mean(data_months)
        axs[n].axhline(y=media, color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.33);

        handles, labels = axs[n].get_legend_handles_labels()
        axs[n].legend([handles[0]], [labels[0]], loc='best')

    plt.tight_layout(h_pad=4);



def pw_mejor_peor_facturacion(data):
    import calendar
    cal_months = list(calendar.month_name)[1:]
    anios = data['Order Date'].dt.year.unique()
    
    best_months = {}
    worst_months = {}
    for n, anio in enumerate(anios):
        data_months = data[data['Order Date'].dt.year==int(anio)]
        data_months = data_months.groupby(data_months['Order Date'].dt.month_name())['Current Value'].sum()
        data_months = data_months.sort_values(ascending=False)
        
        for i in data_months.head(3).index:
            best_months[i] = best_months.setdefault(i, 0) + 1
            
        for i in data_months.tail(3).index:
            worst_months[i] = worst_months.setdefault(i, 0) + 1
        
        
    df_best = pd.Series(best_months)
    df_worst = pd.Series(worst_months)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    list_ser = [df_best, df_worst]
    for n, ser in enumerate(list_ser):
        ser = ser.sort_values(ascending=False)
        ser = ser[ser > 1]
        ser = ser.reindex([i for i in cal_months if i in ser.index])
        ser.plot(kind='bar', ax=axs[n], color=c_med)
        axs[n].set_yticks(range(0, ser.max()+1, 1))
        axs[n].set_xticklabels(axs[n].get_xticklabels(), rotation=45)
        axs[n].grid(axis='y', alpha=0.25)
        
        if n == 0:
            axs[n].set_title('Meses de mejor facturación'.title(), fontsize=18, fontweight='bold', y=1.05)
        else:
            axs[n].set_title('Meses de peor facturación'.title(), fontsize=18, fontweight='bold', y=1.05)