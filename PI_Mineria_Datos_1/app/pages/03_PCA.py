"""
03_PCA.py — Reducción de dimensionalidad: varianza explicada y loadings
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

st.set_page_config(page_title="PCA", page_icon="🔬", layout="wide")
st.title("🔬 Reducción de Dimensionalidad (PCA)")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROCESSED = os.path.join(BASE_DIR, "data", "processed", "reporte_clinica_analisis.csv")

@st.cache_data
def load():
    return pd.read_csv(PROCESSED)

df = load()

# ── Preparar variables ──
df_pca = df.copy()
df_pca['smoker_num'] = df_pca['smoker'].map({'yes': 1, 'no': 0})
df_pca['sex_num'] = df_pca['sex'].map({'male': 1, 'female': 0})
region_dummies = pd.get_dummies(df_pca['region'], prefix='region', drop_first=True)
df_pca = pd.concat([df_pca, region_dummies], axis=1)

feature_cols = ['age', 'bmi', 'children', 'charges', 'smoker_num', 'sex_num',
                'region_northwest', 'region_southeast', 'region_southwest']
X = df_pca[feature_cols]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA()
X_pca = pca.fit_transform(X_scaled)

var_ratio = pca.explained_variance_ratio_
var_cumsum = np.cumsum(var_ratio)

# ── Variables y escalamiento ──
st.markdown("## 📐 Variables utilizadas y escalamiento")

st.markdown(f"""
Se aplicó PCA sobre **{len(feature_cols)} variables** numéricas:

| # | Variable | Tipo |
|---|---|---|
| 1 | `age` | Numérica (edad) |
| 2 | `bmi` | Numérica (IMC) |
| 3 | `children` | Numérica (hijos) |
| 4 | `charges` | Numérica (costo) |
| 5 | `smoker` | Codificada (yes=1, no=0) |
| 6 | `sex` | Codificada (male=1, female=0) |
| 7-9 | `region` | One-hot (3 columnas, 4 regiones) |

**Escalamiento:** `StandardScaler` (media = 0, desviación estándar = 1) para evitar que `charges` domine por su magnitud.
""")

# ── Visualización 1: Varianza explicada ──
st.markdown("---")
st.markdown("## 📊 Visualización 1: Varianza Explicada por Componente")

fig, ax1 = plt.subplots(figsize=(12, 6))

avg_var = 1 / len(feature_cols)
colors = ['steelblue' if vr > avg_var else 'lightgray' for vr in var_ratio]
bars = ax1.bar(range(1, len(var_ratio)+1), var_ratio, color=colors, edgecolor='black')
ax1.axhline(y=avg_var, color='red', linestyle='--', linewidth=1.5,
            label=f'Varianza promedio ({avg_var:.1%})')

ax2 = ax1.twinx()
ax2.plot(range(1, len(var_cumsum)+1), var_cumsum, 'o-', color='darkorange', linewidth=2, label='Acumulada')
ax2.axhline(y=0.80, color='green', linestyle=':', linewidth=1.5, label='80%')
ax2.axhline(y=0.90, color='green', linestyle='--', linewidth=1.5, label='90%')

ax1.set_xlabel('Componente Principal')
ax1.set_ylabel('Varianza Explicada (individual)')
ax2.set_ylabel('Varianza Explicada (acumulada)')
ax1.set_title('Varianza Explicada por Componente Principal')

for bar, vr in zip(bars, var_ratio):
    if vr > 0.03:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{vr:.1%}', ha='center', fontsize=8, fontweight='bold')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center')

st.pyplot(fig)

# ── Tabla de varianza ──
st.markdown("### Varianza explicada por componente")
var_df = pd.DataFrame({
    'Componente': [f'PC{i+1}' for i in range(len(var_ratio))],
    'Varianza individual': [f'{v:.2%}' for v in var_ratio],
    'Varianza acumulada': [f'{v:.2%}' for v in var_cumsum],
})
st.dataframe(var_df.head(9), use_container_width=True, hide_index=True)

n80 = np.argmax(var_cumsum >= 0.80) + 1
n90 = np.argmax(var_cumsum >= 0.90) + 1
st.markdown(f"""
**Interpretación:** PC1 concentra la mayor proporción de varianza.  
Se necesitan **{n80} componentes** para alcanzar el 80% de varianza acumulada 
y **{n90} componentes** para el 90%. Las barras grises muestran componentes que 
aportan menos que una variable original (por debajo de la línea roja).
""")

# ── Visualización 2: Loadings ──
st.markdown("---")
st.markdown("## 📊 Visualización 2: Contribución de Variables (Loadings)")

loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i+1}' for i in range(len(feature_cols))],
    index=feature_cols
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(loadings[['PC1', 'PC2']], annot=True, fmt='.3f', cmap='RdBu_r', center=0,
            vmin=-1, vmax=1, linewidths=0.5, cbar_kws={'label': 'Loading'}, ax=ax)
ax.set_title('Contribución de Variables a PC1 y PC2 (Loadings)')
st.pyplot(fig)

# Top variables
pc1_top = loadings['PC1'].abs().sort_values(ascending=False).head(3)
pc2_top = loadings['PC2'].abs().sort_values(ascending=False).head(3)
st.markdown(f"""
**Interpretación:**  

- **PC1 (eje de costo/riesgo):** dominada por `{pc1_top.index[0]}` ({loadings.loc[pc1_top.index[0], 'PC1']:+.3f}),  
  `{pc1_top.index[1]}` ({loadings.loc[pc1_top.index[1], 'PC1']:+.3f}) y  
  `{pc1_top.index[2]}` ({loadings.loc[pc1_top.index[2], 'PC1']:+.3f}).  
  Esta componente separa asegurados según su nivel de riesgo/costo.

- **PC2 (eje demográfico):** dominada por  
  `{pc2_top.index[0]}` ({loadings.loc[pc2_top.index[0], 'PC2']:+.3f}),  
  `{pc2_top.index[1]}` ({loadings.loc[pc2_top.index[1], 'PC2']:+.3f}) y  
  `{pc2_top.index[2]}` ({loadings.loc[pc2_top.index[2], 'PC2']:+.3f}).  
  Captura variabilidad demográfica y de composición corporal.

El PCA **confirma los hallazgos del EDA**: tabaquismo y edad son los factores 
que más contribuyen a la variabilidad en los costos de seguro.
""")
