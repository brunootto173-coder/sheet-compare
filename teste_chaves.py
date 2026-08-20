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
# REGISTROS DA VALE
# ==========================================

testes = [
    ("41027193", "5558524"),
    ("41118645", "5562900"),
    ("41132706", "5563509"),
    ("41140489", "5563875"),
    ("41167763", "5564999"),
    ("41096190", "5561829"),
    ("41113670", "5562618"),
    ("41120364", "5563015"),
    ("41120744", "5563044"),
    ("41132907", "5563520"),
]


# ==========================================
# NORMALIZAR
# ==========================================

def normalizar(valor):

    if pd.isna(valor):
        return ""

    return str(valor).strip()


for coluna in df.columns:
    df[coluna] = df[coluna].apply(normalizar)


# ==========================================
# PROCURAR OS DOIS VALORES NA MESMA LINHA
# ==========================================

for qru, numero in testes:

    print("\n" + "=" * 80)

    print("VALE:")
    print("  Qru:    ", qru)
    print("  Numero: ", numero)

    encontrou_qru = []
    encontrou_numero = []

    # Procurar Qru
    for coluna in df.columns:

        resultado = df[
            df[coluna] == qru
        ]

        if not resultado.empty:

            for indice in resultado.index:

                encontrou_qru.append(
                    (indice, coluna)
                )

    # Procurar Numero
    for coluna in df.columns:

        resultado = df[
            df[coluna] == numero
        ]

        if not resultado.empty:

            for indice in resultado.index:

                encontrou_numero.append(
                    (indice, coluna)
                )


    print("\nQru encontrado em:")

    if encontrou_qru:
        for indice, coluna in encontrou_qru:
            print(
                f"  linha {indice} -> {coluna}"
            )
    else:
        print("  NÃO ENCONTRADO")


    print("\nNumero encontrado em:")

    if encontrou_numero:
        for indice, coluna in encontrou_numero:
            print(
                f"  linha {indice} -> {coluna}"
            )
    else:
        print("  NÃO ENCONTRADO")


    # ======================================
    # VERIFICAR MESMA LINHA
    # ======================================

    linhas_qru = {
        indice
        for indice, coluna
        in encontrou_qru
    }

    linhas_numero = {
        indice
        for indice, coluna
        in encontrou_numero
    }

    mesmas_linhas = (
        linhas_qru &
        linhas_numero
    )


    print("\nMESMA LINHA:")

    if mesmas_linhas:

        for indice in mesmas_linhas:

            print(
                f"  SIM -> linha {indice}"
            )

            linha = df.loc[indice]

            colunas_importantes = [
                "No.Chamado",
                "eVoucher",
                "Cliente",
                "Valor",
                "Valor Corrida R$",
                "No.Registro",
                "No.Boleto",
                "Dt.Agenda",
            ]

            colunas_importantes = [
                coluna
                for coluna in colunas_importantes
                if coluna in df.columns
            ]

            print(
                linha[
                    colunas_importantes
                ].to_string()
            )

    else:

        print(
            "  NÃO. Os dois valores não aparecem na mesma linha."
        )


print("\n\nFinalizado.")
