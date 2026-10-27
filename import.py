#%%
import pandas as pd
import yfinance as yf
import os

#%%

file_name = "data/amazon.csv"

if not os.path.exists(file_name):
    print(f"Arquivo não encontrado: {file_name}")
    df = None
else:
    print(f"Arquivo encontrado: {file_name}")
    df = pd.read_csv(file_name)

if df is not None:
    print(df.head())

#%%
## normalizando valor de rubris em reais

ticker = yf.Ticker("INRBRL=X")

cotacao_inr_brl = ticker.history(period="1d")["Close"].iloc[-1]
print(f"Cotação da Rupia hoje (via Yahoo Finance): R$ {cotacao_inr_brl:.4f}")

colunas_preco = ["actual_price", "discounted_price"]

for col in colunas_preco:
    df[col] = df[col].astype(str).str.replace("₹", "", regex=False).str.replace(",", "", regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')

df[colunas_preco] = df[colunas_preco] * cotacao_inr_brl

print("\nPreços convertidos para Real (R$):")
print(df[colunas_preco].head())

#%%
#normalizando a coluna porcentagem, deixando como valor númerico

df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
)
df["discount_percentage"] = pd.to_numeric(df["discount_percentage"], errors="coerce") / 100

#%%

df.head()

#%%

df["rating_count"] = df["rating_count"].str.replace(',','')
#%%

df.info()

#%%

df["rating"] = pd.to_numeric(df["rating"], errors='coerce')
df["rating_count"] = pd.to_numeric(df["rating_count"], errors='coerce')

#%%

df.isna().sum()


#%% 

df_2 = df.dropna()

#%%

df_2.isna().sum()

df_2.duplicated().sum()


#%%

df_2.to_csv(path_or_buf="C:/Users/vitor/amazon_tech_challenge/data")
