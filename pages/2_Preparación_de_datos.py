import streamlit as st
import pandas as pd
import numpy as np

st.title('Preparación de datos')

body = '''
El proceso de preparación de datos se ejecutó de manera individualizada para cada uno de los dos conjuntos de datos con los que trabajamos: SIAP y SNIIM. Aunque los procedimientos son en su mayoría idénticos, cada conjunto de datos demandó tratamientos específicos. Comenzaremos detallando la serie de pasos que delinearon el proceso de preparación de datos para el conjunto SIAP y procederemos a hacer lo mimso para el conjunto SNIIM.

## SIAP

Los pasos que conformaron el proceso de preparación de los datos del SIAP fueron:

- 1. Aplicación de filtros
- 2. Ajuste de los tipos de datos
- 3. Análisis de valores faltantes
- 4. Obtención de valores mensuales
- 5. Análisis de valores atípicos

#### 1. Aplicación de filtros

Con base en la retroalimentación proporcionada por nuestro canal de comunicación con la Red BAMX, se implementó un proceso de filtrado con el objetivo de refinar y focalizar nuestro conjunto de datos.

- **Filtrado por año**
Los datos son inicialmente filtrados según la variable "Año", limitándonos exclusivamente a aquellos correspondientes a los años 2020 en adelante. Este criterio temporal asegura que nuestra análisis se centre en la información más reciente y relevante.

- **Filtrado por cultivo**
En consonancia con las recomendaciones proporcionadas, también aplicamos un filtro basado en la variable "Cultivo". Nos enfocamos únicamente en los cultivos de interés para la Red BAMX. Esta selección específica incluye los siguientes cultivos: Tomate rojo (jitomate), Chile verde, Limón, Pepino, Plátano, Mango, Garbanzo, Brócoli, Cebolla, Sandía, Papaya, Calabacita, Lechuga, Tomate verde, Espárrago, Frambuesa, Nopalitos, Nuez, Fresa, Toronja (pomelo), Zarzamora, Piña, Coliflor, Frijol, Berenjena, Uva, Guayaba, Naranja, Papa, Melón, Manzana, Pera, Durazno.
'''

st.markdown(body)