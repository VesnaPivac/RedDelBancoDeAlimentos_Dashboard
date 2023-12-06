import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import calendar
import requests



st.title('Agricultura Sonorense: Datos Esenciales de Nuestra Producción')
# st.markdown('## Agricultura Sonorense: Datos Esenciales de Nuestra Producción')


# Lectura de datos
df_merge = pd.read_parquet('./data/SIAP_SNIIM_preprocessed.parquet')


# Filtros
# curr_year = datetime.now().year

curr_year = datetime.now().year
years = df_merge['Año'].unique()
# tiempos = ['Año Actual', 'Ultimos 3 años','Historico']
# opcion_tiempo = st.selectbox('Periodo:', tiempos, index=0,  placeholder="Choose an option")
# tiempos_dict = {'Año Actual':datetime.now().year,'Ultimos 3 años':[datetime.now().year,datetime.now().year-1,datetime.now().year-2]}
# if(opcion_tiempo == 'Historico'):
#     df_merge_cultivo = df_merge.loc[(df_merge['Entidad']=='Sonora')]
# elif(opcion_tiempo == 'Ultimos 3 años'):
#     df_merge_cultivo = df_merge.loc[(df_merge['Entidad']=='Sonora')&(df_merge['Año'].isin(tiempos_dict[opcion_tiempo]))]
# elif(opcion_tiempo == 'Año Actual'):
opcion_tiempo = 'Año Actual'
tiempos_dict = curr_year
df_merge_cultivo = df_merge.loc[(df_merge['Entidad']=='Sonora')&(df_merge['Año']==curr_year)]
    
# Calcular la suma de la producción por 'Cultivo'
suma_por_cultivo = df_merge_cultivo.groupby('Cultivo')['Produccion'].sum()
# Filtrar para los cultivos donde la suma de la producción no sea igual a cero
cultivos_con_produccion = suma_por_cultivo[suma_por_cultivo != 0.0].index

estados = np.sort(cultivos_con_produccion)
opcion_cultivo = st.selectbox('Cultivo:', estados, index=0,  placeholder="Choose an option")


st.divider()
#-----------------------------------------SECCION 1 -------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
if(opcion_tiempo == 'Historico'):
    cultivo_seleccionado = df_merge[df_merge['Cultivo'] == opcion_cultivo]
elif(opcion_tiempo == 'Ultimos 3 años'):
    cultivo_seleccionado = df_merge[(df_merge['Cultivo'] == opcion_cultivo)&(df_merge['Año'].isin(tiempos_dict[opcion_tiempo]))]
elif(opcion_tiempo == 'Año Actual'):
    cultivo_seleccionado = df_merge[(df_merge['Cultivo'] == opcion_cultivo)&(df_merge['Año']==curr_year)]

color_mexico = '#272F7C'
color_sonora = '#9867CB'
    
# Primeras dos columnas
col1, col2 = st.columns(2)

with col1:
    df_estados = pd.read_parquet('./data/Estados.parquet')
    df_estados = df_estados.loc[df_estados['Cultivo']==opcion_cultivo]
    # Calcular la producción total para el cultivo seleccionado en todos los estados
    produccion_total = df_estados['Produccion'].sum()

    # Calcular la producción total por entidad y ordenar de mayor a menor
    produccion_por_entidad = df_estados.groupby('Entidad')['Produccion'].sum().sort_values(ascending=False)
    
    prd_son = produccion_por_entidad['Sonora']
    pct_mexico_son = (prd_son * 100)/produccion_total
    pct_mexico_son_text = str(round(pct_mexico_son,4))+"%"

    st.subheader(f'Producción Total de {opcion_cultivo}')
    st.markdown(f'##### Producción total de {opcion_cultivo} en México de <span style="color: {color_mexico}">{str("{:,}".format(round(produccion_total,2)))}</span> toneladas del cual Sonora aporta <span style="color:{color_sonora}">{str("{:,}".format(round(prd_son,2)))}</span> toneladas del total.',unsafe_allow_html=True)
    # Crear un DataFrame con los datos de producción total y en Sonora
    data = {
        'Entidad': ['México', 'Sonora'],
        'Produccion': [round(produccion_total,2), round(prd_son,2)]
    }
    df = pd.DataFrame(data)

    # Definir colores para México (gris) y Sonora (morado)
    colors = {'México': color_mexico, 'Sonora': color_sonora}

    # Graficar utilizando Plotly Express y asignar colores específicos a cada barra
    fig = px.bar(df, x='Entidad', y='Produccion', text='Produccion',
                labels={'Produccion': 'Producción'}, 
                color='Entidad', color_discrete_map=colors)

    fig.update_traces(textposition='outside', textfont=dict(color='black'), showlegend=False) 
    fig.update_layout(height=450, width=650)
    fig.update_xaxes(title=None)
    st.plotly_chart(fig)


