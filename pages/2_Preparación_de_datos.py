import streamlit as st
import pandas as pd
import numpy as np

st.title('Preparación de datos')

body = '''
El proceso de preparación de datos se ejecutó de manera individualizada para cada uno de los dos conjuntos de datos con los que trabajamos: SIAP y SNIIM. Aunque los procedimientos son en su mayoría idénticos, cada conjunto de datos demandó tratamientos específicos. Comenzaremos detallando la serie de pasos que delinearon el proceso de preparación de datos para el conjunto SIAP y procederemos a hacer lo mimso para el conjunto SNIIM.

'''

st.markdown(body)

st.divider()

body = '''

## SIAP

Los pasos que conformaron el proceso de preparación de los datos del SIAP fueron:

1. Aplicación de filtros
2. Ajuste de los tipos de datos
3. Análisis de valores faltantes
4. Obtención de valores mensuales
5. Análisis de valores atípicos

#### 1. Aplicación de filtros

Con base en la retroalimentación proporcionada por nuestro canal de comunicación con la Red BAMX, se implementó un proceso de filtrado con el objetivo de refinar y focalizar nuestro conjunto de datos.

- **Filtrado por año**

Los datos son inicialmente filtrados según la variable "Año", limitándonos exclusivamente a aquellos correspondientes a los años 2020 en adelante. Este criterio temporal asegura que nuestra análisis se centre en la información más reciente y relevante.

- **Filtrado por cultivo**

En consonancia con las recomendaciones proporcionadas, también aplicamos un filtro basado en la variable "Cultivo". Nos enfocamos únicamente en los cultivos de interés para la Red BAMX. Esta selección específica incluye los siguientes cultivos: Tomate rojo (jitomate), Chile verde, Limón, Pepino, Plátano, Mango, Garbanzo, Brócoli, Cebolla, Sandía, Papaya, Calabacita, Lechuga, Tomate verde, Espárrago, Frambuesa, Nopalitos, Nuez, Fresa, Toronja (pomelo), Zarzamora, Piña, Coliflor, Frijol, Berenjena, Uva, Guayaba, Naranja, Papa, Melón, Manzana, Pera, Durazno.

#### 2. Ajuste de los tipos de datos
 
Al realizar una revisión de cada columna, se identificó que variables claramente numéricas estaban inicialmente codificadas como objects. Estas variables incluían: Superficie Sembrada, Superficie Cosechada, Producción y Rendimiento. La raíz de este problema radicaba en que los valores dentro de estas variables utilizaban comas como separadores de miles. Por lo tanto, para llevar a cabo la conversión de tipo de dato a flotante, fue necesario eliminar primero este carácter. Este proceso de ajuste aseguró la coherencia en la representación numérica de los datos, facilitando los análisis posteriores.

#### 3. Análisis de valores faltantes

La busqueda de valores faltantes reveló su ausencia en nuestros datos. Por lo tanto, no fue necesario llevar a cabo ningún procedimiento adicional para abordar valores faltantes. 

#### 4. Obtención de valores mensuales

De manera predeterminada, el sistema del SIAP presenta los datos numéricos (Superficie Sembrada, Superficie Cosechada, Superficie Siniestrada, Producción y Rendimiento) en forma acumulativa. En este contexto, los valores para un mes específico, por ejemplo, febrero, se calculan sumando los valores de enero y febrero. De manera análoga, los valores de marzo se obtienen sumando los de enero, febrero y marzo, y así sucesivamente. Dado nuestro interés en analizar los datos de manera mensual, hemos implementado una transformación que resta los valores de los meses anteriores a los de cada mes en particular. 

Es importante destacar que, a pesar de esta transformación, hemos optado por retener los datos acumulativos originales como referencia. Esto nos permite verificar la corrección de los valores mensuales y brinda la posibilidad de utilizar los datos acumulativos en análisis futuros.

#### 5. Análisis de valores atípicos

Para la detección de valores atípicos se implementaron los dos métodos: *Local Outlier Factor* (LOF) y *Isolation Forest* (IF). Los resultados obtenidos por cada método se resumen a continuación:


| **Método**                   | **Cantidad de valores atípicos detectados**      | **Porcentaje del total de datos**  |
|------------------------------|--------------------------------------------------|------------------------------------|
| Local Outlier Factor         | 29552                                            | 7.82%                              |
| Isolation Forest             | 20338                                            | 5.38%                              |


No obstante, la revisión de los datos clasificados como atípicos por estos métodos no reveló patrones verdaderamente anómalos. A pesar de reconocer nuestra limitada experiencia en el ámbito agrícola, los datos identificados como supuestamente atípicos parecían simplemente reflejar períodos fluctuantes de rendimiento para diversos cultivos. Con base en esta observación, se tomó la decisión de mantener el conjunto de datos sin eliminar los datos señalados como atípicos. Este enfoque se fundamenta en la comprensión de que estos valores podrían representar variaciones normales en la producción agrícola, sin necesariamente indicar anomalías significativas.

'''

