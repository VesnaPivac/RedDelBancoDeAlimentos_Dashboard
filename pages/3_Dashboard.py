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
opcion_tiempo = st.selectbox('Periodo:', tiempos, index=0,  placeholder="Choose an option")
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
    st.markdown(f'##### Producción total de {opcion_cultivo} en México de <span style="color: #272F7C">{str("{:,}".format(round(produccion_total,2)))}</span> toneladas del cual Sonora aporta <span style="color: #9867CB">{str("{:,}".format(round(prd_son,2)))}</span> toneladas que equivale al <span style="color: #9867CB">{pct_mexico_son_text}</span> del total',unsafe_allow_html=True)
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
    st.markdown("## Producción Nacional (%)")
    st.markdown(f"###### La mayor producción de {opcion_cultivo} se obtiene de los meses de {top_3_meses[0]}, {top_3_meses[1]} y {top_3_meses[2]}")

    st.pyplot(fig)

st.divider()

col1_2, col2_2 = st.columns(2)

with col1_2:
    
    st.markdown(f"## Producción Promedio de {opcion_cultivo} en Pesos")

    cultivo_seleccionado['Precio total'] = cultivo_seleccionado['Produccion']*cultivo_seleccionado['Precio Frecuente']

    resultado = cultivo_seleccionado.groupby('Entidad').agg({'Produccion': 'sum', 'Precio total': 'sum','Rendimiento': 'sum'})
    resultado = resultado.sort_values('Precio total', ascending=False).head(10).reset_index()
    resultado['Precio total'] = resultado['Precio total'] / 1000000
    resultado = resultado[resultado['Precio total'] != 0]
    resultado = resultado.rename(columns={'Entidad': 'Estado', 'Produccion': 'Producción', 'Precio total': 'Precio Total (MDP)'})



    # Función para resaltar la fila de 'Sonora'
    def resaltar_sonora(row):
        if row['Estado'] == 'Sonora':
            return ['background-color: #E8D7FA'] * len(row)
        else:
            return [''] * len(row)

    # Aplicar estilo de resaltado
    styled_table = resultado.style.apply(resaltar_sonora, axis=1)
    styled_table = styled_table.format({'Producción': '{:.2f}', 'Precio Total (MDP)': '{:.4f}','Rendimiento':'{:.2f}'})
        
    # Mostrar el DataFrame en Streamlit
    st.write(styled_table)

with col2_2:
    st.markdown(f'## Valor de la producción total de {opcion_cultivo} en Sonora')
    meses = {'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6,'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12}
    
    df_merge_valor_produccion = df_merge.loc[(df_merge['Entidad']=='Sonora')&(df_merge['Cultivo']==opcion_cultivo)]
    df_merge_valor_produccion['Precio total'] = df_merge_valor_produccion['Produccion'] * df_merge_valor_produccion['Precio Frecuente']
    df_merge_valor_produccion['Mes'] = df_merge_valor_produccion['Mes'].map(meses)
    df_merge_valor_produccion['Fecha'] = pd.to_datetime(df_merge_valor_produccion['Año'].astype(str) + '-' + df_merge_valor_produccion['Mes'].astype(str))

    # Ordenar por fecha para asegurarse de que los datos estén en orden temporal
    df_merge_valor_produccion = df_merge_valor_produccion.sort_values('Fecha')
    
    tab1, tab2, tab3= st.tabs(["Producción","Precio Total","Rendimiento"])
    
    tab1.subheader("Producción total a lo largo del tiempo")
    fig = px.line(df_merge_valor_produccion, x='Fecha', y='Produccion', markers=True, line_shape='linear',color_discrete_sequence=['#9867CB'])
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Producción',
        xaxis=dict(tickangle=45),
        showlegend=False
    )
    tab1.plotly_chart(fig)

    tab2.subheader("Precio Total en Millones de Pesos (MDP) a lo largo del tiempo")
    df_merge_valor_produccion['Precio total'] = round((df_merge_valor_produccion['Precio total']/1000000),2)

    fig = px.line(df_merge_valor_produccion, x='Fecha', y='Precio total', markers=True, line_shape='linear',color_discrete_sequence=['#9867CB'])
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Precio Total (MDP)',
        xaxis=dict(tickangle=45),
        showlegend=False
    )
    tab2.plotly_chart(fig)

    
    tab3.subheader("Rendimiento total a lo largo del tiempo")
    fig = px.line(df_merge_valor_produccion, x='Fecha', y='Rendimiento', markers=True, line_shape='linear',color_discrete_sequence=['#9867CB'])
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Rendimiento',
        xaxis=dict(tickangle=45),
        showlegend=False
    )
    tab3.plotly_chart(fig)


st.divider()


col1_3, col2_3 = st.columns(2)

with col1_3:
    st.markdown(f'## Cultivo de {opcion_cultivo} en el estado de Sonora por municipios')

    df_municipio = pd.read_parquet('./data/Municipios.parquet')

    if(opcion_tiempo == 'Historico'):
        df_municipio = df_municipio[df_municipio['Cultivo'] == opcion_cultivo]
    elif(opcion_tiempo == 'Ultimos 3 años'):
        df_municipio = df_municipio[(df_municipio['Cultivo'] == opcion_cultivo)&(df_municipio['Año'].isin(tiempos_dict[opcion_tiempo]))]
    elif(opcion_tiempo == 'Año Actual'):
        df_municipio = df_municipio[(df_municipio['Cultivo'] == opcion_cultivo)&(df_municipio['Año']==curr_year)]
        
    # Filtramos para solo con valores de Produccion (%) mayores a cero para poder usar una escala de colores continua en el treemap
    df_municipio = df_municipio[df_municipio['Produccion (%)'] > 0]

    # Crear el treemap con plotly express
    fig = px.treemap(df_municipio,
                    path=["Entidad","Municipio"],
                    values="Produccion (%)",
                    color_discrete_map={'Entidad': "white"},  # Asignar blanco al      
                    width=650, height=600
                    )

    fig.update_traces(root_color="whitesmoke")

    st.plotly_chart(fig)

with col2_3:
    st.markdown(f"")