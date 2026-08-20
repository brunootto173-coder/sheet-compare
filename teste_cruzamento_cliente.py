import pandas as pd


ARQUIVO_CTA = "/workspaces/sheet-compare/BASE CTA.xlsx"


print("Lendo BASE CTA...")

df = pd.read_excel(
    ARQUIVO_CTA,
    sheet_name="Geral",
    header=2,
    dtype=str,
)

print("BASE carregada.")
print("Dimensão:", df.shape)


# ==========================================
# VALORES DA PLANILHA VALE
# ==========================================

testes = [
    {
        "qru": "41027193",
        "numero": "5558524",
        "cliente": "80000-GOVERNO DO ESTADO DO PARANA",
        "valor": "112.30",
    },
    {
        "qru": "41118645",
        "numero": "5562900",
        "cliente": "51780-YAZAKI DO BRASIL LTDA",
        "valor": "88.90",
    },
    {
        "qru": "41132706",
        "numero": "5563509",
        "cliente": "50030-INSTITUTO MONTES RIBEIRO ME",
        "valor": "31.05",
    },
]


# ==========================================
# NORMALIZAR TEXTO
# ==========================================

def normalizar(valor):

    if pd.isna(valor):
        return ""

    return (
        str(valor)
        .strip()
        .upper()
    )


# ==========================================
# PREPARAR BASE
# ==========================================

for coluna in df.columns:

    df[coluna] = df[coluna].apply(normalizar)


# ==========================================
# TESTAR
# ==========================================

for teste in testes:

    print("\n" + "=" * 70)

    print("Qru:", teste["qru"])
    print("Numero:", teste["numero"])
    print("Cliente:", teste["cliente"])
    print("Valor:", teste["valor"])

    cliente = normalizar(teste["cliente"])

    # Procurar o cliente em todas as colunas
    encontrados = []

    for coluna in df.columns:

        mask = df[coluna] == cliente

        resultado = df[mask]

        if not resultado.empty:

            encontrados.append(
                (coluna, resultado)
            )

    if not encontrados:

        print("\nCLIENTE NÃO ENCONTRADO.")

        continue


    print("\nCLIENTE ENCONTRADO:")

    for coluna, resultado in encontrados:

        print(
            f"\nColuna: {coluna}"
        )

        print(
            "Quantidade:",
            len(resultado)
        )

        # Mostrar algumas colunas importantes
        colunas_mostrar = [
            c
            for c in [
                "No.Chamado",
                "eVoucher",
                "Cliente",
                "Valor",
                "Valor Corrida R$",
                "No.Registro",
                "Dt.Agenda",
                "No.Boleto",
            ]
            if c in resultado.columns
        ]

        print(
            resultado[
                colunas_mostrar
            ].head(10).to_string(index=False)
        )


print("\n\nFinalizado.")
