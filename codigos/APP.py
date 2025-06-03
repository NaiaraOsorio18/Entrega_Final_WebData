import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# cores
rosa = '#FFC0CB'
rosa_escuro = '#FF69B4'
lilas = '#C8A2C8'
roxo = '#A569BD'

# Título 
st.markdown("<h1 style='text-align: center; color: #FF69B4;'>🍿🎬 Análise de Filmes - IMDb 🎥✨</h1>", unsafe_allow_html=True)

# Ler a base de dados
df = pd.read_csv('./bases_tratadas/dados_tratados_final.csv')

# Mostrar dados brutos
with st.expander('🔍 Visualizar dados brutos'):
    st.dataframe(df)

# Configurações do sidebar
st.sidebar.header('🎨 Configurações dos Gráficos')

colunas_num = ['Notas', 'Quantidade de Notas', 'Ano']

var_univariada = st.sidebar.selectbox('📈 Variável para análise univariada', colunas_num)
var_bivariada_x = st.sidebar.selectbox('🔸 Variável X para análise bivariada', colunas_num)
var_bivariada_y = st.sidebar.selectbox('🔹 Variável Y para análise bivariada', colunas_num)

# Tema dos gráficos
sns.set_style('whitegrid')
sns.set_palette([rosa_escuro, lilas, roxo, rosa])

# --- Gráficos Univariados ---
st.subheader(f'🌸 Distribuição de {var_univariada}')

fig1, ax1 = plt.subplots()
sns.histplot(df[var_univariada], bins=20, kde=True, ax=ax1, color=rosa_escuro)
ax1.set_facecolor('#fff0f5')
ax1.set_title(f'Distribuição de {var_univariada}', fontsize=14, color=roxo)
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
sns.boxplot(x=df[var_univariada], ax=ax2, color=lilas)
ax2.set_facecolor('#fff0f5')
ax2.set_title(f'Boxplot de {var_univariada}', fontsize=14, color=roxo)
st.pyplot(fig2)

# --- Gráficos Bivariados ---
st.subheader(f'💗 Relação entre {var_bivariada_x} e {var_bivariada_y}')

fig3, ax3 = plt.subplots()
sns.scatterplot(x=df[var_bivariada_x], y=df[var_bivariada_y], ax=ax3, color=rosa)
ax3.set_facecolor('#fff0f5')
ax3.set_title(f'Scatter plot: {var_bivariada_x} vs {var_bivariada_y}', fontsize=14, color=roxo)
st.pyplot(fig3)

st.subheader(f'💜 Distribuição de {var_bivariada_y} por Ano')

fig4, ax4 = plt.subplots()
sns.boxplot(x=df['Ano'].astype(str), y=df[var_bivariada_y], ax=ax4, color=rosa_escuro)
plt.xticks(rotation=45)
ax4.set_facecolor('#fff0f5')
ax4.set_title(f'Boxplot de {var_bivariada_y} por Ano', fontsize=14, color=roxo)
st.pyplot(fig4)

# --- Texto com medidas estatísticas ---
st.subheader('📌 Resumo Estatístico')

media = df[var_univariada].mean()
mediana = df[var_univariada].median()
std = df[var_univariada].std()

st.markdown(f"""
✨ **Média de {var_univariada}:** {media:.2f}  
✨ **Mediana de {var_univariada}:** {mediana:.2f}  
✨ **Desvio Padrão de {var_univariada}:** {std:.2f}  
""")

corr = df[[var_bivariada_x, var_bivariada_y]].corr().iloc[0,1]
st.markdown(f'💞 **Correlação entre {var_bivariada_x} e {var_bivariada_y}:** {corr:.2f}')

