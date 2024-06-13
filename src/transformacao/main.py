import pandas as pd
import sqlite3
from datetime import datetime

# Leitura do arquivo JSONL
df = pd.read_json('../data/data.jsonl', lines=True)

# Mostrar todas as colunas
pd.options.display.max_columns = None

# Adicionar coluna _source com um valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/tenis-de-corrida-feminino"

# Adicionar coluna _data_coleta com a data e hora atuais
df['_data_coleta'] = datetime.now()

 
# Tratar valores null para colunas númericas 
numerical_columns = ['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos', 'reviews_rating_number']
for col in numerical_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)

# Remover parênteses das colunas 'reviews_amount'
df['reviews_amount'] = df['reviews_amount'].str.replace(r'[\(\)]', '', regex=True)
df['reviews_amount'] = pd.to_numeric(df['reviews_amount'], errors='coerce').fillna(0).astype(int)

# Tratar preços tipo float e calcular valores totais
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remover as colunas antigas de preços
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('data/quotes.db')

# Salvar DataFrame no banco
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fechar conexão do bd
conn.close()

print(df.head())

