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


testes = [
    {
        "cliente": "51780-YAZAKI DO BRASIL LTDA",
        "valor": "88.90",
    },
    {
        "cliente": "50030-INSTITUTO MONTES RIBEIRO ME",
        "valor": "31.05",
    },
    {
        "cliente": "50960-PSG COMERCIO DE ALIMENTOS LTDA",
        "valor": "35.00",
    },
]


for teste in testes:

    cliente = teste["cliente"]
    valor = teste["valor"]

    print("\n" + "=" * 80)
    print("CLIENTE:", cliente)
    print("VALOR:", valor)

    # procura parte do nome do cliente
    parte_cliente = cliente.split("-", 1)[-1].strip()

    mask_cliente = (
        df["Cliente"]
        .fillna("")
        .str.upper()
        .str.contains(
            parte_cliente.upper(),
            regex=False,
        )
    )

    encontrados = df[mask_cliente]

    print("\nRegistros encontrados pelo cliente:", len(encontrados))

    if len(encontrados) == 0:
        print("CLIENTE NÃO ENCONTRADO.")
        continue

    # mostrar registros do cliente
    colunas = [
        "No.Chamado",
        "eVoucher",
        "Cliente",
        "Valor",
        "Valor Corrida R$",
        "No.Registro",
        "No.Boleto",
        "Dt.Agenda",
    ]

    colunas_existentes = [
        c for c in colunas
        if c in df.columns
    ]

    print(
        encontrados[colunas_existentes]
        .head(20)
        .to_string(index=True)
    )

    # tentar encontrar o valor
    valores = encontrados[
        encontrados["Valor"]
        .fillna("")
        .str.replace(",", ".", regex=False)
        == valor
    ]

    print("\nRegistros com CLIENTE + VALOR:", len(valores))

    if len(valores):
        print(
            valores[colunas_existentes]
            .to_string(index=True)
        )


print("\nFinalizado.")
