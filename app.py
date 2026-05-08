# ===============================================
#   Proyecto  Aplicación Streamlit
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


# Normalizar columna 'condition' a minúsculas
if 'condition' in df_clean.columns:
    df_clean['condition'] = (df_clean['condition'].astype(str)
                             .str.lower().str.strip()
                             .replace({'nan': 'unknown'}))
else:
    df_clean['condition'] = 'unknown'

# Limpiar todas las columnas de texto: eliminar espacios vacios de los extremos,
# capitalizar cada palabra y cambiar espacios por '_'
cols_texto = df_clean.select_dtypes(include=['object', 'category']).columns
for col in cols_texto:
    if col != 'date_posted':
        df_clean[col] = df_clean[col].astype(str).str.strip().str.title().str.replace(' ', '_')



# ==== Configuración de la aplicación Streamlit ====
st.header('🚗 Análisis de Anuncios de Vehículos')
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
                customdata=df_clean[['brand', 'model_name']].values,
                marker=dict(
                    size=8,
                    opacity=0.7,
                    color=df_clean['odometer'],
                    colorscale='Sunset',
                    line=dict(width=0.5, color='white'),
                    showscale=True,
                    colorbar=dict(
                        title=dict(
                            text='<b>Millaje (Millas)</b>',
                            font=dict(size=12, color='#555555')
                        ),
                        thickness=12,
                        len=0.75,
                        outlinewidth=0,
                        tickfont=dict(color='#7F8C8D'),
                        tickformat=',.0f'
                    )
                ),
                hovertemplate=(
                    '<b>Marca:</b> %{customdata[0]}<br>'
                    '<b>Modelo:</b> %{customdata[1]}<br>'
                    '<b>Odómetro:</b> %{marker.color:,.0f} millas<br>'
                    '<b>Año:</b> %{x}<br>'
                    '<b>Precio:</b> $%{y:,.0f}<br>'
                    '<extra></extra>'
                )
            )
        ]
    )

    fig_scatter.update_layout(
        title=dict(
            text='Relación entre <b>Precio</b>, <b>Año</b> y <b>Millaje</b>',
            font=dict(size=22, color='#2C3E50', family='Arial, sans-serif'),
            x=0.05,
            y=0.95
        ),
        xaxis=dict(
            title='Año de Fabricación',
            showgrid=True,
            gridcolor='#F0F4F8',
            linecolor='#D5DDE5',
            zeroline=False,
            tickfont=dict(color='#7F8C8D')
        ),
        yaxis=dict(
            title='Precio (USD)',
            showgrid=True,
            gridcolor='#F0F4F8',
            linecolor='#D5DDE5',
            zeroline=False,
            tickformat='$,.0f',
            tickfont=dict(color='#7F8C8D')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=40, t=80, b=60),
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Arial, sans-serif'
        )
    )
    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig_scatter, use_container_width=True)


# ==== Gráfico de Barras Apiladas: Tipos de Vehículos por Modelo ====
st.subheader('Gráfico de Barras Apiladas de Tipos de Vehículos por Modelo')
if st.button('Mostrar gráficos por fabricante'):
    fig_bar = px.histogram(
        df_clean,
        x='model',
        color='type',
        title='Tipos de Vehículos por Modelo',
        labels={
            'model': 'Modelo',
            'type': 'Tipo'
        }
    )

    # Ajustes visuales y orden descendente
    fig_bar.update_layout(
        barmode='stack',
        xaxis={'categoryorder': 'total descending'},
        title_x=0.5,
        yaxis_title="Unidades"
    )

    st.plotly_chart(fig_bar, use_container_width=True)
