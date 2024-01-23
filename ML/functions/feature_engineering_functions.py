import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

c_med = '#008B8B'


def feature_importance_plot(baseline):
    dataset = pd.DataFrame({
        'Features': baseline.feature_names_in_,
        'Importance': baseline.feature_importances_
    })
    dataset = dataset.sort_values(by='Importance', ascending=False)

    ax = dataset.plot(kind='bar', color=c_med, figsize=(12, 6))
    feature_names = dataset['Features']
    ax.set_xticklabels(feature_names, rotation=45, ha='right')
    plt.title('Feature Importance\n', fontsize=18, fontweight='bold')
    plt.xlabel('Características')
    plt.ylabel('Importancia de las Características')
    media = np.mean(dataset['Importance'])
    mediana = np.median(dataset['Importance'])
    ax.axhline(y=media, color='red', linestyle='--', label=f'Media: {media:.2f}', alpha=0.33)
    ax.axhline(y=mediana, color='blue', linestyle='--', label=f'Mediana: {mediana:.2f}', alpha=0.33)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[0:-1], labels[0:-1], loc='best');


def filter_outliers(data):
    """
    Aplica un filtro para eliminar outliers en cada columna de un DataFrame utilizando el método del rango intercuartílico (IQR).

    Parámetros:
    - data: DataFrame, el conjunto de datos original.

    Retorna:
    - DataFrame, una copia del conjunto de datos original con outliers reemplazados en cada columna.
    """
    df = data.copy()
    for column in data.columns:
        q1 = np.percentile(data[column], 25)
        q3 = np.percentile(data[column], 75)
        iqr = q3 - q1
        threshold_low = q1 - 1.5 * iqr
        threshold_high = q3 + 1.5 * iqr
    
        col_type = df[column].dtype
        df[column][df[column] < threshold_low] = threshold_low.astype(col_type)
        df[column][df[column] > threshold_high] = threshold_high.astype(col_type)
    
    return df   


def log_exp_transform(data):
    """
    Aplica transformaciones logarítmicas o exponenciales a las columnas del conjunto de datos
    basándose en el skewness y kurtosis para mejorar la distribución de los datos.

    Parameters:
    - data (DataFrame): El conjunto de datos que se va a transformar.

    Returns:
    - DataFrame: El conjunto de datos transformado con las mejores transformaciones aplicadas.
    """
    data_copy = data.copy()
    dataset = pd.DataFrame()

    if 'Target' in data_copy.columns:
        data_copy = data_copy.drop('Target', axis=1)

    # Este bucle aplica la función dependiendo del skewness y luego compara el skewness de la
    # transformación con el skewness anterior a la transformación y quedarme con el mejor. 
    for n, col in enumerate(data_copy.columns):
        fila = n // 3
        
        if n % 3 == 0:
            columna = 0
        if n % 3 == 1:
            columna = 1
        if n % 3 == 2:
            columna = 2

        feature = data_copy[col]
        skewness = stats.skew(feature)
        kurtosis = stats.kurtosis(feature)

        provisional = pd.DataFrame()
        if skewness >= 0:
            provisional[col] = np.log(feature + 1e-10)
            condicion = (stats.skew(provisional[col]) < skewness) & (stats.kurtosis(provisional[col]) < kurtosis)
            dataset[col] = np.where(condicion, provisional[col], feature)
            
        if skewness < 0:
            provisional[col] = np.exp(feature + 1e-10)
            condicion = (stats.skew(provisional[col]) > skewness) & (stats.kurtosis(provisional[col]) < kurtosis)
            dataset[col] = np.where(condicion, provisional[col], feature)

    return dataset


def droppear_columnas(dataset, list_columns_to_drop):
    df = dataset.drop(columns=list_columns_to_drop)
    return df