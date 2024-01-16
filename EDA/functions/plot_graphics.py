import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

c_med = '#008B8B'

nombre_meses = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']



def diff_ventas_facturacion(data_raw):
    # Crear los gráficos
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))

    # GRAFICO_1
    users = data_raw.groupby('User ID').size().to_frame()

    conditions = [
        (users == 1),
        (users == 2),
        (users == 3),
        ((users >= 4) & (users < 10)),
        ((users >= 10) & (users < 20)),
        (users >= 20)
    ]
    options = ['1 Curso', '2 Cursos', '3 Cursos', 'Entre 4 y 9 Cursos', 'Entre 10 y 19 Cursos', 'Más de 20']

    users['Cluster_cantidad'] = np.select(conditions, options, default='No ha comprado')
    users = users['Cluster_cantidad'].value_counts(ascending=True)
    users = users.reindex(options)[::-1]
    users.plot(kind='barh', title='Cantidad de cursos que suelen comprar los Alumnos\n', xlabel='Cantidad de Alumnos', ylabel='Cantidad de cursos', color=c_med, ax=axs[0, 0])
    for i, v in enumerate(users.values):
        axs[0, 0].text(v + 0.1, i, str(v), color='black', va='center', ha='left', alpha=0.5)
    axs[0, 0].grid(axis='x', alpha=0.25)
    axs[0, 0].title.set_fontweight('bold')


    # GRAFICO_2
    users = data_raw.groupby('User ID').size()
    top_5 = users.sort_values(ascending=False).head()[::-1]
    top_5.plot(kind='barh', title='Los cinco alumnos que más cursos tienen\n(Incluye cursos gratuitos)\n', xlabel='Cantidad de cursos', ylabel='User ID alumnos', color=c_med, ax=axs[0, 1])
    for i, v in enumerate(top_5.values):
        axs[0, 1].text(v + 0.1, i, str(v), color='black', va='center', ha='left', alpha=0.5)
    axs[0, 1].grid(axis='x', alpha=0.25)
    axs[0, 1].title.set_fontweight('bold')


    # GRAFICO_3
    compras = data_raw[data_raw['Current Value'] != 0]
    compras = compras.groupby('User ID').size()
    top_compras = compras.sort_values(ascending=False).head()[::-1]
    top_compras.plot(kind='barh', title='Los cinco alumnos que más cursos han comprado\n(Sólo cursos de pago)\n', xlabel='Cantidad de cursos', ylabel='User ID alumnos', color=c_med, ax=axs[1, 0])
    for i, v in enumerate(top_compras.values):
        axs[1, 0].text(v + 0.1, i, str(v), color='black', va='center', ha='left', alpha=0.5)
    axs[1, 0].grid(axis='x', alpha=0.25)
    axs[1, 0].title.set_fontweight('bold')


    # GRAFICO_4
    facturacion = data_raw.groupby('User ID')['Current Value'].sum()
    top_facturacion = facturacion.sort_values(ascending=False).head()[::-1]
    top_facturacion.plot(kind='barh', title='Los cinco alumnos que más facturación han generado\n', xlabel='Cantidad de cursos', ylabel='User ID alumnos', color=c_med, ax=axs[1, 1])
    for i, v in enumerate(top_facturacion.values):
        axs[1, 1].text(v + 0.1, i, str(v), color='black', va='center', ha='left', alpha=0.5)
    axs[1, 1].grid(axis='x', alpha=0.25)
    axs[1, 1].title.set_fontweight('bold')


    # Ajustar el espacio entre los subplots
    plt.tight_layout(pad=5)



