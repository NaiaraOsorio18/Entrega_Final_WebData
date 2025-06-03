from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.by import By
import re

def tratar_quantidade_nota(valor):
    if pd.isna(valor):
        return None
    valor = valor.strip().replace('(', '').replace(')', '').replace('"', '').strip()
    match = re.match(r'([\d.,]+)\s*(mi|mil)', valor)
    if match:
        numero = match.group(1).replace(',', '.')
        unidade = match.group(2)
        if unidade == 'mi':
            return int(float(numero) * 1_000_000)
        elif unidade == 'mil':
            return int(float(numero) * 1_000)
    return None

# Configura o serviço do Chrome
servico = Service(ChromeDriverManager().install())

# Abre o navegador
navegador = webdriver.Chrome(service=servico)

# Acessa a página
navegador.get("https://www.imdb.com/chart/top/")
navegador.maximize_window()

lista_nomes = []
lista_notas = []
lista_anos = []
lista_qtde_notas = []

for i in range(1, 31):
    try:
        nome = navegador.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/div[1]/a/h3').text
        nota = navegador.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/span/div/span/span[1]').text
        ano = navegador.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/div[2]/span[1]').text
        qtde_notas = navegador.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div/div/div/div/div[2]/span/div/span/span[2]').text

        lista_nomes.append(nome)
        lista_notas.append(nota)
        lista_anos.append(ano)
        lista_qtde_notas.append(qtde_notas)
    except:
        pass

navegador.quit()

# Criar DataFrame
df = pd.DataFrame({
    'Título': lista_nomes,
    'Notas': lista_notas,
    'Quantidade de Notas': lista_qtde_notas,
    'Ano': lista_anos
})

df.to_csv('../bases_originais/bases_originais.csv', index=False)

# Limpar o título (remover "1. ", "2. ", etc do início)
df['Título'] = df['Título'].str.replace(r'^\d+\.\s*', '', regex=True)

# Limpar a coluna 'Quantidade de Notas' para tirar espaços e aspas
df['Quantidade de Notas'] = df['Quantidade de Notas'].str.strip().str.replace('"', '').str.replace("'", "")

# Aplicar a função para transformar em número inteiro
df['Quantidade de Notas'] = df['Quantidade de Notas'].apply(tratar_quantidade_nota)

# Converter Notas para float, trocando vírgula por ponto
df['Notas'] = df['Notas'].str.replace(',', '.').astype(float)

# Extrair ano e converter para inteiro
df['Ano'] = df['Ano'].str.extract(r'(\d{4})').astype(int)

print(df.head())
print('fim')

# Salvar em CSV
df.to_csv('../bases_tratadas/dados_tratados.csv', index=False)

# --- depois do dataframe estar com as colunas limpas e convertidas ---

# Tratar valores nulos
df['Notas'] = df['Notas'].fillna(0)
df['Título'] = df['Título'].fillna('missing')

# Tratar outliers no Ano (exemplo: limitar a 1992)
df.loc[df['Ano'] > 2010, 'Ano'] = 2010

# Remover duplicatas
df = df.drop_duplicates()

# Salvar novamente o arquivo tratado final
df.to_csv('../bases_tratadas/dados_tratados_final.csv', index=False)

print("Tratamentos finais aplicados:")
print(df.info())
print(df.head())
