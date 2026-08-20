import pandas as pd

arquivo = input("Digite o caminho do arquivo VALE - TROCA: ")

df = pd.read_excel(arquivo, header=None)

print("\n===== DIMENSÕES =====")
print(df.shape)

print("\n===== PRIMEIRAS 40 LINHAS =====")
print(df.head(40).to_string())

print("\n===== TIPOS =====")
print(df.dtypes)