def demanda(data_raw):
    # Crear la estructura de los gráficos
    fig, axs = plt.subplots(2, 2, figsize=(20, 9))

    # GRÁFICO_1
    data_filt = data_raw[data_raw['Course']!='Pack']
    top10_ventas = data_filt.groupby('Course').size().sort_values(ascending=False).head(10)[::-1]
    top10_ventas.plot(kind='barh', title='Los 10 cursos más vendidos\n(Sin contar con los Packs)\n', ylabel='Nombre del curso', xlabel='Número de ventas totales', color=c_med, ax=axs[0, 0])
    axs[0, 0].grid(axis='x', alpha=0.25)
    axs[0, 0].title.set_fontweight('bold')


    # Cursos ordenados por facturación (SIN PACKS)
    facturacion_cursos = data_filt.groupby('Course')['Current Value'].sum()
    facturacion_cursos = facturacion_cursos.sort_values(ascending=False)

    # GRÁFICO_2
    top10_facturacion_cursos = facturacion_cursos.head(10)[::-1]
    top10_facturacion_cursos.plot(kind='barh', title='Los 10 cursos que más han facturado\n(Sin contar con los Packs)\n', xlabel='Facturación (en Euros)', ylabel='Nombre del curso', color=c_med, ax=axs[0, 1])
    axs[0, 1].grid(axis='x', alpha=0.25)
    axs[0, 1].title.set_fontweight('bold')

    # Más vendidos del top10 cursos que más han facturado
    lista_top10_facturacion_cursos = top10_facturacion_cursos.index
    data_top10_facturacion_cursos = data_raw[data_raw['Course'].isin(lista_top10_facturacion_cursos)]
    top10_facturacion_mas_vendidos = data_top10_facturacion_cursos.groupby('Course').size()

    # GRÁFICO_3
    top5_facturacion_mas_vendidos = top10_facturacion_mas_vendidos.sort_values(ascending=False).head()[::-1]
    top5_facturacion_mas_vendidos.plot(kind='barh', title='Los 5 cursos más vendidos\n(Sólo cursos de pago)\n', xlabel='Número de ventas totales', ylabel='Nombre del curso', color=c_med, ax=axs[1, 0])
    for i, v in enumerate(top5_facturacion_mas_vendidos.values):
        axs[1, 0].text(v + 0.1, i, str(v), color='black', va='center', ha='left', alpha=0.5)
    axs[1, 0].grid(axis='x', alpha=0.25)
    axs[1, 0].title.set_fontweight('bold')


    # GRÁFICO_4
    mas_vendidos = data_raw.groupby('Course').size()
    top5_mas_vendidos = mas_vendidos.sort_values(ascending=False).head()
    otros = mas_vendidos.sort_values(ascending=False)[6:].sum()
    ser_otros = pd.Series({'Otros':otros})
    ser_cursos = pd.concat((ser_otros, top5_mas_vendidos), axis=0).sort_values(ascending=True)
    ser_cursos.plot(kind='barh', title='Los 5 cursos más "vendidos"\n(incluye gratuitos)\n', xlabel='Número de ventas totales', ylabel='Nombre del curso', color=c_med, ax=axs[1, 1])
    for i, v in enumerate(ser_cursos.values):
        axs[1, 1].text(v + 0.1, i, str(v), color='black', va='center', ha='left', alpha=0.5)
    axs[1, 1].grid(axis='x', alpha=0.25)
    axs[1, 1].title.set_fontweight('bold')


    # Ajustar el espacio entre los subplots
    plt.tight_layout(pad=5);



def plot_packs(data_raw):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # GRÁFICO_1
    facturacion = data_raw.groupby('Course')['Current Value'].sum()
    packs = facturacion[facturacion.index=='Pack']
    no_packs = facturacion[facturacion.index!='Pack']

    dataf = pd.DataFrame({
        'Packs':[packs.values[0]],
        'No Packs':[no_packs.values.sum()]
    })

    dataf_T = dataf.T
    dataf_T.plot(kind='barh', title='Facturación entre Packs vs. No_Packs\n', xlabel='Cantidad (en Euros)', ylabel='', legend=False, color=c_med, ax=axs[0])
    axs[0].grid(axis='x', alpha=0.25)
    axs[0].title.set_fontweight('bold');


    # GRÁFICO_2
    packs = data_raw[data_raw['Course']=='Pack']
    packs = packs.groupby('Product')['Current Value'].sum()
    packs = packs.sort_values(ascending=True)
    packs.plot(kind='barh', title='Packs que más han facturado\n', xlabel='Cantidad (en Euros)', ylabel='', legend=False, color=c_med, ax=axs[1])
    axs[1].grid(axis='x', alpha=0.25)
    axs[1].title.set_fontweight('bold')
    for i, v in enumerate(packs.values):
        axs[1].text(v + 0.1, i, str(v), color='black', va='center', ha='left', alpha=0.5);


    # Ajustar el espacio entre los subplots
    plt.tight_layout(pad=5);




