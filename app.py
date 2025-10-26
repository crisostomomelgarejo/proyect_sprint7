# ===============================================
#   Proyecto Sprint 7 - Aplicación Streamlit
#   Autor: Crisóstomo Melgarejo
#   Descripción: Análisis interactivo de anuncios de vehículos
# ===============================================

# ==== Importación de librerías ====
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


# ==== Lectura y preparación de los datos ====
df = pd.read_csv('vehicles_us.csv')

# Limpieza y normalización de texto en la columna 'model'
df['model'] = df['model'].astype(str).str.strip()

# División de 'model' en dos columnas: 'brand' y 'model_name'
split = df['model'].str.split(' ', n=1, expand=True)
df['brand'] = split[0].str.capitalize().str.strip()
df['model_name'] = split[1].str.lower().str.strip().fillna('')

# Normalizar la columna 'model' (solo primera palabra)
df['model'] = df['model'].str.split().str[0].str.capitalize()

# ==== Limpieza general del DataFrame ====
df_clean = df.copy()

# Eliminar filas con valores faltantes críticos
df_clean.dropna(subset=['model_year', 'cylinders', 'odometer'], inplace=True)

# Convertir a tipo entero
df_clean['model_year'] = df_clean['model_year'].astype(int)
df_clean['cylinders'] = df_clean['cylinders'].astype(int)
df_clean['odometer'] = df_clean['odometer'].astype(int)

# Rellenar valores faltantes en otras columnas
df_clean['paint_color'] = df_clean['paint_color'].fillna('unknown')
df_clean['is_4wd'] = df_clean['is_4wd'].fillna(0).astype(int)


# ==== Configuración de la aplicación Streamlit ====
st.header('🚗 Análisis de Anuncios de Vehículos (Sprint 7)')
st.subheader('by Crisóstomo Melgarejo')

# Mostrar DataFrame limpio
st.subheader('Datos Limpios')
st.dataframe(df_clean, use_container_width=True)


# ==== Gráfico Sunburst ====
st.subheader('Gráfico Sunburst de Vehículos por Marca y Modelo')
if st.button('Mostrar gráfico Sunburst'):
    fig_sun = px.sunburst(
        df_clean,
        path=['brand', 'model_name'],
        values=None,  # Cuenta ocurrencias automáticamente
        title='Conteo de Vehículos por Marca y Modelo',
        color='brand'
    )
    fig_sun.update_traces(textinfo='label+percent entry')
    st.plotly_chart(fig_sun, use_container_width=True)


# ==== Histograma: Condición vs Año del Modelo ====
st.subheader('Gráfico de Histograma de Vehículos por Condición y Año del Modelo')
if st.button('Mostrar histograma de condición vs Año del Modelo'):
    fig_hist = px.histogram(
        df_clean,
        x='model_year',
        color='condition',
        title='Histograma de Condición vs Año del Modelo',
        barmode='stack',
        labels={
            'model_year': 'Año del Modelo',
            'condition': 'Condición',
            'count': 'Cantidad'
        }
    )
    st.plotly_chart(fig_hist, use_container_width=True)


# ==== Gráfico de Dispersión: Precio vs Año del Modelo ====
st.subheader('Gráfico de Dispersión: Precio vs Año del Modelo')
if st.button('Mostrar gráfico de dispersión'):
    fig_scatter = go.Figure(
        data=[
            go.Scatter(
                x=df_clean['model_year'],
                y=df_clean['price'],
                mode='markers',
                marker=dict(
                    size=6,
                    opacity=0.6,
                    color=df_clean['model_year'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(
                        title='Año del Modelo',  # Título de la escala de color
                        titleside='right'
                    )
                )
            )
        ]
    )

    # Configurar diseño del gráfico
    fig_scatter.update_layout(
        title='Precio vs. Año del Modelo',
        xaxis_title='Año del Modelo',
        yaxis_title='Precio (USD)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_x=0.5  # Centrar título
    )

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig_scatter, use_container_width=True)


# ==== Gráfico de Barras Apiladas: Tipos de Vehículos por Modelo ====
st.subheader('Gráfico de Barras Apiladas de Tipos de Vehículos por Modelo')
if st.button('Mostrar gráficos por fabricante'):
    fig_bar = px.bar(
        df_clean,
        x='model',
        color='type',
        title='Tipos de Vehículos por Modelo',
        labels={
            'model': 'Modelo',
            'type': 'Tipo',
            'count': 'Unidades'
        }
    )

    # Ajustes visuales y orden descendente
    fig_bar.update_layout(
        barmode='stack',
        xaxis={'categoryorder': 'total descending'},
        title_x=0.5
    )

    st.plotly_chart(fig_bar, use_container_width=True)
