import streamlit as st
import pandas as pd
import numpy as np

st.title('Preparación de datos')

body = '''
El proceso de preparación de datos se ejecutó de manera individualizada para cada uno de los dos conjuntos de datos con los que trabajamos: SIAP y SNIIM. Aunque los procedimientos son en su mayoría idénticos, cada conjunto de datos demandó tratamientos específicos. Comenzaremos detallando la serie de pasos que delinearon el proceso de preparación de datos para el conjunto SIAP y procederemos a hacer lo mimso para el conjunto SNIIM.

## SIAP

- 1. Aplicación de filtros
- 2. Ajuste de los tipos de datos
- 3. Análisis de valores faltantes
- 4. Obtención de valores mensuales
- 5. Análisis de valores atípicos

#### 1. Aplicación de filtros

Con base en la retroalimentación ofrecida por medio de nuestro intermediario con la Red BAMX, primero se filtran los datos con base en la variable "Año", para trabajar solo con aquellos de los años 2020 en adelante.
Derivado de la misma retroalimentación, se filtra también con base en la variable "Cultivo" para trabajar solo con aquellos de interés para la Red BAMX. Específicamente, la lista de cultivos es la siguiente: Tomate rojo (jitomate), Chile verde, Limón, Pepino, Plátano, Mango, Garbanzo, Brócoli, Cebolla, Sandía, Papaya, Calabacita, Lechuga, Tomate verde, Espárrago, Frambuesa, Nopalitos, Nuez, Fresa, Toronja (pomelo), Zarzamora, Piña, Coliflor, Frijol, Berenjena, Uva, Guayaba, Naranja, Papa, Melón, Manzana, Pera, Durazno.
'''

st.markdown(body)