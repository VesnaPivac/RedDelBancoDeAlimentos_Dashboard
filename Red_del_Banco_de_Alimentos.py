import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.title('Red del Banco de Alimentos')

body = 'Este proyecto es parte del curso "Ingeniería de Características" de la Maestría en Ciencia de Datos de la Universidad de Sonora. Su motivación principal es contribuir a la Red de Bancos de Alimentos de México (red BAMX) mediante el análisis de datos públicos relacionados con la producción y el mercado de alimentos a nivel nacional. El objetivo final es realizar el "Storytelling" que permita a la red BAMX identificar ventanas de oportunidad para optimizar sus procedimientos en la colecta y redistribución de alimentos.'

body2 = '''
El proyecto se divide en tres partes:

1. **Obtención de los datos**

El objetivo de esta fase es la identificación y descarga de los datos necesarios de fuentes públicas y confiables. Esto se lleva a cabo de manera programática, para que cualquier persona pueda replicar la descarga simplificadamente por medio de líneas de código. El resultado final son los datos sin ningún tipo de procesamiento, pero organizados de manera tidy. Esto se refiere a que los datos cumplen con las condiciones de que cada columna sea una variable y cada fila una observación.

2. **Preparación de los datos**

Esta etapa se enfoca en la transformación y acondicionamiento de los datos adquiridos para su posterior análisis. Los datos obtenidos en la etapa anterior pueden presentar inconsistencias, formatos no adecuados, valores faltantes o valores atípicos. Para garantizar la fiabilidad y la utilidad de estos, se realizan las siguientes acciones:
  - Limpieza de datos: Se identifican y corrigen inconsistencias en los valores, eliminando datos duplicados o erróneos.
  - Estandarización de formatos: Se asegura que los datos sigan un formato coherente y que los tipos de datos sean apropiados para su análisis.
  - Manejo de valores faltantes: Se abordan los valores faltantes de manera adecuada, ya sea rellenándolos con estimadores o eliminando registros incompletos, dependiendo del impacto en el análisis.
  - Manejo de valores atípicos: Se aplican técnicas estadísticas para identificar y se decidir cómo tratarlos, ya sea corrigiéndolos, transformándolos o manteniéndolos según su relevancia para la historia que se narra con los datos.

3. **Visualización de los datos**

En esta parte del proyecto se da vida a los datos a través de gráficos y representaciones visuales. La información recopilada se presenta de manera efectiva en un dashboard interactivo que facilita la identificación de patrones, tendencias y áreas de interés. Estas visualizaciones ayudan a contar la historia que se encuentra en los datos, proporcionando una visión clara y accesible para la red BAMX.
Las visualizaciones se diseñan metodológicamente para destacar aspectos relevantes de la producción y el mercado de alimentos a nivel nacional. Este proceso permite identificar oportunidades significativas que podrían beneficiar a la red BAMX en la optimización de sus procedimientos de recolección y redistribución de alimentos.
'''

# image = Image.open('')
st.write(body)
st.markdown("<span style='font-size: 12px;'>Equipo: Vesna Camile Pivac Alcaraz, Jose Carlos Barreras Maldonado y Luis Ernesto Ortiz Villalon</span>", unsafe_allow_html=True)


# st.image()
st.subheader('Descripción del proyecto', divider='rainbow')
st.markdown(body2)

