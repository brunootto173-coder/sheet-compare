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


valores = [
    "41118645",
    "5562900",
    "41132706",
    "5563509",
    "41140489",
    "5563875",
]


for valor in valores:

    print("\n" + "=" * 70)
    print("PROCURANDO:", valor)

    encontrou = False

    for coluna in df.columns:

        serie = (
            df[coluna]
            .fillna("")
            .astype(str)
        )

        # procura o valor dentro do conteúdo da célula
        mask = serie.str.contains(
            valor,
            regex=False,
            na=False,
        )

        resultado = df[mask]

        if not resultado.empty:

            encontrou = True

            print(
                f"\nEncontrado na coluna: {coluna}"
            )

            print(
                "Quantidade:",
                len(resultado)
            )

            print(
                resultado[
                    [
                        c
                        for c in [
                            "No.Chamado",
                            "eVoucher",
                            "Cliente",
                            "Valor",
                            "Valor Corrida R$",
                            "Dt.Agenda",
                        ]
                        if c in df.columns
                    ]
                ].head(10).to_string(index=False)
            )

    if not encontrou:
        print("NÃO ENCONTRADO EM NENHUMA CÉLULA.")


print("\nFinalizado.")