with col2:
    st.markdown(f"## Producción de {opcion_cultivo} en México")
    
    df_estados = pd.read_parquet('./data/Estados.parquet')
    if opcion_tiempo == 'Año Actual':
        df_filtered = df_estados[(df_estados['Año'] == curr_year)&(df_estados['Cultivo'] == opcion_cultivo)]
    elif opcion_tiempo == 'Ultimos 3 años':
        df_filtered = df_estados[(df_estados['Año'].isin(tiempos_dict[opcion_tiempo]))&(df_estados['Cultivo'] == opcion_cultivo)]
    else:
        df_filtered = df_estados[(df_estados['Cultivo'] == opcion_cultivo)]
    
    # df_filtered = df_filtered[df_filtered['Cultivo'] == opcion_cultivo][['Entidad', 'Produccion','Produccion (%)']]
    # df_estados = df_estados[df_estados['Cultivo'] == opcion_cultivo][['Entidad', 'Produccion','Produccion (%)']]

    # Calcula la producción por entidad usando el DataFrame filtrado
    produccion_por_entidad = df_filtered.groupby('Entidad')['Produccion'].sum()

    # Encuentra la entidad con la producción máxima
    entidad_max_produccion = produccion_por_entidad.idxmax()

    repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
    mx_regions_geo = requests.get(repo_url).json()

    # Create a DataFrame with all states of Mexico
    all_states_df = pd.DataFrame({'Entidad': df_estados['Entidad'].unique()})

    # Define the function to plot the map
    def plot_map():
        # Merge with all_states_df to ensure all states are present
        merged_df = all_states_df.merge(df_filtered, on='Entidad', how='left')
        merged_df = merged_df.fillna(0)

        # st.table(merged_df)

        
        if entidad_max_produccion == 'Sonora':
            custom_color_scale = ["#F2EBFE", px.colors.sequential.Purples[-1]]  # Light purple to dark purple
        else:
            custom_color_scale = ["#D6EAF8", px.colors.sequential.Blues[-1]]  # Light blue to dark blue

        # Plot the choropleth map
        fig = px.choropleth(data_frame=merged_df,
                            geojson=mx_regions_geo,
                            locations='Entidad',
                            featureidkey='properties.name',
                            color='Produccion (%)',
                            color_continuous_scale=custom_color_scale
                            )

        
        fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

        
        fig.update_layout(
            geo=dict(
                showframe=False  # Hide the map frame borders
            )
        )

        return fig

    fig = plot_map()

    st.plotly_chart(fig)





#-----------------------------------------SECCION 2 -------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------

# st.divider()

col1_1, col2_1 = st.columns(2)

