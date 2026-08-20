import io
import pandas as pd


def ler_planilha(nome_arquivo, dados):

    extensao = nome_arquivo.lower().split(".")[-1]

    if extensao == "csv":

        return pd.read_csv(
            io.BytesIO(dados)
        )

    if extensao in ["xlsx", "xls"]:

        return pd.read_excel(
            io.BytesIO(dados)
        )

    raise ValueError(
        "Formato de arquivo não suportado."
    )


def ler_vale_troca(nome_arquivo, dados):
    """
    Lê a planilha VALE - TROCA.

    A planilha possui vários blocos de motoristas.
    Cada bloco contém novamente os cabeçalhos:

        Documento | Qru | Numero | Cliente | Valor | Atendente

    Para a comparação, somente estes campos interessam:

        Qru
        Numero
        Cliente
        Valor

    Todas as demais linhas são ignoradas.
    """

    extensao = nome_arquivo.lower().split(".")[-1]

    if extensao not in ["xlsx", "xls"]:
        raise ValueError(
            "A planilha VALE - TROCA deve estar em formato XLS ou XLSX."
        )

    df = pd.read_excel(
        io.BytesIO(dados),
        header=None,
    )

    # ==========================================
    # COLUNAS REAIS DA VALE - TROCA
    # ==========================================

    COLUNA_QRU = 2
    COLUNA_NUMERO = 3
    COLUNA_CLIENTE = 4
    COLUNA_VALOR = 9

    registros = []

    for _, linha in df.iterrows():

        qru = linha.iloc[COLUNA_QRU]
        numero = linha.iloc[COLUNA_NUMERO]
        cliente = linha.iloc[COLUNA_CLIENTE]
        valor = linha.iloc[COLUNA_VALOR]

        # ======================================
        # IGNORAR LINHAS QUE NÃO SÃO CORRIDAS
        # ======================================

        if pd.isna(qru):
            continue

        if pd.isna(numero):
            continue

        if pd.isna(cliente):
            continue

        if pd.isna(valor):
            continue

        # ======================================
        # GARANTIR QUE VALOR É NUMÉRICO
        # ======================================

        try:
            valor_numerico = float(valor)
        except (ValueError, TypeError):
            continue

        # ======================================
        # ADICIONAR REGISTRO
        # ======================================

        registros.append(
            {
                "Qru": qru,
                "Numero": numero,
                "Cliente": cliente,
                "Valor": valor_numerico,
            }
        )

    resultado = pd.DataFrame(
        registros,
        columns=[
            "Qru",
            "Numero",
            "Cliente",
            "Valor",
        ],
    )

    return resultado

def ler_cta(nome_arquivo, dados):
    """
    Lê a planilha CTA.

    Campos utilizados na comparação:

        No.Chamado
        eVoucher
        Cliente
        Valor
    """

    extensao = nome_arquivo.lower().split(".")[-1]

    if extensao == "csv":

        df = pd.read_csv(
            io.BytesIO(dados)
        )

    elif extensao in ["xlsx", "xls"]:

        df = pd.read_excel(
            io.BytesIO(dados)
        )

    else:

        raise ValueError(
            "A planilha CTA deve estar em formato XLS, XLSX ou CSV."
        )

    # ==========================================
    # VALIDAR COLUNAS
    # ==========================================

    colunas_obrigatorias = [
        "No.Chamado",
        "eVoucher",
        "Cliente",
        "Valor",
    ]

    faltantes = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    if faltantes:

        raise ValueError(
            "A planilha CTA não possui as colunas obrigatórias: "
            + ", ".join(faltantes)
        )

    # ==========================================
    # SELECIONAR SOMENTE O NECESSÁRIO
    # ==========================================

    resultado = df[
        [
            "No.Chamado",
            "eVoucher",
            "Cliente",
            "Valor",
        ]
    ].copy()

    # ==========================================
    # REMOVER LINHAS SEM IDENTIFICAÇÃO
    # ==========================================

    resultado = resultado.dropna(
        subset=[
            "No.Chamado",
            "eVoucher",
        ]
    )

    # ==========================================
    # NORMALIZAR VALOR
    # ==========================================

    resultado["Valor"] = pd.to_numeric(
        resultado["Valor"],
        errors="coerce",
    )

    # ==========================================
    # REMOVER VALORES SEM VALOR
    # ==========================================

    resultado = resultado.dropna(
        subset=["Valor"]
    )

    return resultado.reset_index(drop=True)
