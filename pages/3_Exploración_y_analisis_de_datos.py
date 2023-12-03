import streamlit as st
import pandas as pd
import numpy as np

st.title('Exploración y Análisis de Datos')

body = '''
A partir de los datos previamente procesados, esta sección se enfoca en analizar visualmente las relaciones entre las diversas variables que componen nuestros datos. En este punto, es crucial recordar el objetivo principal del proyecto: identificar patrones que indiquen oportunidades para optimizar los procesos de recolección de alimentos por parte de la red BAMX.

Con este objetivo en mente y con la intención de organizar nuestras visualizaciones de manera estructurada, nos planteamos las siguientes preguntas. Buscaremos responder a estas interrogantes a través de la inspección visual de los datos:

- ¿En qué épocas del año es más probable que se generen excedentes?
- ¿En qué localidades existe una mayor probabilidad de acumulación de excedentes?
- ¿Qué cultivos tienden a ser producidos en exceso con mayor frecuencia?
'''

st.markdown(body)

st.divider()


# '''
# El objetivo es identificar patrones que representen ventanas de oportunidad para la eficientización de los procesos de recolecta de alimentos por parte de la red del banco de alimentos. Ejemplos de estos patrones podrían ser aquellos que den respuesta a algunas de las siguientes preguntas: 

# ¿En qué épocas del año es más probable que se generen excedentes? 
# ¿En qué localidades hay mayor probabilidad de acumulación de excedentes?
# ¿Qué cultivos tienen mayor tendencia a ser producidos excesivamente?

# La respuesta a cada una de estas preguntas ofrecería pautas para una implementación de esfuerzos de manera más dirigida por parte de la red del banco de alimentos. Saber Qué, Cuándo y Dónde es más probable encontrar excedentes alimenticios, supone una mejora sustancial en su recolecta.

# A su vez, cada una de estas preguntas puede descomponerse en sub-preguntas que pueden ser abordadas desde el análisis y visualización de nuestros datos. A continuación se desglosan los sub-cuestionamientos que derivan de cada pregunta.

# 1. ¿En qué épocas del año es más probable que se generen excedentes? 

# - ¿Cómo es la producción en cada mes?
# - ¿Esto ha sido igual en todos los años?
# - Ponderando a través de los años, ¿es posible identificar un mes o 
#  conjunto de meses con mayor producción?, ¿qué mes o meses serían? 

# - ¿Cómo fluctúan los precios de los cultivos a través de los meses?
# - ¿Esto ha sido igual en todos los años?
# - Ponderando a través de los años, ¿es posible identificar un mes o 
#  conjunto de meses en el que los precios son menores?, ¿qué  
#  mes o meses serían?

# 2. ¿En qué localidades hay mayor probabilidad de acumulación de excedentes?

# - ¿Cómo es la producción en cada estado?
# - ¿Cómo es la producción en cada municipio?
# - ¿Esto ha sido igual en todos los años?
# - Ponderando a través de los años, ¿es posible identificar un estado o conjunto de estados con mayor producción?, ¿y qué tal un municipio o conjunto de municipios?

# - ¿Cuál es la distribución de los precios promedio en los distintos 
#   estados?
# - ¿Cuál es la distribución de los precios promedio en los distintos 
#   municipios?
# - ¿Esto ha sido igual en todos los años?
# - Ponderando a través de los años, ¿es posible identificar un estado o         
#   conjunto de estados con en el que los precios sean menores?, ¿y qué 
#   tal un municipio o conjunto de municipios? 

# 3. ¿Qué cultivos tienen mayor tendencia a ser producidos excesivamente?

# - ¿Cómo es la producción de cada cultivo? 
# - ¿Esto ha sido igual a lo largo de los años? 
# - Ponderando a través de los años, ¿es posible identificar un cultivo o 
#   conjunto de cultivos con mayor producción?

# - ¿Cuál es la distribución de los precios de los distintos productos?
# - ¿Esto ha sido igual a lo largo de los años? 
# - Ponderando a través de los años, ¿es posible identificar un cultivo o 
#   conjunto de cultivos cuyo precio sea menor?


# 4. Preguntas interseccionales 

# En esta sección se plantean sub-preguntas que impliquen a más de una de las preguntas principales. Por ejemplo, habiendo ubicado un mes en el que la producción siempre es mayor, podemos preguntarnos por los estados/municipios que presenten mayor producción en dicho mes. Podemos incluso ahondar más preguntándonos por los cultivos específicos que llevan la delantera en cuanto a producción, en este mes y en estas localidades. 
# '''