with col1_1:
    df = pd.read_parquet('./data/Estados.parquet')
     
    if opcion_tiempo == 'Año Actual':
        df = df[(df['Año'] == curr_year)]
    elif opcion_tiempo == 'Ultimos 3 años':
        df = df[(df['Año'].isin(tiempos_dict[opcion_tiempo]))]
    
    # Filtrar el DataFrame por el cultivo deseado y seleccionar las columnas 'Entidad' y 'Produccion'
    filtered_df = df[df['Cultivo'] == opcion_cultivo][['Entidad', 'Produccion']]

    # Calcular la suma de la producción por entidad
    produccion_por_entidad = filtered_df.groupby('Entidad')['Produccion'].sum()

    # Calcular la producción total de todos los cultivos
    produccion_total = produccion_por_entidad.sum()

    # Calcular la producción porcentaje de la producción total por entidad
    produccion_por_entidad = produccion_por_entidad.reset_index()  # Reiniciar el índice del DataFrame
    produccion_por_entidad['Porcentaje'] = (produccion_por_entidad['Produccion'] * 100) / produccion_total


    top3 = produccion_por_entidad.sort_values(by='Produccion',ascending=False)

    if 'Sonora' in (top3['Entidad'].head(3).tolist()):
        top3 = top3.head(3)
    else:
        top_son = top3.loc[top3['Entidad']=='Sonora']
        top3 = top3.head(3)
        top3 = pd.concat([top3,top_son],ignore_index=True)

    top3['Porcentaje'] = top3['Porcentaje'].round(3).astype(str) + '%'
    
    top3 = top3.sort_values('Produccion', ascending=True)

    # Asignar colores según las condiciones especificadas
    top3['Color'] = 'gray'  # Por defecto, todas las filas tienen el color gris

    # Si 'Sonora' está en el top 1
    if top3.iloc[-1]['Entidad'] == 'Sonora':
        top3.loc[top3['Entidad'] == 'Sonora', 'Color'] = 'purple'  # Asignar morado a 'Sonora' en el top 1

    # Si 'Sonora' está en el top 3 pero no en el top 1
    elif 'Sonora' in top3['Entidad'].tolist()[:3]:
        top3.loc[top3['Entidad'] == 'Sonora', 'Color'] = 'purple'  # Asignar morado a 'Sonora' en el top 3
        top3.loc[top3.index[-1], 'Color'] = 'blue'  # Asignar azul al top 1

    # Crear el gráfico con Plotly Express
    fig = px.bar(top3, x='Produccion', y='Entidad', orientation='h', color='Color',
                 text=top3['Porcentaje'],
                color_discrete_map={'gray': 'gray', 'purple': color_sonora, 'blue': '#81B4E3'},
                labels={'Produccion': 'Producción (Toneladas)', 'Entidad': 'Entidad'})
    
    fig.update_layout(showlegend=False)
    
    # Personalizar el diseño de texto (posición y formato)
    fig.update_traces(textposition='outside')  # Mostrar el texto fuera de las barras
    fig.update_layout(xaxis=dict(title='Producción', showgrid=True, gridcolor='lightgray'))  # Ajustar la apariencia del eje X

    mayor_productor = top3.iloc[-1]['Entidad']

    st.markdown(f"## Principales Entidades Contribuyentes a la Producción de {opcion_cultivo}")
    if top3.iloc[0]['Entidad'] == 'Sonora':
        st.text(f"Sonora y los tres principales productores.")


    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
    

    porcentaje_sonora = float(top3.loc[top3['Entidad'] == 'Sonora', 'Porcentaje'].str.rstrip('%').iloc[0])
    if mayor_productor == 'Sonora':
        st.markdown(f'##### {mayor_productor} es el mayor productor de {opcion_cultivo} con una aportación del <span style="color: {color_sonora}">{str(porcentaje_sonora) + "%"}</span> de la producción total del país',unsafe_allow_html=True)
    else:
        porcentaje_top1 = float(top3.loc[top3['Entidad'] == mayor_productor, 'Porcentaje'].str.rstrip('%').iloc[0])
        st.markdown(f'##### {mayor_productor} es el mayor productor de {opcion_cultivo} con <span style="color: #81B4E3">{str(porcentaje_top1)+"%"}</span> de la producción total del país mientras que Sonora aporta el <span style="color: {color_sonora}">{str(porcentaje_sonora)+"%"}</span> del total de producción.',unsafe_allow_html=True)

    st.markdown("<span style='font-size: 12px;'>* Porcentaje con respecto a la producción total</span>", unsafe_allow_html=True)


