import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from functions.topN import top_courses
c_med = '#007780'


def secuential_revenue(N=3, date_DMA=None, save_image=False):
    dict_topN = top_courses(N=N, date_DMA=date_DMA)
        
    # Bucle for en el que voy a correr todos los dataframes Top-N
    for n, (key, dataf_raw) in enumerate(dict_topN.items()):
        dataf = dataf_raw.copy()
        
        # Me quedo con el nombre del curso top (lo utilizaré para el título)
        title = dataf['Top Course'].unique()[0]
        
        # Me quedo con los tres cursos más demandados en cada posición de la secuencia de compra del alumno.
        # Next_1, Next_2 & Next_3 representan la secuencia de compras del alumno tras comprar el curso TOP:
            # Next_1 -- son los cursos que se compraron tras comprar el curso TOP
            # Next_2 -- son los cursos que se compraron, con un salto de un curso (Nexet_1) tras comprar el curso TOP
            # Next_3 -- son los cursos que se compraron, con un salto de dos cursos (Nexet_1 y Next_2) tras comprar el curso TOP
        Next_1 = dataf[dataf['Next_1 Course']!=title].dropna(subset='Next_1 Course')['Next_1 Course'].value_counts(ascending=False).head(3)
        Next_2 = dataf[dataf['Next_2 Course']!=title].dropna(subset='Next_2 Course')['Next_2 Course'].value_counts(ascending=False).head(3)
        Next_3 = dataf[dataf['Next_3 Course']!=title].dropna(subset='Next_3 Course')['Next_3 Course'].value_counts(ascending=False).head(3)



        # ---- GRÁFICO DE BARRAS ----
        # Instanciar el gráfico
        fig1, axs = plt.subplots(1, 3, figsize=(18, 5))
        plt.suptitle(f'Curso TOP{n+1}: {title}'.title(), fontsize=24, fontweight='bold', y=1.15)
        
        # Plotear los Gráficos
        list_nexts = [Next_1, Next_2, Next_3]
        for num, next in enumerate(list_nexts):
            next.plot(kind='bar', xlabel='', color=c_med, ax=axs[num])
            axs[num].set_xticks(axs[num].get_xticks())
            axs[num].set_xticklabels(axs[num].get_xticklabels(), rotation=45, ha='right')
            axs[num].set_ylabel('Cuenta', labelpad=15)
            axs[num].set_title(f'Top{num+1} Next_{num+1}'.title(), fontweight='bold', y=1.05)
            axs[num].grid(axis='y', alpha=0.25);
            
        if save_image:
            plt.savefig(f'./images/Gráfico_Barras__Top{n+1}.png', bbox_inches='tight')

        
        
        # ---- HISTOGRAMA ----
        # Filtro el datframe para eliminar las filas en la que el curso en la secuencia es el mismo curso que el curso TOP)
        dataf_filtered = dataf[(dataf['Next_1 Course']!=title) | (dataf['Next_2 Course']!=title) | (dataf['Next_3 Course']!=title)]
        
        # Instanciar el gráfico
        fig2, axs = plt.subplots(3, 2, figsize=(12, 9), gridspec_kw={'width_ratios': [3, 3]})
        plt.suptitle(f'Curso TOP{n+1}: {title}'.title(), fontsize=24, fontweight='bold', y=1.05)

        # Ejecuto el bucle que irá colocando cada gráfico es su posición
        for num in range(3):
            for nn in range(2):
                if nn == 0:
                    axs[num, nn].hist(dataf_filtered[f'Diff{num+1}'], bins=250, color=c_med)
                    axs[num, nn].set_yscale('log')
                    if dataf_filtered[f'Diff{num+1}'].max() >= 720:
                        axs[num, nn].set_xticks(range(0, dataf_filtered[f'Diff{num+1}'].max(), 180))
                    else:
                        axs[num, nn].set_xticks(range(0, dataf_filtered[f'Diff{num+1}'].max(), 30))
                    axs[num, nn].set_xlabel('Días', labelpad=15)
                    axs[num, nn].set_ylabel('Frecuencia (log)', labelpad=15)
                    axs[num, nn].grid(alpha=0.25)
                    axs[num, nn].set_title(f'Histograma con escala logarítmica (Next_{num+1})', fontsize=12, fontweight='bold', y=1.05);
                if nn == 1:
                    dataf_filtered[f'Diff{num+1}'].plot(ax=axs[num, nn], kind='box', ylabel='', vert=False, color=c_med, medianprops={'color':'red'})
                    if dataf_filtered[f'Diff{num+1}'].max() >= 720:
                        axs[num, nn].set_xticks(range(0, dataf_filtered[f'Diff{num+1}'].max(), 180))
                    else:
                        axs[num, nn].set_xticks(range(0, dataf_filtered[f'Diff{num+1}'].max(), 30))
                    axs[num, nn].set_xlabel('Días', labelpad=15)
                    axs[num, nn].set_yticklabels([])
                    axs[num, nn].grid(axis='x', alpha=0.25)
                    axs[num, nn].set_title(f'Boxplot (Next_{num+1})', fontsize=12, fontweight='bold', y=1.05)
                    media = np.mean(dataf_filtered[f'Diff{num+1}'])
                    mediana = np.median(dataf_filtered[f'Diff{num+1}'])
                    moda = dataf_filtered[f'Diff{num+1}'].mode()[0]
                    axs[num, nn].axvline(x=media, color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.33)
                    axs[num, nn].axvline(x=moda, color='blue', linestyle=':', label=f'Moda: {moda:.2f}', alpha=0.33)
                    lineas = [
                        plt.Line2D([0], [0], color='red', linestyle='-', label=f'Mediana: {mediana:.2f}'),
                        plt.Line2D([0], [0], color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.5),
                        plt.Line2D([0], [0], color='blue', linestyle=':', label=f'Moda: {moda:.2f}', alpha=0.5)
                    ]
                    axs[num, nn].legend(handles=lineas);
                    
        if save_image:
            plt.savefig(f'./images/Histograma_Boxplot__Top{n+1}.png', bbox_inches='tight')


        plt.tight_layout(h_pad=3);


    