st.markdown(body)

st.divider()

body = '''

## SNIIM

Los pasos que conformaron el proceso de preparación de los datos del SNIIM fueron:

1. Aplicación de filtros
2. Ajuste de los tipos de datos
3. Análisis de valores faltantes
4. Ajuste de nombres de estados
5. Ajuste de nombre de cultivos
6. Obtención de precios mensuales
7. Análisis de valores atípicos

#### 1. Aplicación de filtros

Se emplearon de manera idéntica los filtros temporales y por tipo de cultivo que fueron utilizados en el tratamiento del conjunto de datos del SIAP.

#### 2. Ajuste de los tipos de datos
 
La revisión de cada columna evidenció que todas las variables concordaban con sus tipos de datos esperados, excepto la variable "Fecha". Los valores de esta columnas eran de tipo object, por lo que decidimos transformarlos a datetime para facilitar posibles análisis futuros.

#### 3. Análisis de valores faltantes

Tal como en el conjunto de datos del SIAP, no se identificaron valores faltantes, por lo que no fue necesario efectuar algún tratamiento adicional a los datos.

#### 4. Ajuste de nombres de estados

Con la finalidad de homogeneizar los valores de las variables compartidas entre ambos conjuntos de datos, se llevó a cabo un análisis para identificar aquellos estados en el conjunto de datos del SNIIM que presentaban denominaciones diferentes en comparación con el conjunto de datos del SIAP. Estas discrepancias en los nombres fueron corregidas en el conjunto de datos del SNIIM para garantizar la coherencia y comparabilidad entre ambos conjuntos de datos.

#### 5. Ajuste de nombre de cultivos

Siguiendo la misma línea que en el punto anterior, se procedió a estandarizar las denominaciones de los cultivos en ambos conjuntos de datos. Se identificó una disparidad, donde el SIAP utiliza nombres específicos de cultivos, tales como Papa, Melón, Manzana, Pera, entre otros, mientras que en el SNIIM se emplean denominaciones que incluyen el nombre de la variedad del cultivo, como por ejemplo: piña chica_primera, col mediana_primera, melón cantaloupe, entre otros.

Para lograr la homogeneización de los nombres, se implementaron expresiones regulares que conservan únicamente la primera palabra de las denominaciones del SNIIM y capitalizan la primera letra. Es relevante mencionar que esta metodología se aplicó exclusivamente a aquellos cultivos cuyos nombres en el SIAP estaban conformados por una sola palabra. En contraste, para los cultivos con nombres compuestos por más de una palabra (por ejemplo, Tomate rojo (jitomate), Chile verde, Tomate verde, Toronja (pomelo)), se llevó a cabo una modificación manual de sus nombres para asegurar la coherencia y uniformidad en la representación de los cultivos en ambos conjuntos de datos.

#### 6. Obtención de precios mensuales

Como último paso en el proceso de homogeneización de los conjuntos de datos, se procedió a obtener los precios promedio mensuales. Dicha acción fue necesaria debido a la diferencia en la granularidad de los datos, ya que los valores del SIAP se presentan de manera mensual, mientras que los precios del SNIIM se registran a diario. Este ajuste permitió establecer una comparación coherente y mensual entre las variables de interés, asegurando una alineación temporal adecuada en la información de ambos conjuntos de datos.

#### 7. Análisis de valores atípicos

Del mismo modo que con el conjunto de datos del SIAP, se utilizaron los métodos *Local Outlier Factor* y *Isolation Forest*. Los resultados de estos métodos se resumen a continuación:


| **Método**                   | **Cantidad de valores atípicos detectados**      | **Porcentaje del total de datos**  |
|------------------------------|--------------------------------------------------|------------------------------------|
| Local Outlier Factor         | 25717                                            | 8.99%                              |
| Isolation Forest             | 48582                                            | 16.98%                              |


Sin embargo, de manera análoga a lo observado en el conjunto de datos del SIAP, la revisión de los datos señalados como atípicos no reveló patrones verdaderamente anómalos. Se identificaron observaciones de productos como la nuez, cuyo precio elevado es conocido de antemano y, por lo tanto, no puede considerarse simplemente como atípico. Por lo tanto, se decidió conservar estos supuestos datos atípicos y continuar con el conjunto de datos completo. 

'''

st.markdown(body)