with col2_1:
        
    
    # Definir el orden deseado de los meses
    orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    cultivo_seleccionado_sonora = cultivo_seleccionado.loc[cultivo_seleccionado['Entidad']=='Sonora']
    produccion_por_mes = cultivo_seleccionado_sonora.groupby('Mes')['Produccion'].sum().reset_index()

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
    colores = plt.cm.Purples(produccion_normalizada)

    # GRAFICA -------------------------------------------------------------------------------------------------------------
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
    st.markdown("## Producción Estatal de Sonora (%)")
    st.markdown(f"###### La mayor producción de {opcion_cultivo} se obtiene de los meses de {top_3_meses[0]}, {top_3_meses[1]} y {top_3_meses[2]}")

    st.pyplot(fig)

    st.markdown("<span style='font-size: 12px;'>* Porcentaje con respecto a la producción total de Sonora</span>", unsafe_allow_html=True)







#-----------------------------------------SECCION 3 -------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------


st.divider()

col1_2, col2_2 = st.columns(2)

with col1_2:
    
    st.markdown(f"## Producción Promedio de {opcion_cultivo} en Pesos")

    cultivo_seleccionado['Precio total'] = cultivo_seleccionado['Produccion']*(cultivo_seleccionado['Precio Frecuente']*1000)

    resultado = cultivo_seleccionado.groupby('Entidad').agg({'Produccion': 'sum', 'Precio total': 'sum','Rendimiento': 'sum'})
    resultado = resultado.sort_values('Precio total', ascending=False).reset_index()
    resultado['Precio total'] = resultado['Precio total'] / 1000000
    resultado['Rendimiento Economico (MDP)'] = (resultado['Precio total'] * resultado['Produccion'])/1000000
    precio_total_pais = resultado['Precio total'].sum()
    precio_total_son = resultado.loc[resultado['Entidad']=='Sonora','Precio total'].sum()
    resultado = resultado[resultado['Precio total'] != 0]
    resultado = resultado.head(10)
    resultado = resultado.rename(columns={'Entidad': 'Estado', 'Produccion': 'Producción (Toneladas)', 'Precio total': 'Precio Total (MDP)'})

    resultado.set_index('Estado', inplace=True)

    # Función para resaltar la fila de 'Sonora'
    def resaltar_sonora(row):
        if row.name == 'Sonora':  # Utiliza row.name para referenciar el índice
            return ['background-color: #E8D7FA'] * len(row)
        else:
            return [''] * len(row)

    # Aplicar estilo de resaltado
    
    styled_table = resultado.style.apply(resaltar_sonora, axis=1)
    styled_table = styled_table.format({'Producción (Toneladas)': '{:,.2f}', 'Precio Total (MDP)': '{:,.4f}','Rendimiento':'{:,.2f}','Rendimiento Economico (MDP)':'{:,.2f}'})
    
    # Mostrar el DataFrame en Streamlit
    st.write(styled_table.set_caption('Estado'),unsafe_allow_html=True, width=400)

    if opcion_tiempo == 'Historico':
        precio_total_tiempo_txt = ' desde el 2020 hasta el año actual.'
    elif opcion_tiempo == 'Ultimos 3 años':
        precio_total_tiempo_txt = ' desde el ' + str(datetime.now().year - 2) + ' hasta el año actual.'
    elif opcion_tiempo == 'Año Actual':
        precio_total_tiempo_txt = ' en el año actual ' + str(datetime.now().year) + '.'

    st.markdown(f'##### La producción total de {opcion_cultivo} en todo México es de {"{:,}".format(round(precio_total_pais,2))} MDP del cual Sonora ha aportado <span style="color: {color_sonora}">{"{:,}".format(round(precio_total_son,2))}</span> MDP{precio_total_tiempo_txt}',unsafe_allow_html=True)




