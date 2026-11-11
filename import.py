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

df["actual_price"] = round(df["actual_price"], 2)
df["discounted_price"] = round(df["discounted_price"], 2)

df.head()
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
df_2 = df.dropna()

#%%

df_2["product_id"].duplicated().sum()

#%%

df_3 = df_2.drop_duplicates("product_id")

#%%

df_3

#%%

df_3["category_1"] = df_3["category"].str.split("|").str[0]
df_3["category_2"] = df_3["category"].str.split("|").str[1]

#%%
df_4 = (df_3.groupby("category_2")
           .agg(qtd_produtos=("product_id", "count"),
                total_avaliacoes=("rating_count", "sum"),
                nota_media=("rating", "mean"))
           .sort_values("total_avaliacoes", ascending=False))

df_4["pct_total"] = df_4["total_avaliacoes"] / df_4["total_avaliacoes"].sum()

#%%

df_4 = df_4.reset_index()


df_5 = df_4.head(8)

#%%

df_5.to_excel("data/amazon_q1.xlsx", index=False)



#%%

df_prod = (df_3[["product_id", "product_name", "category_2", "rating", "rating_count"]]
           .sort_values("rating_count", ascending=False)
           .reset_index(drop=True))

df_prod["pct_total"] = df_prod["rating_count"] / df_prod["rating_count"].sum()

df_prod.head(10)

#%%

df_prod.head(10).to_excel("data/amazon_q1_prod.xlsx", index=False)
