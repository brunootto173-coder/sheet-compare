import pandas as pd

arquivo = "/workspaces/sheet-compare/BASE CTA.xlsx"

print("Lendo BASE CTA...")
df = pd.read_excel(
    arquivo,
    sheet_name="Geral",
    header=2,
    dtype=str,
)

print("BASE carregada.")
print("Dimensão:", df.shape)

# Valores que vimos na planilha VALE - TROCA
valores_teste = [
    "41027193",
    "5558524",
    "41118645",
    "5562900",
    "41132706",
    "5563509",
]

print("\n===== PROCURANDO VALORES =====\n")

for valor in valores_teste:

    print(f"\nValor procurado: {valor}")

    encontrou = False

    for coluna in df.columns:

        serie = df[coluna].fillna("").astype(str).str.strip()

        resultado = df[serie == valor]

        if not resultado.empty:

            encontrou = True

            print(
                f"ENCONTRADO na coluna: {coluna}"
            )

            print(
                resultado[
                    [coluna]
                ].head(3).to_string(index=False)
            )

    if not encontrou:
        print("Não encontrado.")

print("\nFinalizado.")