with col2_2:
    st.markdown(f'## Valor de la producción total de {opcion_cultivo} en Sonora')
    meses = {'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6,'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12}
    
    df_merge_valor_produccion = df_merge.loc[(df_merge['Entidad']=='Sonora')&(df_merge['Cultivo']==opcion_cultivo)]
    df_merge_valor_produccion['Precio total'] = df_merge_valor_produccion['Produccion'] * (df_merge_valor_produccion['Precio Frecuente']  * 1000)
    df_merge_valor_produccion['Mes'] = df_merge_valor_produccion['Mes'].map(meses)
    df_merge_valor_produccion['Fecha'] = pd.to_datetime(df_merge_valor_produccion['Año'].astype(str) + '-' + df_merge_valor_produccion['Mes'].astype(str))
    # df_merge_valor_produccion['Rendimiento Economico (MDP)'] = round(((df_merge_valor_produccion['Precio total'] * df_merge_valor_produccion['Produccion'])/1000000),2)

    # Ordenar por fecha para asegurarse de que los datos estén en orden temporal
    df_merge_valor_produccion = df_merge_valor_produccion.sort_values('Fecha')
    
    tab1, tab2, tab3= st.tabs(["Producción","Precio Total","Rendimiento"])
    
    tab1.subheader("Producción total a lo largo del tiempo")
    fig = px.line(df_merge_valor_produccion, x='Fecha', y='Produccion', markers=True, line_shape='linear',color_discrete_sequence=['#9867CB'])
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Producción (Toneladas)',
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
        yaxis_title='Rendimiento (Hectarea*Pesos)',
        xaxis=dict(tickangle=45),
        showlegend=False
    )
    tab3.plotly_chart(fig)





#-----------------------------------------SECCION 4 -------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------

st.divider()

col1_4, col2_4,col3_4 = st.columns([2,5,2])

with col2_4:
    st.markdown(f'## Superficie Sembrada, Cosechada y Siniestrada de {opcion_cultivo} en Sonora')
    #Cultivo y año    
    sembrada_vs_cosechada = df_merge.loc[(df_merge['Entidad'] == 'Sonora')&(df_merge['Cultivo']==opcion_cultivo)]
  
    sembrada_vs_cosechada['Mes'] = sembrada_vs_cosechada['Mes'].map(meses)
    sembrada_vs_cosechada['Fecha'] = pd.to_datetime(sembrada_vs_cosechada['Año'].astype(str) + '-' + sembrada_vs_cosechada['Mes'].astype(str))

    # Ordenar por fecha para asegurarse de que los datos estén en orden temporal
    sembrada_vs_cosechada = sembrada_vs_cosechada.sort_values('Fecha')
    
        
    # Graficar con Plotly Express
    fig = px.line(sembrada_vs_cosechada, x='Fecha', y=['Superficie Siniestrada','Superficie Cosechada', 'Superficie Sembrada'], 
                labels={'Fecha': 'Fecha', 'value': 'Superficie (Hectáreas)'})

    # Configuraciones adicionales si es necesario
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Superficie (Hectáreas)', legend_title='Tipo de Superficie')
    fig.update_traces(mode='lines')

    # Mostrar la figura en Streamlit
    st.plotly_chart(fig)
    







#-----------------------------------------SECCION 5 -------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------
st.divider()
col1_5, col2_5, col3_5, col4_5,col5_5= st.columns([1,2,1,2,1])

with col2_5:
    st.markdown(f"## Producción restante potencial:")
    potencial_cosechar = df_merge.copy()
    potencial_cosechar = potencial_cosechar.loc[(potencial_cosechar['Entidad'] == 'Sonora')&(potencial_cosechar['Año']==curr_year)&(potencial_cosechar['Cultivo']==opcion_cultivo)]
    num_meses = len(potencial_cosechar['Mes'].unique())
    rendimiento_promedio = potencial_cosechar['Rendimiento'].sum()/num_meses
    potencial_cosechar_kpi = (potencial_cosechar['Superficie Sembrada'].sum() - (potencial_cosechar['Superficie Cosechada'].sum() + potencial_cosechar['Superficie Siniestrada'].sum())) * rendimiento_promedio
    
    fig, ax = plt.subplots(figsize=(5, 0.1), dpi=500)
    ax.text(0.3, 0.3, str("{:,}".format(round(potencial_cosechar_kpi,2))), ha='center', va='center', fontsize=30, color='#9867CB')
    # ax.set_title("Producción Total")
    ax.axis('off')  # Desactivar ejes
    plt.tight_layout()

    st.pyplot(fig)


