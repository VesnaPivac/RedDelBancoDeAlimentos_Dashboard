import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO

st.title('Exploración y Análisis de Datos')

body = '''
Basándonos en los datos previamente procesados, esta sección se centra en el análisis visual de las relaciones entre las diversas variables que componen nuestros datos. En este punto, es fundamental recordar el objetivo principal del proyecto: identificar patrones que sugieran oportunidades para optimizar los procesos de recolección de alimentos por parte de la red BAMX.

Con este objetivo en mente y con la intención de estructurar nuestras visualizaciones de manera organizada, desglosamos nuestro análisis en tres categorías principales: análisis temporal, geográfico y de cultivo. Además, se aborda una cuarta categoría económica, con el propósito de examinar las tres categorías anteriores desde un enfoque diferente. Para cada análisis, nos proponemos abordar las siguientes preguntas mediante la inspección visual de los datos:

**Análisis Temporal**

¿En qué épocas del año es más probable que se generen excedentes?

**Análisis Geográfico**

¿En qué localidades existe una mayor probabilidad de acumulación de excedentes?

**Análisis de Cultivo**

¿Qué cultivos muestran una tendencia a ser producidos en exceso con mayor frecuencia?

**Análisis Económico**

¿Para qué época/cultivo/localidad el comportamiento económico sugiere la posibilidad de que se generen excedentes?

Para llevar a cabo cada uno de los análisis, empleamos widgets que posibilitaron un examen interactivo del comportamiento de las diversas variables en nuestros datos. Estos widgets nos permitieron explorar de manera dinámica los valores temporales, geográficos y de cultivo. A raíz de este análisis exhaustivo de todas las variables, decidimos focalizar nuestro enfoque exclusivamente en nuestro territorio estatal, Sonora, considerando sus municipios y los cultivos que son activamente producidos aquí. A continuación de describe cada una de las gráficas empleadas. Se utiliza como ejemplo a la Uva, cultivo para el cúal Sonora se posiciona como el principal estado productor.  
'''

st.markdown(body)

st.divider()

body = '''
## Análisis Temporal

#### Gráfica de valores mensuales de las distintas variables y cultivos
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot1.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''
#### Gráfica de valores acumulados de las distintas variables y cultivos
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot2.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''
#### Gráfica de mejores meses en términos de las distintas variables y cultivos
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot3.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''
#### Gráfica de evolución de las distintas variables y cultivos a lo largo del tiempo
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot4.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''
#### Gráfica de correlación entre variables a lo largo del tiempo para los distintos cultivos
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot5.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)


st.divider()

body = '''
## Análisis Geográfico

#### Correlación entre variables SIAP y SNIIM en los distintos estados del país
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot6.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''
#### Gráfica de mejores estados en términos de las distintas variables y cultivos
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot7.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''
#### Treemap de municipios en términos de las distintas variables y cultivos
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot8.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''
#### Gráfica de mejores municipios en términos de las distintas variables y cultivos
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot9.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''
#### Gráfica de mejores cultivos en términos de las distintas variables y años
'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot10.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)


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



