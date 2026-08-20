from app.services.excel_reader import ler_vale_troca


arquivo = "/workspaces/sheet-compare/18-08-2026 - troca.xls"


with open(arquivo, "rb") as f:
    dados = f.read()


df = ler_vale_troca(
    arquivo,
    dados,
)


print("\n===== RESULTADO =====")
print(df.head(20).to_string(index=False))


print("\n===== DIMENSÕES =====")
print(df.shape)


print("\n===== COLUNAS =====")
print(list(df.columns))