with col4_5:
    st.markdown(f"## Valor económico de la superficie por cosechar:")
    potencial_cosechar2 = df_merge.copy()
    potencial_cosechar2 = potencial_cosechar2.loc[(potencial_cosechar2['Entidad'] == 'Sonora')&(potencial_cosechar2['Año']==curr_year)&(potencial_cosechar2['Cultivo']==opcion_cultivo)]
    num_meses2 = len(potencial_cosechar2['Mes'].unique())
    rendimiento_promedio2 = potencial_cosechar2['Rendimiento'].sum()/num_meses2

    potencial_cosechar2['potencial_cosechar_kpi2'] = ((potencial_cosechar['Superficie Sembrada'].sum() - (potencial_cosechar['Superficie Cosechada'].sum() + potencial_cosechar['Superficie Siniestrada'].sum())) * rendimiento_promedio) * potencial_cosechar2['Precio Frecuente']
    # potencial_cosechar2['potencial_cosechar_kpi2'] = ((potencial_cosechar['Superficie Sembrada'].sum() - (potencial_cosechar['Superficie Cosechada'].sum() + potencial_cosechar['Superficie Siniestrada'].sum())) * rendimiento_promedio) * (potencial_cosechar2['Precio Frecuente'].sum() / len(potencial_cosechar2['Precio Frecuente'])) 

    
    potencial_cosechar_kpi2 = potencial_cosechar2['potencial_cosechar_kpi2'].sum()
    # Convertir a formato de texto con comas separadoras para los miles
    potencial_cosechar_kpi2_text = "{:,.2f}".format(round(float(potencial_cosechar_kpi2), 2))

    fig, ax = plt.subplots(figsize=(5, 0.1), dpi=500)
    ax.text(0.3, 0.3, '$'+str("{:,}".format(round(potencial_cosechar_kpi2,2))), ha='center', va='center', fontsize=30, color='#9867CB')
    # ax.set_title("Producción Total")
    ax.axis('off')  # Desactivar ejes
    plt.tight_layout()

    st.pyplot(fig)




#-----------------------------------------SECCION 6 -------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------




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
    custom_color_scale = ["#F2EBFE", px.colors.sequential.Purples[-1]] 

    # Crear el treemap con plotly express
    fig = px.treemap(df_municipio,
                    path=["Entidad","Municipio"],
                    values="Produccion (%)",
                    color_discrete_map={'Entidad': "white"},     
                    width=500, height=600
                    )

    fig.update_traces(root_color="whitesmoke")

    st.plotly_chart(fig)


with col2_3:
    st.markdown(f'## Superficie Sembrada, Cosechada y Siniestrada de {opcion_cultivo} por municipio')
    #Cultivo y año    
    df_municipio = pd.read_parquet('./data/Municipios.parquet')
    sembrada_vs_cosechada = df_municipio.copy()

    municipio_menu = sembrada_vs_cosechada['Municipio'].unique()
    opcion_mun = st.selectbox('Municipio:', municipio_menu, index=0,  placeholder="Choose an option")

    sembrada_vs_cosechada = sembrada_vs_cosechada.loc[sembrada_vs_cosechada['Municipio']==opcion_mun]
        
    fig = px.bar(sembrada_vs_cosechada, x='Año', y=['Superficie Siniestrada', 'Superficie Sembrada','Superficie Cosechada'], 
                labels={'Fecha': 'Fecha', 'value': 'Superficie (Hectarias)'}, barmode='group')

    fig.update_layout(xaxis_title='Año', yaxis_title='Superficie (Hectarias)', legend_title='Tipo de Superficie')
    fig.update_xaxes(tickmode='linear', tick0=sembrada_vs_cosechada['Año'].min(), dtick=1)  # Configuración para mostrar solo enteros en el eje x

    st.plotly_chart(fig)





st.divider()
st.markdown("<span style='font-size: 12px; color:#C0B9C9;'>By: Vesna Camile Pivac Alcaraz, Jose Carlos Barreras Maldonado y Luis Ernesto Ortiz Villalon</span>", unsafe_allow_html=True)

