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


valores = [
    "112.30",
    "88.90",
    "31.05",
    "35.00",
    "97.60",
]


for valor in valores:

    print("\n" + "=" * 70)
    print("PROCURANDO VALOR:", valor)

    # normaliza valores
    serie = (
        df["Valor"]
        .fillna("")
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )

    encontrados = df[serie == valor]

    print("Encontrados:", len(encontrados))

    if len(encontrados) > 0:

        colunas = [
            "No.Chamado",
            "eVoucher",
            "Cliente",
            "Valor",
            "Valor Corrida R$",
            "No.Registro",
            "Dt.Agenda",
        ]

        colunas = [
            c for c in colunas
            if c in df.columns
        ]

        print(
            encontrados[colunas]
            .head(20)
            .to_string(index=True)
        )


print("\nFinalizado.")

