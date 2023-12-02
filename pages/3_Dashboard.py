import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime



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


    st.subheader(f'Producción Total de {opcion_cultivo}')
    prd_son = produccion_por_entidad['Sonora']
    st.markdown(f'##### Producción total de {opcion_cultivo} en México de {str("{:,}".format(round(produccion_total,2)))} toneladas del cual Sonora aporta {str("{:,}".format(round(prd_son,2)))} toneladas')
    # Crear un DataFrame con los datos de producción total y en Sonora
    data = {
        'Entidad': ['México', 'Sonora'],
        'Produccion': [produccion_total, prd_son]
    }
    df = pd.DataFrame(data)

    # Definir colores para México (gris) y Sonora (morado)
    colors = {'México': 'gray', 'Sonora': 'purple'}

    # Graficar utilizando Plotly Express y asignar colores específicos a cada barra
    fig = px.bar(df, x='Entidad', y='Produccion', text='Produccion',
                labels={'Produccion': 'Producción'}, 
                color='Entidad', color_discrete_map=colors)

    fig.update_traces(textposition='outside', textfont=dict(color='black')) 
    fig.update_layout(height=450, width=650)
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)


    st.divider()


    st.markdown(f"### Top 3: Producción de {opcion_cultivo} por Entidad")
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
    colors = ['gray'] * (len(df_plot) - 1) + ['MediumPurple']  # Todas en gris excepto la más grande en morado

    # Configurar colores de las barras
    fig.update_traces(marker=dict(color=colors))
    fig.update_traces(textposition='outside', textfont=dict(color='black'))
    fig.update_layout(height=300, width=600)
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig) 
    mayor_productor = df_plot.Entidad[0] 
    st.markdown(f'##### {mayor_productor} es el mayor productor de {opcion_cultivo} con {df_plot["Porcentaje con respecto a la producción total"][0]} de la producción total del país')


with col2:
   st.markdown(f"### Producción de {opcion_cultivo} en México")


