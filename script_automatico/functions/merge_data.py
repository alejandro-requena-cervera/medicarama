import numpy as np
import pandas as pd
import os
from functions.stopwords_list import stopwords


# Diccionario que reemplaza los nombres de la base de datos por aquellos nombres con los que vamos a trabajar
dict_replace = {
    'Actualización En Pandemia Por Coronavirus': 'Actualización En Covid-19',
    'Valoración Geriatrica Integral': 'Valoración Geriátrica Integral',
    'Nutrición Para El Síndrome Intestino Irritable (Sii)': 'Nutrición En El Síndrome De Intestino Irritable',
    'Nutrición Para La Enfermedad Inflamatoria Intestinal (Eii)': 'Nutrición En La Enfermedad Inflamatoria Intestinal',
    'Fibromialgia Y Dolor Crónico': 'Fibromialgia Y Dolor De La Actividad',
    'Fibromialgia Y Dolor Crónico Para Enfermeros/As': 'Fibromialgia Y Dolor De La Actividad Para Enfermeros/As',
    'Fibromialgia Y Dolor Crónico Para Fisioterapeutas': 'Fibromialgia Y Dolor De La Actividad Para Fisioterapeutas',
    'Fibromialgia Y Dolor Crónico Para Médicos': 'Fibromialgia Y Dolor De La Actividad Para Médicos',
    'Fibromialgia Y Dolor Crónico Para Psicólogos/As': 'Fibromialgia Y Dolor De La Actividad Para Psicólogos/As',
    'Fibromialgia Y Dolor Crónico Para Terapeutas Ocupacionales': 'Fibromialgia Y Dolor De La Actividad Para Terapeutas Ocupacionales',
    'Fibromialgia Y Dolor Crónico Para Técnicos-Auxiliares De Farmacia Y Técnicos En Farmacia Y Parafarmacia': 'Fibromialgia Y Dolor De La Actividad Para Técnicos-Auxiliares De Farmacia Y Técnicos En Farmacia Y Parafarmacia',
    'Neonatología Para Enfermeros/As': 'Actualización En Neonatología Para Enfermeros/As',
    'Neonatología Para Fisioterapeutas': 'Actualización En Neonatología Para Fisioterapeutas',
    'Neonatología Para Médicos': 'Actualización En Neonatología Para Médicos',
    'Neonatología Para Tcaes': 'Actualización En Neonatología Para Tcaes',
    'Neonatología Para Tes': 'Actualización En Neonatología Para Tes',
    'Neonatología Para Técnicos Auxiliares De Farmacia': 'Actualización En Neonatología Para Técnicos Auxiliares De Farmacia',
    'Tdah - Trastorno Por Déficit De Atención E Hiperactividad': 'Tdah: Trastorno Por Déficit De Atención E Hiperactividad',
    'Tdah - Trastorno Por Déficit De Atención E Hiperactividad Para Enfermeros/As': 'Tdah: Trastorno Por Déficit De Atención E Hiperactividad Para Enfermeros/As',
    'Tdah - Trastorno Por Déficit De Atención E Hiperactividad Para Médicos': 'Tdah: Trastorno Por Déficit De Atención E Hiperactividad Para Médicos',
    'Tdah - Trastorno Por Déficit De Atención E Hiperactividad Para Psicólogos/As': 'Tdah: Trastorno Por Déficit De Atención E Hiperactividad Para Psicólogos/As',
    'Tdah - Trastorno Por Déficit De Atención E Hiperactividad Para To': 'Tdah: Trastorno Por Déficit De Atención E Hiperactividad Para To',
    'Tecnologías De La Información En Entorno Sanitario': 'Tecnologías De La Información En Entornos Sanitarios',
    'Introducción Al Manejo De La Vía Aérea Difícil': 'Introducción Al Manejo Integral De La Vía Aérea Difícil',
    'Atención Integral Al Paciente Con Diabetes Mellitus': 'Atención Integral Del Paciente Con Diabetes Mellitus',
    'Atención Integral Al Paciente Con Obesidad': 'Atención Integral Del Paciente Con Obesidad',
    'Actuación En Incidentes Con Múltiples Víctimas Y Catástrofes': 'Actualización En Incidentes Con Múltiples Víctimas Y Catástrofes',
    'Abordaje Psicológico Y Nutricional De Los Problemas De Alimentación': 'Abordaje Psicológico Y Nutricional En Los Trastornos De Alimentación'
}


