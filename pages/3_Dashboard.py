import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import calendar



st.title('Red del Banco de Alimentos')
st.markdown('## Producción en Sonora y su actividad economica')
st.divider()


# Funciones
@st.cache_data
def load_data_SIAP_SNIIM():
    data = pd.read_parquet('./data/SIAP_SNIIM_preprocessed.parquet')
    return data

# Lectura de datos
df_merge = load_data_SIAP_SNIIM()


# Filtros
curr_year = datetime.now().year

curr_year = datetime.now().year
tiempos = ['Año Actual', 'Ultimos 3 años','Historico']
opcion_tiempo = st.selectbox('Tiempo:', tiempos, index=0,  placeholder="Choose an option")
tiempos_dict = {'Año Actual':datetime.now().year,'Ultimos 3 años':[datetime.now().year,datetime.now().year-1,datetime.now().year-2]}
if(opcion_tiempo == 'Historico'):
    df_merge_cultivo = df_merge.loc[(df_merge['Entidad']=='Sonora')]
elif(opcion_tiempo == 'Ultimos 3 años'):
    df_merge_cultivo = df_merge.loc[(df_merge['Entidad']=='Sonora')&(df_merge['Año'].isin(tiempos_dict[opcion_tiempo]))]
elif(opcion_tiempo == 'Año Actual'):
    df_merge_cultivo = df_merge.loc[(df_merge['Entidad']=='Sonora')&(df_merge['Año']==curr_year)]
    
# Calcular la suma de la producción por 'Cultivo'
suma_por_cultivo = df_merge_cultivo.groupby('Cultivo')['Produccion'].sum()
# Filtrar para los cultivos donde la suma de la producción no sea igual a cero
cultivos_con_produccion = suma_por_cultivo[suma_por_cultivo != 0.0].index

estados = np.sort(cultivos_con_produccion)
opcion_cultivo = st.selectbox('Cultivo:', estados, index=0,  placeholder="Choose an option")



# Primeras dos columnas
col1, col2 = st.columns(2)

with col1:

    if(opcion_tiempo == 'Historico'):
        cultivo_seleccionado = df_merge[df_merge['Cultivo'] == opcion_cultivo]
    elif(opcion_tiempo == 'Ultimos 3 años'):
        cultivo_seleccionado = df_merge[(df_merge['Cultivo'] == opcion_cultivo)&(df_merge['Año'].isin(tiempos_dict[opcion_tiempo]))]
    elif(opcion_tiempo == 'Año Actual'):
        cultivo_seleccionado = df_merge[(df_merge['Cultivo'] == opcion_cultivo)&(df_merge['Año']==curr_year)]
        

    # Calcular la producción total para el cultivo seleccionado en todos los estados
    produccion_total = cultivo_seleccionado['Produccion'].sum()

    # Calcular la producción total por entidad y ordenar de mayor a menor
    produccion_por_entidad = cultivo_seleccionado.groupby('Entidad')['Produccion'].sum().sort_values(ascending=False)

    # Seleccionar solo los primeros 3 elementos con mayor producción
    top_3_entidades = produccion_por_entidad.head(3)

    # Calcular el porcentaje de la producción de cada entidad con respecto a la producción total
    porcentaje_total = (top_3_entidades / produccion_total) * 100
    
    prd_son = produccion_por_entidad['Sonora']
    pct_mexico_son = (prd_son * 100)/produccion_total
    pct_mexico_son_text = str(round(pct_mexico_son,2))+"%"

    st.subheader(f'Producción Total de {opcion_cultivo}')
    st.markdown(f'##### Producción total de {opcion_cultivo} en México de <span style="color: #272F7C">{str("{:,}".format(round(produccion_total,2)))}</span> toneladas del cual Sonora aporta <span style="color: MediumPurple">{str("{:,}".format(round(prd_son,2)))}</span> toneladas que equivale al <span style="color: #9867CB">{pct_mexico_son_text}</span> del total',unsafe_allow_html=True)
    # Crear un DataFrame con los datos de producción total y en Sonora
    data = {
        'Entidad': ['México', 'Sonora'],
        'Produccion': [produccion_total, prd_son]
    }
    df = pd.DataFrame(data)

    # Definir colores para México (gris) y Sonora (morado)
    colors = {'México': '#272F7C', 'Sonora': '#9867CB'}

    # Graficar utilizando Plotly Express y asignar colores específicos a cada barra
    fig = px.bar(df, x='Entidad', y='Produccion', text='Produccion',
                labels={'Produccion': 'Producción'}, 
                color='Entidad', color_discrete_map=colors)

    fig.update_traces(textposition='outside', textfont=dict(color='black'), showlegend=False) 
    fig.update_layout(height=450, width=650)
    fig.update_xaxes(title=None)
        
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)



