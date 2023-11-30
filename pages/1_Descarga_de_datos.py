import streamlit as st
import pandas as pd
import numpy as np

st.title('Descarga de datos')

@st.cache_data
def load_data(x):
    if x == 'SIAP':
        data = pd.read_parquet('./data/SIAP.parquet')
    elif x == 'SNIIM':
        data = pd.read_parquet('./data/SNIIM.parquet')
    return data

data_siap = load_data('SIAP')
data_sniim = load_data('SNIIM')

st.subheader('SIAP: Servicio de Información Agroalimentaria y Pesquera')

body = '''
La principal fuente para la obtención de datos relacionados con la producción de alimentos en el campo es el Servicio de Información Agroalimentaria y Pesquera (SIAP). A esta plataforma se puede acceder por medio del siguiente enlace. Dentro de los datos de relevancia proporcionados por esta fuente se encuentran las hectareas de cultivo sembrada, cosechada y siniestrada, junto con su respectiva producción y rendimiento. Desde la perspectiva geográfica, la plataforma ofrece al usuario la posibilidad de solicitar estos datos para todos los municipios de cada estado. Por otro lado, la resolución temporal mínima permitida se basa en reportes con los avances mensuales de cada año.
Para la adquisición programática de los datos, es necesario realizar un request al endpoint https://nube.siap.gob.mx/avance_agricola/. Como resultado, se obtiene una cadena de texto en formato XML que contiene una tabla equivalente a la mostrada en la figura, pero cuyo contenido depende de los identificadores (ID's) proporcionados en el request. Es importante mencionar que estos ID no están disponibles directamente en la plataforma, por lo que fue necesario manipular los filtros para su obtención. Una vez adquiridos, los ID's fueron almacenados en un JSON, el cual fue añadido al presente repositorio (Victor-dict.json). Para la obtención de los datos de las cadenas de texto con formato XML es necesario aplicar un parsing utilizando BeautifulSoup, de modo que se facilite la identificación y extracción del contenido de cada una de las celdas.
Dado que el interés principal es obtener datos mensuales de cada cultivo desde 2018 hasta el presente año, el siguiente paso consistió en repetir este proceso anidadamente para los ID de años, meses y cultivos de interés. En cada iteración, el contenido de la tabla correspondiente a un mes de un año en particular se almacenó en un archivo CSV en la carpeta "raw" del presente repositorio, siguiendo el formato: "Avance_Agricola_año_mes.csv". A estos datos se la añade una columna "Cultivo", cuyo valor indica el cultivo al que se refieren los datos. En total, al tratarse de 6 años y 12 meses, se obtuvo un apróximado de 72 archivos (en realidad son menos porque el 2023 está incompleto). Posteriormente, estos archivos locales se volvieron a cargar en el entorno de programación para organizarlos de manera tidy. Esto implicó combinarlos en un único dataframe al que se le agregaron columnas para "año" y "mes". Debido a su tamaño (992213 filas con 10 columnas), este DataFrame se almacena en un archivo parquet, el cual fue añadido al repositorio.
Como nota, es necesario mencionar que no se iteró sobre las categorías de los filtros de Riego y Modalidad. En su lugar, en ambos casos se empleó la categoría que abarca a todas las otras.

#### Dataframe tidy

A continuación se muestra una descripción del DataFrame *SIAP* que resultó de la descarga y organización de los datos, el cual fue almacenado en formato parquet.

##### Información general

- **Nombre del DataFrame:** SIAP.parquet
- **Número de filas:** 992213
- **Número de columnas:** 10

##### Columnas

A continuación, se muestra una lista de las columnas en el DataFrame *tidy*, además de una breve descripción:

| **Columna**          | **Descripción**                                    | **Unidad** |
|----------------------|----------------------------------------------------|------------|
| Entidad              | Entidad a la que pertenece el dato                 |            |
| Municipio            | Nombre del municipio al que pertenece el dato     |            |
| Superficie Sembrada  | Superficie destinada a la siembra (hectareas)      | Hectarea  |
| Superficie Cosechada | Superficie cosechada                 | Hectarea |
| Superficie Siniestrada| Superficie siniestrada                 | Hectarea |
| Produccion           | Cantidad de producción         | Unidad de medida |
| Rendimiento          | Rendimiento del cultivo | Unidad de medida / hectarea |
| Anio                 | Año en el que se registraron los datos            |            |
| Mes                  | Mes en el que se registraron los datos            |            |
| Cultivo              | Tipo de cultivo                                    |            |

'''
st.markdown(body)
st.markdown('Aquí hay una muestra de cinco filas seleccionadas aleatoriamente del DataFrame para darnos una idea de cómo se ven los datos:')
st.dataframe(data_siap.sample(5))

