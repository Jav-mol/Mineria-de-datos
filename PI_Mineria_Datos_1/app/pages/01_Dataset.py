"""
01_Dataset.py — Vista previa, calidad y transformaciones del dataset
"""

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dataset", page_icon="📋", layout="wide")
st.title("📋 Dataset")

# ── Cargar datos ──
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROCESSED = os.path.join(BASE_DIR, "data", "processed", "reporte_clinica_analisis.csv")
RAW = os.path.join(BASE_DIR, "data", "raw", "reporte_clinica_original.csv")

@st.cache_data
def load_data():
    df_proc = pd.read_csv(PROCESSED)
    df_raw = pd.read_csv(RAW)
    return df_raw, df_proc

df_raw, df = load_data()

# ── Descripción general ──
st.markdown("## 📊 Descripción general")
st.markdown(f"""
El dataset contiene **{df.shape[0]:,} registros** de asegurados con **{df.shape[1]} variables**:

| Columna | Tipo | Descripción |
|---|---|---|
| `age` | Numérica | Edad del asegurado (18–64 años) |
| `sex` | Categórica | Sexo: `female` / `male` |
| `bmi` | Numérica | Índice de Masa Corporal |
| `children` | Numérica | Número de hijos dependientes |
| `smoker` | Categórica | Fumador: `yes` / `no` |
| `region` | Categórica | Región geográfica (4 regiones) |
| `charges` | Numérica | Costo del seguro (USD) |
""")

# ── Vista previa ──
st.markdown("## 🔍 Vista previa del dataset")
st.dataframe(df.head(10), use_container_width=True)

# ── Resumen de calidad ──
st.markdown("## 🧹 Resumen de calidad y limpieza")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Dataset original")
    st.metric("Filas", f"{df_raw.shape[0]:,}")
    st.metric("Columnas", df_raw.shape[1] - 1)  # sin Unnamed: 0
    st.metric("Valores nulos", f"{df_raw.isnull().sum().sum():,}")

with col2:
    st.markdown("### Dataset procesado")
    st.metric("Filas", f"{df.shape[0]:,}")
    st.metric("Columnas", df.shape[1])
    st.metric("Valores nulos", f"{df.isnull().sum().sum():,}")

st.markdown("---")

st.markdown("### Transformaciones aplicadas")

with st.expander("Ver detalle de transformaciones"):
    st.markdown("""
    | # | Transformación | Impacto |
    |---|---|---|
    | 1 | Eliminar columna índice sobrante | 8 → 7 columnas |
    | 2 | Estandarizar `sex` a minúsculas | 4 → 2 categorías |
    | 3 | Estandarizar `smoker` a minúsculas | 4 → 2 categorías |
    | 4 | Estandarizar `region`: siglas → nombres | 8 → 4 categorías |
    | 5 | Convertir outliers `bmi` (≤0, ≥100) a NaN | +20 nulos |
    | 6 | Convertir outliers `children` (<0, >10) a NaN | +10 nulos |
    | 7 | Imputar `age` con mediana | 102 nulos → 0 |
    | 8 | Imputar `bmi` con mediana | 70 nulos → 0 |
    | 9 | Imputar `children` con mediana | 10 nulos → 0 |
    """)

st.markdown("### Distribución de variables categóricas")
cat_cols = ['sex', 'smoker', 'region']
col1, col2, col3 = st.columns(3)
for i, (col_name, c) in enumerate(zip(cat_cols, [col1, col2, col3])):
    with c:
        st.markdown(f"**{col_name}**")
        st.dataframe(df[col_name].value_counts().reset_index(), hide_index=True)
