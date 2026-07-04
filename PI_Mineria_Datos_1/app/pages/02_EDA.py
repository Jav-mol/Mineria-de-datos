"""
02_EDA.py — Análisis Exploratorio: 2 univariadas + 2 bivariadas + 1 multivariada
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="EDA", page_icon="📈", layout="wide")
st.title("📈 Análisis Exploratorio de Datos (EDA)")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROCESSED = os.path.join(BASE_DIR, "data", "processed", "reporte_clinica_analisis.csv")

@st.cache_data
def load():
    return pd.read_csv(PROCESSED)

df = load()

# ── Univariada 1: Distribución de charges ──
st.markdown("---")
st.markdown("### 1. Univariada: Distribución de Costos de Seguro")
st.markdown("**Pregunta:** ¿Cómo se distribuyen los costos del seguro médico?")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df['charges'], kde=True, bins=40, color='steelblue', edgecolor='white', ax=ax1)
ax1.axvline(df['charges'].median(), color='red', linestyle='--', linewidth=2, label=f'Mediana: ${df["charges"].median():,.0f}')
ax1.axvline(df['charges'].mean(), color='orange', linestyle='--', linewidth=2, label=f'Media: ${df["charges"].mean():,.0f}')
ax1.set_title('Histograma de Costos')
ax1.set_xlabel('Costo (USD)')
ax1.legend()

sns.boxplot(x=df['charges'], color='lightblue', ax=ax2)
ax2.set_title('Boxplot de Costos')
ax2.set_xlabel('Costo (USD)')
st.pyplot(fig)

st.markdown(f"""
**Interpretación:** La distribución de costos muestra una clara **asimetría positiva (skew = {df['charges'].skew():.2f})**. 
La mayoría de los asegurados paga entre $2,000 y $15,000, pero existe un grupo reducido con costos muy elevados. 
La media (${df['charges'].mean():,.0f}) es significativamente mayor que la mediana (${df['charges'].median():,.0f}), 
lo cual indica que un subconjunto pequeño de la población impulsa el costo promedio hacia arriba.
""")

# ── Univariada 2: Distribución por edad ──
st.markdown("---")
st.markdown("### 2. Univariada: Distribución por Grupo Etario")
st.markdown("**Pregunta:** ¿Qué grupo etario está más representado en el dataset?")

bins = [0, 25, 35, 45, 55, 100]
labels = ['18-25', '26-35', '36-45', '46-55', '56-64']
df_plot = df.copy()
df_plot['age_group'] = pd.cut(df_plot['age'], bins=bins, labels=labels, right=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df['age'], bins=20, kde=True, color='teal', edgecolor='white', ax=ax1)
ax1.set_title('Distribución de Edad')
ax1.set_xlabel('Edad')

age_counts = df_plot['age_group'].value_counts().sort_index()
colors = sns.color_palette('Blues_d', len(age_counts))
ax2.bar(age_counts.index.astype(str), age_counts.values, color=colors, edgecolor='black')
ax2.set_title('Por Grupo Etario')
ax2.set_xlabel('Grupo Etario')
ax2.tick_params(axis='x', rotation=45)
for j, v in enumerate(age_counts.values):
    ax2.text(j, v + 2, str(v), ha='center', fontsize=9)
st.pyplot(fig)

st.markdown("""
**Interpretación:** La distribución de edades es relativamente uniforme entre los 18 y 64 años, 
con una ligera mayor concentración en el rango 18-25. No hay un sesgo etario marcado, lo cual 
sugiere que el dataset captura una muestra diversa en términos de edad.
""")

# ── Bivariada 1: Smoker vs Charges ──
st.markdown("---")
st.markdown("### 3. Bivariada: Costos según Condición de Fumador")
st.markdown("**Pregunta:** ¿Existen diferencias significativas en los costos entre fumadores y no fumadores?")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(x='smoker', y='charges', data=df, palette={'yes': 'coral', 'no': 'lightgreen'}, ax=ax1)
ax1.set_title('Boxplot: Costos por Fumador')
ax1.set_xlabel('Fumador'); ax1.set_ylabel('Costo (USD)')

sns.violinplot(x='smoker', y='charges', data=df, palette={'yes': 'coral', 'no': 'lightgreen'}, ax=ax2)
ax2.set_title('Violin: Distribución por Fumador')
ax2.set_xlabel('Fumador'); ax2.set_ylabel('Costo (USD)')
st.pyplot(fig)

smoker_means = df.groupby('smoker')['charges'].mean()
ratio = smoker_means['yes'] / smoker_means['no']
st.markdown(f"""
**Interpretación:** La diferencia entre fumadores y no fumadores es **drástica y concluyente**. 
Los fumadores pagan en promedio **{ratio:.1f} veces más** que los no fumadores. 
Además, la dispersión de costos en fumadores es mucho mayor, lo cual indica que dentro del grupo 
de fumadores hay también variabilidad significativa. El tabaquismo es el factor individual con 
mayor impacto en el costo del seguro.
""")

# ── Bivariada 2: Age vs Charges ──
st.markdown("---")
st.markdown("### 4. Bivariada: Relación Edad vs Costo")
st.markdown("**Pregunta:** ¿Cómo se relaciona la edad con el costo del seguro?")

fig, ax = plt.subplots(figsize=(12, 6))
for smoker, color in [('yes', 'coral'), ('no', 'steelblue')]:
    subset = df[df['smoker'] == smoker]
    ax.scatter(subset['age'], subset['charges'], alpha=0.6, s=50, c=color, label=smoker, edgecolor='white')
    z = np.polyfit(subset['age'], subset['charges'], 1)
    p = np.poly1d(z)
    x_r = np.linspace(subset['age'].min(), subset['age'].max(), 100)
    ax.plot(x_r, p(x_r), color='darkred' if smoker == 'yes' else 'darkblue', linewidth=2, linestyle='--')

ax.set_title('Relación Edad vs Costo de Seguro')
ax.set_xlabel('Edad'); ax.set_ylabel('Costo (USD)')
ax.legend()
st.pyplot(fig)

age_corr = df['age'].corr(df['charges'])
st.markdown(f"""
**Interpretación:** La edad muestra una **correlación positiva moderada** con los costos (r = {age_corr:.3f}). 
Sin embargo, lo más revelador es la interacción con el tabaquismo: la pendiente de la tendencia 
para fumadores es mucho más pronunciada. Esto significa que **el efecto de la edad sobre el costo 
se amplifica en fumadores**.
""")

# ── Multivariada: Matriz de correlación ──
st.markdown("---")
st.markdown("### 5. Multivariada: Matriz de Correlación")
st.markdown("**Pregunta:** ¿Qué combinación de factores explica mejor la variabilidad en los costos?")

df_enc = df.copy()
df_enc['smoker_num'] = df_enc['smoker'].map({'yes': 1, 'no': 0})
df_enc['sex_num'] = df_enc['sex'].map({'male': 1, 'female': 0})
region_dummies = pd.get_dummies(df_enc['region'], prefix='region', drop_first=True)
df_enc = pd.concat([df_enc, region_dummies], axis=1)

cols_corr = ['age', 'bmi', 'children', 'charges', 'smoker_num', 'sex_num',
             'region_northwest', 'region_southeast', 'region_southwest']
corr = df_enc[cols_corr].corr()

fig, ax = plt.subplots(figsize=(11, 9))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            mask=mask, square=True, linewidths=0.5, ax=ax)
ax.set_title('Matriz de Correlación entre Variables')
st.pyplot(fig)

st.markdown("""
**Interpretación:** La matriz de correlación revela que:
- **`smoker`** es el factor dominante (corr ≈ 0.79 con charges)
- **`age`** es el segundo factor más importante (corr ≈ 0.30)
- **`bmi`** tiene correlación baja pero positiva
- **`children`, `sex` y `region`** tienen correlaciones ≈ 0 con charges

Esto confirma que el tabaquismo y la edad son los principales determinantes del costo del seguro.
""")