if st.checkbox('Mostrar código'):
    st.markdown('  Se utilizó la siguiente función para realizar el request a la API de SIAP para realizar la descarga de los datos:')
    code_siap = '''
    def API_SIAP(anio,mes,cultivo):
    """Esta función permite hacer un request a la API de avance agrícola mensual y recibe como argumento el año,
        mes y cultivo del que queremos obtener la información. Los demás filtros reciben un valor fijo."""

    # Endpoint
    url = "https://nube.siap.gob.mx/avance_agricola/"

    # Diccionario con atributos del request
    payload = {'xajax': 'reporte', # Para obtener la tabla
    'xajaxr': '1696449941927', # Timestamp UNIX
    'xajaxargs[]': [
        '1', # 1: Desglose por estados, 2: Cultivo total
        str(anio), # Anio
        '5', # ID Ciclo
        '3', # ID Modalidad
        '0', # ID Estado (0: Nacional)
        '--',
        '--',
        str(cultivo), # ID Cultivo
        '200201',
        '0',
        '1', # 1: Por municipio
        'undefined',
        'undefined',
        'undefined',
        str(mes) # Valor del mes: va de 1 a 8, con 1 siendo Enero y 8 Agosto
        ]
    }

    headers = {
        'Cookie': 'PHPSESSID=45ri2k73cbp2iptcrufu88p360'
    }

    # Hacemos el request
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    response.encoding='ISO-8859-1'

    # Regresamos un string con el XML con la tabla que contiene los datos solicitados
    return response.text
    '''

    st.code(code_siap, language='python')


#---------------------------------------------------------------------------------------------------------------------------------------------------------------

st.divider()
st.subheader('SNIIM: Sistema Nacional de Información e Integración de Mercados')
body1 = '''
La obtención de datos del SNIIM se realiza mediante una clase "ScrapperMarketAgriculture" especializada en web scraping que automatiza el proceso. Esta clase gestiona las bibliotecas necesarias, como requests y BeautifulSoup, para realizar solicitudes web y analizar los resultados de estas solicitudes. En este caso, la solicitud a http://www.economia-sniim.gob.mx/NUEVO/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas arroja un HTML que contiene una tabla equivalente a la mostrada en la figura para un cultivo particular. Esta tabla contiene la información histórica de precios del cultivo en los distintas parejas de mercado de origen-destino de todo México. Tal como en los datos del SIAP, estamos interesados en el periodo que va del 2018 al presente. Aunque el periodo de tiempo entre dos instancias subsecuentes es variable, por lo general este es de varios días.
Cada producto de interés se trata como una instancia de esta clase, lo que permite una gestión controlada del proceso. En cada una de estas instancias se realiza un parsing con BeautifulSoup, a partir del cual se puede extraer el contenido de cada una de las celdas de la tabla. Este contenido se almacena en un DataFrame temporal. A su vez, este DataFrame se guarda en un archivo CSV cuyo nombre sigue el formato: "sniim_product_cultivo_calidad.csv". Estos archivos fueron añadidos la carpeta "raw" del presente repositorio.
Por último, la transformación de estos datos a un formato tidy implicó cargar y concatenar todos los archivos CSV. Tal como con los datos del SIAP, este nuevo DataFrame tidy se guardó en formato parquet, y se añadió al presente repositorio.
'''
st.markdown(body1)

text_sniim = '''
#### Dataframe Tidy
A continuación se muestra una descripción del DataFrame *SNIIM* que resultó de la descarga y organización de los datos, el cual fue almacenado en formato parquet.

##### Información general

- **Nombre del DataFrame:** SNIIM.parquet
- **Número de columnas:** 9

##### Columnas

A continuación, se muestra una lista de las columnas en el DataFrame *tidy*, junto con una breve descripción de cada una:
| **Columna**    | **Descripción**                                  |
|--------------  |--------------------------------------------------|
| Fecha         | Fecha de los registros de precios                |
| Presentacion  | Tipo de presentación del producto                |
| Origen        | Origen del producto                              |
| Destino       | Destino del producto                             |
| Precio_min    | Precio mínimo del producto                       |
| Precio_max    | Precio máximo del producto                       |
| Precio_frec   | Precio frecuente del producto                    |
| Observacion   | Observación sobre los registros                  |
| Cultivo       | Nombre del cultivo                               |

'''
st.markdown(text_sniim)

st.markdown('Aquí hay una muestra de cinco filas seleccionadas aleatoriamente del DataFrame para que se tenga una idea de cómo se ven los datos:')
st.dataframe(data_siap.sample(5))