with col2:
   st.markdown(f"## Producción de {opcion_cultivo} en México")


st.divider()

# col1_1, col2_1, col3_1 = st.columns([1,3,1])
col1_1, col2_1 = st.columns(2)

with col1_1:
   
    st.markdown(f"## Top 3: Producción de {opcion_cultivo} por Entidad")
    st.text(f"Porcentaje con respecto a la producción total")
    data_plot = {
        'Entidad': top_3_entidades.index,
        'Producción Acumulada': top_3_entidades.values,
        'Porcentaje con respecto a la producción total': porcentaje_total.values.round(2)
    }
    df_plot = pd.DataFrame(data_plot)
    df_plot['Porcentaje con respecto a la producción total'] = df_plot['Porcentaje con respecto a la producción total'].astype(str) + '%'

    # Ordenar de mayor a menor
    df_plot = df_plot.sort_values('Producción Acumulada', ascending=True)

    # Crear gráfico de barras horizontales con Plotly Express
    fig = px.bar(df_plot, x='Producción Acumulada', y='Entidad', text='Porcentaje con respecto a la producción total',
                orientation='h',
                labels={'Producción Acumulada': 'Producción Acumulada'})
    fig.update_yaxes(title=None)
        
    # Definir colores para todas las barras, excepto la más grande
    if df_plot.Entidad[0] == 'Sonora':
        colors = ['gray'] * (len(df_plot) - 1) + ['#9867CB']
    else:
        colors = ['gray'] * (len(df_plot) - 1) + ['#81B4E3']  # Todas en gris excepto la más grande en morado

    # Configurar colores de las barras
    fig.update_traces(marker=dict(color=colors))
    fig.update_traces(textposition='outside', textfont=dict(color='black'))
    fig.update_layout(height=300, width=400)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig,use_container_width=True) 
    mayor_productor = df_plot.Entidad[0] 
    if(mayor_productor == 'Sonora'):
        st.markdown(f'##### {mayor_productor} es el mayor productor de {opcion_cultivo} con <span style="color: #9867CB">{df_plot["Porcentaje con respecto a la producción total"][0]}</span> de la producción total del país',unsafe_allow_html=True)
    else:
        st.markdown(f'##### {mayor_productor} es el mayor productor de {opcion_cultivo} con <span style="color: #81B4E3">{df_plot["Porcentaje con respecto a la producción total"][0]}</span> de la producción total del país',unsafe_allow_html=True)

with col2_1:
        
    
    # Definir el orden deseado de los meses
    orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    produccion_por_mes = cultivo_seleccionado.groupby('Mes')['Produccion'].sum().reset_index()

    # Convertir la columna 'Mes' a tipo Categorical con el orden deseado
    produccion_por_mes['Mes'] = pd.Categorical(produccion_por_mes['Mes'], categories=orden_meses, ordered=True)

    # Reordenar los datos según el orden de los meses
    produccion_por_mes = produccion_por_mes.sort_values('Mes')

    # Calcular la producción total
    produccion_total = produccion_por_mes['Produccion'].sum()

     # Meses ordenados de mayor a menor produccion
    produccion_por_mes_ordenado = produccion_por_mes.sort_values('Produccion', ascending=False)

    # Seleccionar los tres meses con mayor producción
    top_3_meses = produccion_por_mes_ordenado.head(3)['Mes'].tolist()


    # Normalizar la producción para usarla como intensidad de color
    produccion_normalizada = (produccion_por_mes['Produccion'] - produccion_por_mes['Produccion'].min()) / (produccion_por_mes['Produccion'].max() - produccion_por_mes['Produccion'].min())

    # Crear una paleta de colores de blanco a púrpura (o cualquier color deseado)
    colores = plt.cm.Blues(produccion_normalizada)

    # Crear el gráfico de barras con colores proporcionales a la producción
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(produccion_por_mes['Mes'], produccion_por_mes['Produccion'], color=colores)

    # Configurar etiquetas y título
    ax.set_xlabel('Mes')
    ax.set_ylabel('Producción')

    # Ajustar el diseño para que los nombres de los meses se muestren correctamente
    plt.xticks(rotation=45, ha='right')

    # Agregar etiquetas de porcentaje encima de cada barra
    for bar in bars:
        height = bar.get_height()
        percentage = (height / produccion_total) * 100
        ax.annotate(f'{percentage:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                    textcoords='offset points', ha='center', va='bottom')

    # Mostrar el gráfico en Streamlit
    st.markdown("## Producción Anual Nacional (%)")
    st.markdown(f"###### La mayor producción de {opcion_cultivo} se obtiene de los meses de {top_3_meses[0]}, {top_3_meses[1]} y {top_3_meses[2]}")

    st.pyplot(fig)

st.divider()


st.markdown(f"## Producción Anual Promedio de {opcion_cultivo}")
    







