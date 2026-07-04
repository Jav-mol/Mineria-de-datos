"""
Home.py — Página principal de la app Streamlit
Proyecto Integrador: Minería de Datos I
"""

import streamlit as st

st.set_page_config(page_title="Proyecto Integrador", page_icon="📊", layout="wide")

st.title("📊 Proyecto Integrador — Minería de Datos I")
st.subheader("Análisis de Factores de Costo en Seguros Médicos")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👥 Integrantes")
    st.markdown("- **Javier Molina**")
    st.markdown("- **Federico Claramunt**")

    st.markdown("### 📋 Información del curso")
    st.markdown("- **Materia:** Minería de Datos I — Mañana")
    st.markdown("- **Módulo:** 3 — Modelar y Comunicar")
    st.markdown("- **Fecha de entrega:** 4 de julio de 2026")

with col2:
    st.markdown("### 🔗 Enlaces")
    st.markdown("**Repositorio GitHub:**")
    st.markdown("[github.com/Jav-mol/Mineria-de-datos](https://github.com/Jav-mol/Mineria-de-datos)")
    st.markdown("**App Streamlit Cloud:** [mineria-de-datos.streamlit.app](https://mineria-de-datos.streamlit.app/)")

st.markdown("---")

st.markdown("### 🎯 Contexto")

st.markdown("""
Este proyecto analiza un dataset de **1,363 asegurados** de salud con el objetivo de 
identificar los principales factores que influyen en el costo del seguro médico. 

A través de técnicas de **análisis exploratorio de datos (EDA)**, **reducción de 
dimensionalidad (PCA)** y **visualización interactiva**, se busca comprender qué 
variables tienen mayor impacto en los costos y comunicar estos hallazgos de manera 
clara y accesible.

El dataset contiene información sobre **edad, sexo, IMC, número de hijos, condición 
de fumador, región geográfica y costo del seguro** de cada asegurado.
""")

st.markdown("---")

st.markdown("### 📁 Estructura del proyecto")

st.markdown("""
| Carpeta/Archivo | Descripción |
|---|---|
| `data/raw/` | Dataset original sin modificaciones |
| `data/processed/` | Dataset limpio y preparado para análisis |
| `notebooks/` | Desarrollo completo del proyecto (5 notebooks) |
| `app/` | Aplicación interactiva Streamlit |
| `reports/` | Informe final en PDF |
| `logs/` | Registro de transformaciones ETL |
| `README.md` | Documentación técnica del proyecto |
""")

st.markdown("---")

st.info("👈 **Navegá por las páginas de la izquierda** para explorar el dataset, los análisis y las conclusiones.")