if st.checkbox('Mostrar código  '):
    st.markdown('  Se utilizaron las siguiente funciones para realizar la descarga de los datos del SNIIM:')
    code_sniim = '''
    class ScrapperMarketAgriculture:
        total_records = 0
        inserted_records = 0
        current_product = 'None'
        first_print = True

        base_url = 'http://www.economia-sniim.gob.mx/NUEVO/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas'
        init_urls = [
            ['Frutas y Hortalizas', '/ConsultaFrutasYHortalizas.aspx', '/ResultadosConsultaFechaFrutasYHortalizas.aspx'],
            ['Flores', '/ConsultaFlores.aspx?SubOpcion=5', '/ResultadosConsultaFechaFlores.aspx'],
            ['Granos', '/ConsultaGranos.aspx?SubOpcion=6', '/ResultadosConsultaFechaGranos.aspx'],
            ['Aceites', '/ConsultaAceites.aspx?SubOpcion=8', '/ResultadosConsultaFechaAceites.aspx']
        ]

        last_year = 2023

        def __init__(self, *args, **kwargs):
            self.is_historic = kwargs.get('is_historic', True)
            self.df = pd.DataFrame()

        def read_category(self, category, url, url_form):
            category_page = requests.get(self.base_url + url)
            category_page = BeautifulSoup(category_page.content, features="html.parser")

            products = [(product.getText(), product['value'], ) for product in category_page.select_one('select#ddlProducto').find_all('option')]

            for product in products[105:]:
                product_name, product_id = product
                if product_id == '-1':
                    continue

                if self.current_product != 'None':
                prod = re.sub(r'\s','_',self.current_product)
                self.df.to_csv(f'./raw/SNIIM/sniim_product_{prod}.csv', index=False)
                self.current_product = str(product_name).lower().replace('-','').replace('  ', '_')
                self.first_print = True
                self.df = pd.DataFrame()

                with indent(4):
                    puts(colored.magenta("Producto: {}".format(self.current_product)))

                if self.is_historic:
                    for year in range(2018, 2024):
                        payload = {
                            'fechaInicio':'01/01/{0}'.format(str(year)),
                            'fechaFinal':'01/01/{0}'.format(str(year + 1)),
                            'ProductoId':product_id,
                            'OrigenId':'-1',
                            'Origen':'Todos',
                            'DestinoId':'-1',
                            'Destino':'Todos',
                            'PreciosPorId':'2',
                            'RegistrosPorPagina':'1000'
                        }

                        if not self.gather_prices(payload, url_form):
                            continue
                else:
                    today = datetime.datetime.today()
                    deleta = datetime.timedelta(days=-1)
                    payload = {
                            'fechaInicio':'{}'.format(today.strftime('%d/%m/%Y')),
                            'fechaFinal':'{}'.format((today).strftime('%d/%m/%Y')),
                            'ProductoId':product_id,
                            'OrigenId':'-1',
                            'Origen':'Todos',
                            'DestinoId':'-1',
                            'Destino':'Todos',
                            'PreciosPorId':'2',
                            'RegistrosPorPagina':'1000'
                        }

                    if not self.gather_prices(payload, url_form):
                        continue

            return

        def scraping(self):
            self.total_records = 0
            self.inserted_records = 0

            for category, url, url_form in self.init_urls:
                self.read_category(category, url, url_form)
                time.sleep(60)

        def gather_prices(self, payload, url_form):
            with indent(4):
                puts(colored.blue("Peticion: {}".format(str(payload))))

            response = requests.get(self.base_url + url_form, params=payload)
            time.sleep(30)
            if response.status_code != 200:
                with indent(4):
                    puts(colored.red("Error en la peticion HTTP: {}".format(str(response.text))))
                return False

            product_prices = BeautifulSoup(response.content, features="html.parser")

            try:
                table_prices = product_prices.select_one('table#tblResultados')
            except Exception as error:
                with indent(4):
                    puts(colored.red("Error en el parseo: {}".format(str(error))))
                return False

            fields = ('fecha', 'presentacion', 'origen', 'destino', 'precio_min', 'precio_max', 'precio_frec', 'obs')
            counter_row = 0

            for observation in table_prices.find_all('tr'):
                if counter_row > 1:
                    row = {}
                    counter_field = 0
                    if self.first_print:
                    self.first_print = False
                    for metric in observation.find_all('td'):
                        row[fields[counter_field]] = metric.getText()
                        counter_field += 1

                    row['name'] = self.current_product
                    df2 = pd.DataFrame(row, index=[0]) 
                    self.df = pd.concat([self.df, df2])

                self.total_records += 1
                counter_row += 1
                if self.total_records % 1000 == 0:
                prod = re.sub(r'\s','_',self.current_product)
                self.df.to_csv(f'./raw/SNIIM/sniim_product_{prod}.csv', index=False) 
            return True
    '''

    st.code(code_sniim, language='python')
