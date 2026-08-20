
from app.services.excel_reader import ler_cta


arquivo = "/workspaces/sheet-compare/BASE CTA.xlsx"


with open(arquivo, "rb") as f:
    dados = f.read()


df = ler_cta(
    arquivo,
    dados,
)


print("\n===== RESULTADO =====")
print(df.head(20).to_string(index=False))


print("\n===== DIMENSÕES =====")
print(df.shape)


print("\n===== COLUNAS =====")
print(list(df.columns))

from app.services.excel_reader import ler_cta


arquivo = "/workspaces/sheet-compare/BASE CTA.xlsx"


with open(arquivo, "rb") as f:
    dados = f.read()


df = ler_cta(
    arquivo,
    dados,
)


print("\n===== RESULTADO =====")
print(df.head(20).to_string(index=False))


print("\n===== DIMENSÕES =====")
print(df.shape)


print("\n===== COLUNAS =====")
print(list(df.columns))