# Diccionario con los nuevos cursos y sus caracteríticas
new_courses = {
    'Introducción Al Powerpoint Para Profesionales Sanitarios': {'CR': 0, 'H': 0},
    'Introducción A Los Sistemas De Gestión De Imagen Médica Digital': {'CR': 0, 'H': 0},
    'Introducción A La Geriatría': {'CR': 4.2, 'H': 30},
    'Curso Completo De Diálisis Peritoneal': {'CR': 7, 'H': 50}
}



def merge_datasets(data1=0, data2=1):
    """
    Función que ejecuta, limpia y mergea los archivos excels.
    
    PARÁMETROS:
    -- data1: Posición del primer archivo. Por defecto es 0.
    -- data2: Posición del segudo archivo. Por defecto es 1.
    """
    # Cargo la data y creo la ruta para poder leer los excels
    my_path = os.getcwd()
    num_levels = 1  # retroceder N niveles en la ruta
    for _ in range(num_levels):
        my_path = os.path.abspath(os.path.join(my_path, os.pardir))
    my_path = my_path + '\\data\\excel'

    name_data1 = os.listdir(my_path)[data1]
    name_data2 = os.listdir(my_path)[data2]

    read_data1 = my_path + '\\' + name_data1
    read_data2 = my_path + '\\' + name_data2

    excel1 = pd.read_excel(read_data1, index_col=0)
    excel2 = pd.read_excel(read_data2)

    if 'Unnamed: 0' in excel1.columns:
        excel1 = excel1.drop('Unnamed: 0', axis=1)
    if 'Unnamed: 0' in excel2.columns:
        excel2 = excel2.drop('Unnamed: 0', axis=1)
    
    # Averiguo cuál de los dos excels tiene la columna 'User ID'
    list_excels = [excel1, excel2]
    for excel in list_excels:
        if excel.columns.isin(['User ID']).any():
            excel_userid = excel
        else:
            excel_courses = excel
            
    
    # Limpieza 'excel_courses'
    excel_courses['CURSO'] = excel_courses['CURSO'].str.title().str.strip()   # Que cada palabra empiece por mayúscula
    
    
    # Actualizo 'excel_courses' con los nuevos cursos
    for key, value in new_courses.items():
        df_prov = pd.DataFrame({
            'CURSO': [key],
            'CR': value['CR'],
            'H': value['H']
        })
        excel_courses = pd.concat((excel_courses, df_prov), axis=0).reset_index(drop=True)
            
            
    # Limpieza 'excel_userid'
    excel_userid = excel_userid.loc[:, ['User ID', 'Order Date', 'Product', 'Current Value']]   # Filtro las columnas que quiero del dataset
    excel_userid = excel_userid.dropna(subset='Product')    # Elimino valores nulos
    excel_userid['Product'] = excel_userid['Product'].str.title().str.strip()   # Que cada palabra empiece por mayúscula
    excel_userid = excel_userid[excel_userid['Current Value']!=0]  # Filtro para eliminar las filas de los cursos que fueron gratuitos
    excel_userid = excel_userid[~excel_userid['Product'].str.contains('Pack')]  # Filtro para eliminar las filas que contienen la palabra 'Pack'
    excel_userid = excel_userid[~excel_userid['Product'].str.contains('|'.join(stopwords), na=True)]    # Filtro eliminando las filas que contienen 'stopwords'
    dict_replace_copy = {key.title():value.title() for key, value in dict_replace.items()}   # Me aseguro de que cada palabra de las keywords y los valores del diccionario  empiecen por mayúscula
    excel_userid['Product'] = excel_userid['Product'].replace(dict_replace_copy) # Reemplazo los nombres de los cursos por los nuevos nombres (diccionario)
    excel_userid = excel_userid.sort_values(by='Order Date', ascending=True)    # Ordeno por 'Order Date' de manera ascendente
    
    
    # Añadir columna 'Course' a 'excel_userid'
    courses_list = excel_courses['CURSO'].values
    products_list = excel_userid.groupby('Product').size().index
    
    dict_course = {}
    for curso in courses_list:
        for prod in products_list:
            if curso in prod:
                dict_course.setdefault(prod, curso)

    loc_col = excel_userid.columns.get_loc('Product')
    data_course = excel_userid['Product'].replace(dict_course)
    excel_userid.insert(loc_col +1, 'Course', data_course)
    
    
    # Hago el merge de ambos excels
    df_merge = excel_userid.merge(right=excel_courses, left_on='Course', right_on='CURSO', how='left')
    df_merge = df_merge.drop('CURSO', axis=1)
    
    
    return df_merge