def facturacion(data_raw):
    anios = data_raw['Order Date'].dt.year.unique()

    num_filas = int(np.ceil(len(anios) / 2) + 1)

    fig, axs = plt.subplots(num_filas, 2, figsize=(12, 25))

    # GRÁFICO_1
    max_year = data_raw.groupby(data_raw['Order Date'].dt.year)['Current Value'].sum()
    max_year.plot(kind='bar', xlabel='', ylabel='Facturación (En Euros)', color=c_med, ax=axs[0, 0])
    axs[0, 0].set_title('Facturación Anual\n', fontsize=15, fontweight='bold')
    axs[0, 0].ticklabel_format(style='plain', axis='y')
    axs[0, 0].tick_params(axis='x', rotation=45)
    axs[0, 0].set_xticklabels(axs[0, 0].get_xticklabels(), ha='right')
    axs[0, 0].grid(axis='y', alpha=0.25)
    axs[0, 0].title.set_fontweight('bold')


    # GRÁFICO_2
    fecha = data_raw.groupby(data_raw['Order Date'].dt.month_name())['Current Value'].sum()
    fecha = fecha.reindex(nombre_meses)
    fecha.plot(kind='bar', xlabel='', ylabel='Facturación (en Euros)', color=c_med, ax=axs[0, 1])
    axs[0, 1].set_title('Facturación global por mes\n', fontsize=15, fontweight='bold')
    axs[0, 1].tick_params(axis='x', rotation=45)
    axs[0, 1].set_xticklabels(axs[0, 1].get_xticklabels(), ha='right')
    axs[0, 1].grid(axis='y', alpha=0.25)
    axs[0, 1].title.set_fontweight('bold')

    # GRÁFICOS POR AÑO
    for num, anio in enumerate(anios, start=2):
        if num % 2 == 0:
            fila = int(np.floor(num / 2))
            columna = 0
        else:
            fila = int(np.floor(num / 2))
            columna = 1

        data_filt = data_raw[data_raw['Order Date'].dt.year == anio]
        fecha = data_filt.groupby(data_filt['Order Date'].dt.month_name())['Current Value'].sum()
        fecha = fecha.reindex(nombre_meses)
        fecha.plot(kind='bar', xlabel='', ylabel='Facturación (en Euros)', color=c_med, ax=axs[fila, columna])
        axs[fila, columna].set_title(f'Facturación por mes (Año {anio})\n', fontsize=15, fontweight='bold')
        axs[fila, columna].tick_params(axis='x', rotation=45)
        axs[fila, columna].set_xticklabels(axs[fila, columna].get_xticklabels(), ha='right')
        axs[fila, columna].grid(axis='y', alpha=0.25)
        axs[fila, columna].title.set_fontweight('bold')

    plt.tight_layout(pad=5);



