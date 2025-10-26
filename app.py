import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.header('🚗 Análisis de Anuncios de Vehículos (TripleTen BOMCAM)')

# Leer los datos
car_data = pd.read_csv('vehicles_us.csv')

# Botón para histograma
if st.button('Mostrar histograma de odómetro'):
    st.write('Distribución del kilometraje (odómetro)')
    fig = go.Figure(data=[go.Histogram(x=car_data['odometer'])])
    fig.update_layout(title='Distribución del Odómetro')
    st.plotly_chart(fig, use_container_width=True)

# Botón para gráfico de dispersión
if st.button('Mostrar gráfico de dispersión'):
    st.write('Relación entre el año del modelo y el precio')
    fig2 = go.Figure(data=[go.Scatter(
        x=car_data['model_year'],
        y=car_data['price'],
        mode='markers'
    )])
    fig2.update_layout(title='Precio vs Año del Modelo')
    st.plotly_chart(fig2, use_container_width=True)
if st.button('Mostrar gráfico de barras de marcas'):
    st.write('Cantidad de vehículos por marca')
    brand_counts = car_data['brand'].value_counts().reset_index()
    brand_counts.columns = ['brand', 'count']
    fig3 = go.Figure(data=[go.Bar(
        x=brand_counts['brand'],
        y=brand_counts['count']
    )])
    fig3.update_layout(title='Cantidad de Vehículos por Marca')
    st.plotly_chart(fig3, use_container_width=True)
