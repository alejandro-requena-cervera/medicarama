import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def groupby_userID(data):
  """
  Agrupa y transforma el conjunto de datos por 'User ID', eliminando cursos gratuitos y Packs,
  eliminando filas de usuarios con un solo curso, creando la variable objetivo ('Target'), obteniendo
  variables derivadas de fechas, total de cursos, precios, créditos, horas, y categorías, y organizando
  las columnas de manera estructurada.

  Parameters:
  - data (DataFrame): El conjunto de datos original.

  Returns:
  - DataFrame: El conjunto de datos transformado y agrupado por 'User ID'.
  """
  
  # aquí me estoy cargando los Packs
  # Eliminar filas de cursos gratuitos y Packs
  df_merge = data[data['Current Value']!=0]
  df_merge = df_merge[df_merge['Course']!='Pack']
  # Eliminar filas de alumnos con un sólo curso
  total_cursos = df_merge.groupby(['User ID'])['Course'].size()
  df_merge['N Courses'] = df_merge['User ID'].map(total_cursos)
  df_merge = df_merge[df_merge['N Courses'] > 1]
  # Crear el Target
  target = df_merge.drop_duplicates(subset=['User ID'], keep='last')[['User ID', 'Course']]    # Me quedo con el útlimo valor
  df_merge = df_merge.merge(right=target, on=['User ID', 'Course'], how='left', indicator=True)   # Hago merge con target he indico si aparace en ambos dfs o no
  df_merge = df_merge[df_merge['_merge']=='left_only'].drop('_merge', axis=1)     # Elimino aquellas filas donde la fila se ha encontrado en ambos dfs al mergear
  df_merge['N Courses'] = df_merge['N Courses'] - 1   # Elimino 1 curso del total de curso de cada alumno (ahora ese curso eliminado es el target)
  target = target.rename({'Course': 'Target'}, axis=1).set_index('User ID')    # Antes de hacer merge, cambio el nombre de la columna
  # # Get dummies
  df_merge = pd.get_dummies(df_merge, columns=['Category'], dtype=int)
  columnas_category = [col for col in df_merge.columns if ('Category' in col)]
  # Obtener variables 
  #   Fecha
  max_fecha = df_merge.groupby('User ID')['Order Date'].max()
  ano = pd.to_datetime(max_fecha).dt.year.rename('Year last purchased')
  month = pd.to_datetime(max_fecha).dt.month.rename('Month last purchased')
  day = pd.to_datetime(max_fecha).dt.day.rename('Day last purchased')
  dayOFweek = pd.to_datetime(max_fecha).dt.day_of_week.rename('DayOfWeek last purchased')
  n_dias_ultima_compra = (pd.Timestamp.today() - pd.to_datetime(max_fecha)).dt.days.rename('N days to date')
  #   Total Cursos
  n_courses = df_merge.groupby(['User ID'])['N Courses'].max()
  #   Precio
  sum_precio = df_merge.groupby(['User ID'])['Current Value'].sum().rename('Current Value Sum')
  max_precio = df_merge.groupby(['User ID'])['Current Value'].max().rename('Current Value Max')
  min_precio = df_merge.groupby(['User ID'])['Current Value'].min().rename('Current Value Min')
  mean_precio = df_merge.groupby(['User ID'])['Current Value'].mean().rename('Current Value Mean')
  #   Créditos
  sum_cr = df_merge.groupby(['User ID'])['CR'].sum().rename('Credits Sum')
  max_cr = df_merge.groupby(['User ID'])['CR'].max().rename('Credits Max')
  min_cr = df_merge.groupby(['User ID'])['CR'].min().rename('Credits Min')
  mean_cr = df_merge.groupby(['User ID'])['CR'].mean().rename('Credits Mean')
  #   Horas
  sum_h = df_merge.groupby(['User ID'])['H'].sum().rename('Hours Sum')
  max_h = df_merge.groupby(['User ID'])['H'].max().rename('Hours Max')
  min_h = df_merge.groupby(['User ID'])['H'].min().rename('Hours Min')
  mean_h = df_merge.groupby(['User ID'])['H'].mean().rename('Hours Mean')
  #   Email
  # email = df_merge.groupby(['User ID'])['Email'].first()
  # Merges
  df_merge = df_merge.groupby('User ID')[columnas_category].sum().reset_index()
  lista_series = [ano, month, day, dayOFweek, n_dias_ultima_compra, n_courses,  # email
                  sum_precio, max_precio, min_precio, mean_precio,
                  sum_cr, max_cr, min_cr, mean_cr, 
                  sum_h, max_h, min_h, mean_h,
                  target]   
  for serie in lista_series:
      df_merge = df_merge.merge(right=serie, left_on='User ID', right_index=True, how='left')

  # Reorganizar columnas
  col_top = ['User ID', "Year last purchased", 'Month last purchased', 'Day last purchased', 'DayOfWeek last purchased', 'N days to date', 'N Courses']
  col_others = df_merge.columns.difference(col_top + columnas_category)
  df_merge = df_merge[col_top + columnas_category + list(col_others)]

  print('Número de filas que habían (si agrupo por User ID):', data.groupby('User ID').size().shape)
  print('Número de filas que hay (tras las transformaciones):', df_merge.shape)

  return df_merge


if __name__ == '__main__':
    pass