def top3_ventas_facturacion(data_raw):
    # Crear estructura de los gráficos
    fig, axs = plt.subplots(2, 2, figsize=(21, 14))

    # GRÁFICO_1
    data_filt = data_raw[data_raw['Course']!='Pack']
    top3_ventas = data_filt.groupby('Course').size().sort_values(ascending=False).head(3).index
    data_top3_ventas = data_raw[data_raw['Course'].isin(top3_ventas)]
    grupo = data_top3_ventas.groupby([data_top3_ventas['Order Date'].dt.month_name(), 'Course']).size()
    grupo = grupo.unstack().reindex(nombre_meses)
    grupo.plot(kind='bar', title='Ventas por mes de los tres cursos más vendidos\n', xlabel='Meses del año', ylabel='Número de ventas totales', colormap='viridis', ax=axs[0, 0])
    axs[0, 0].ticklabel_format(style='plain', axis='y')
    axs[0, 0].tick_params(axis='x', rotation=45)
    axs[0, 0].set_xticklabels(axs[0, 0].get_xticklabels(), ha='right')
    axs[0, 0].grid(axis='y', alpha=0.25)
    axs[0, 0].title.set_fontweight('bold')
    axs[0, 0].legend(loc='center left', bbox_to_anchor=(1, 0.75))


    # GRÁFICO_2
    # Lista top3 facturación
    data_filt = data_raw[data_raw['Course']!='Pack']
    facturacion_cursos = data_filt.groupby('Course')['Current Value'].sum()
    top3_facturacion_cursos = facturacion_cursos.sort_values(ascending=False).head(3).index
    data_top3_fact = data_raw[data_raw['Course'].isin(top3_facturacion_cursos)]
    # Mostrar top3 cursos que más han facturado por mes
    grupo = data_top3_fact.groupby([data_top3_fact['Order Date'].dt.month_name(), 'Course'])['Current Value'].sum()
    grupo = grupo.unstack().reindex(nombre_meses)
    grupo.plot(kind='bar', title=f'Facturación por mes de los 3 cursos que más facturan\n', ylabel='Facturación total', xlabel='Meses del año', colormap='viridis', ax=axs[0, 1])
    axs[0, 1].tick_params(axis='x', rotation=45)
    axs[0, 1].set_xticklabels(axs[0, 1].get_xticklabels(), ha='right')
    axs[0, 1].grid(axis='y', alpha=0.25)
    axs[0, 1].title.set_fontweight('bold')
    axs[0, 1].legend(loc='center left', bbox_to_anchor=(1, 0.75))


    # GRÁFICO_3
    # Lista top3 ventas (incluyendo gratuitos)
    data_filt = data_raw[data_raw['Course']!='Pack']
    top3_ventas_includeAll = data_filt.groupby('Course').size().sort_values(ascending=False).head(3).index
    data_top3_ventas_includeAll = data_raw[data_raw['Course'].isin(top3_ventas_includeAll)]
    # Mostrar facturación del top3 ventas por mes (incluyendo gratuitos)
    grupo = data_top3_ventas_includeAll.groupby([data_raw['Order Date'].dt.month_name(), 'Course'])['Current Value'].sum()
    grupo = grupo.unstack().reindex(nombre_meses)
    grupo.plot(kind='bar', title=f'Facturación por mes de los 3 cursos más vendidos\n(Incluye cursos gratuitos)\n', ylabel='Facturación total', xlabel='Meses del año', colormap='viridis', ax=axs[1, 0])
    axs[1, 0].tick_params(axis='x', rotation=45)
    axs[1, 0].set_xticklabels(axs[1, 0].get_xticklabels(), ha='right')
    axs[1, 0].grid(axis='y', alpha=0.25)
    axs[1, 0].title.set_fontweight('bold')
    axs[1, 0].legend(loc='center left', bbox_to_anchor=(1, 0.75))


    # GRÁFICO_4
    # Lista top3 ventas (Sólo cursos de pago)
    data_filt = data_raw[data_raw['Course']!='Pack']
    data_filt = data_filt[data_filt['Current Value']>0]
    top3_ventas_fact= data_filt.groupby('Course').size().sort_values(ascending=False).head(3).index
    facturacion_top3_ventas_fact = data_raw[data_raw['Course'].isin(top3_ventas_fact)]
    # Mostrar facturación del top3 ventas por mes (sólo cursos de pago)
    grupo = facturacion_top3_ventas_fact.groupby([data_raw['Order Date'].dt.month_name(), 'Course'])['Current Value'].sum()
    grupo = grupo.unstack().reindex(nombre_meses)
    grupo.plot(kind='bar', title=f'Facturación por mes de los 3 cursos más vendidos \n(Sólo cursos de pago)\n', ylabel='Facturación total', xlabel='Meses del año', colormap='viridis', ax=axs[1, 1])
    axs[1, 1].tick_params(axis='x', rotation=45)
    axs[1, 1].set_xticklabels(axs[1, 1].get_xticklabels(), ha='right')
    axs[1, 1].grid(axis='y', alpha=0.25)
    axs[1, 1].title.set_fontweight('bold')
    axs[1, 1].legend(loc='center left', bbox_to_anchor=(1, 0.75))


    plt.tight_layout();