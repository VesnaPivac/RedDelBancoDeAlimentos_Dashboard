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

- **Análisis Temporal**: ¿En qué épocas del año es más probable que se generen excedentes?
- **Análisis Geográfico**: ¿En qué localidades existe una mayor probabilidad de acumulación de excedentes?
- **Análisis de Cultivo**: ¿Qué cultivos muestran una tendencia a ser producidos en exceso con mayor frecuencia?
- **Análisis Económico**: ¿Para qué época/cultivo/localidad el comportamiento económico sugiere la posibilidad de que se generen excedentes?

Para llevar a cabo cada uno de los análisis, empleamos widgets que posibilitaron un examen interactivo del comportamiento de las diversas variables en nuestros datos. Estos widgets nos permitieron explorar de manera dinámica los valores temporales, geográficos y de cultivo. A raíz de este análisis exhaustivo de todas las variables, decidimos focalizar nuestro enfoque exclusivamente en nuestro territorio estatal, Sonora, considerando sus municipios y los cultivos que son activamente producidos aquí. A continuación se presenta cada una de las gráficas empleadas. Se utiliza como ejemplo a la Uva, cultivo para el cual Sonora se posiciona como el principal estado productor. Cabe mencionar que, aunque el análisis económico no tiene su propia sección, este se realizó mediante la manipulación pertinente de las variables en los widgets de las gráficas  
'''

st.markdown(body)

st.divider()

body = '''
## Análisis Temporal

#### Gráfica de valores mensuales de las distintas variables y cultivos

De manera general, en esta gráfica resalta le hecho de que cada cultivo tiene distintas épocas del año destinadas a sus procesos agrícolas. Además, permite comparar cómo los valores, tanto de las variables agrícolas como las económicas, de cada época han variado en los distintos años analizados. 


'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot1.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''


#### Gráfica de valores acumulados de las distintas variables y cultivos

Aunque en la visualización previa podemos darnos una idea de los cambios que han ocurrido a través de los años, esta gráfica acumulada permite realizar una comparación más concreta. Esto es porque al comparar simplemente las barras de los meses de diciembre, podemos saber en qué año los valores fueron mayores o menores.

'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot2.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''


#### Gráfica de mejores meses en términos de las distintas variables y cultivos

De manera más cuantitativa, esta visualización nos permite saber cuál, y en qué magnitud, es la mejor época de cada cultivo en términos de las distintas variables analizadas.

'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot3.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''


#### Gráfica de evolución de las distintas variables y cultivos a lo largo del tiempo

Esta visualización arroja una idea global de cómo han evolucionado las distintas variables de cada cultivo a lo largo de todo el periodo de interés. Esto permite identificar cambios abruptos en épocas particulares, dando a pauta que futuros proyecto se interesen en entender las causas detrás de dichos cambios.


'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot4.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''


#### Gráfica de correlación entre variables a lo largo del tiempo para los distintos cultivos

Esta es una versión duplicada de la visualización anterior, permitiendo inspeccionar la posible correlación entre variables económicas y/o agrícolas de los cultivos.

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

Esta visualización tiene dos utilidades principales. La primera es que permite apreciar cómo se distribuyen los valores de las variables agrícolas y ecónomicas en los distintos estados del país. La segunda, siguiendo con la linea de la gráfica previa, permite visualizar posibles correlaciones entre las variables agrícolas y económicas a lo largo del territorio nacional. 

'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot6.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''


#### Gráfica de mejores estados en términos de las distintas variables y cultivos

Esta visualización es un aterrizado cuantitativo de lo visto en la gráfica anterior. Nos ofrece un ordenamiento de los estados en términos de las distintas variables analizadas.


'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot7.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''


#### Treemap de municipios en términos de las distintas variables y cultivos

En esta gráfica podemos observar qué municipios, y en qué magnitud, tienen el dominio de los distintos cultivos en términos de sus variables agrícolas.  

'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot8.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

body = '''


#### Gráfica de mejores municipios en términos de las distintas variables y cultivos

Esta visualización nos permite saber el orden de los municipios de manera cuantificada en términos de las variables económicas y agrícolas. 

'''

st.markdown(body)

url = 'https://raw.githubusercontent.com/VesnaPivac/RedDelBancoDeAlimentos_Dashboard/main/images/plot9.png'

response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img)

st.divider()

body = '''
## Análisis de cultivo

#### Gráfica de mejores cultivos en términos de las distintas variables y años

Esta gráfica nos permite identificar de manera cuantitativa, qué cultivos tienen mayor dominio en términos de sus variables económicas y agrícolas.


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



