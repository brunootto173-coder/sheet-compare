import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

SHEET_CTA = 0
SHEET_TROCAS = "Recuperada_Planilha1"


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def normalizar_chave(valor):
    """
    Normaliza campos utilizados nas chaves compostas.

    - Converte para texto
    - Remove espaços nas extremidades
    - Corrige valores como 123.0 para 123
    """

    if pd.isna(valor):
        return ""

    texto = str(valor).strip()

    if texto.endswith(".0"):
        try:
            numero = float(texto)

            if numero.is_integer():
                texto = str(int(numero))

        except ValueError:
            pass

    return texto


def criar_chave(campo1, campo2):
    """
    Cria a chave composta utilizada no cruzamento.
    """

    return (
        campo1.map(normalizar_chave)
        + "|"
        + campo2.map(normalizar_chave)
    )


def normalizar_valor(valor):
    """
    Converte o valor monetário para número.
    """

    if pd.isna(valor):
        return 0.0

    if isinstance(valor, str):
        valor = valor.strip()

        if "," in valor:
            valor = valor.replace(".", "").replace(",", ".")

    return float(valor)


# ============================================================
# LEITURA CTA
# ============================================================

def ler_cta_trocas(arquivo_cta, arquivo_trocas):
    """
    Lê as duas planilhas utilizando a estrutura real
    do processo CTA x TROCAS.
    """

    cta = pd.read_excel(
        arquivo_cta,
        sheet_name=SHEET_CTA,
        header=2,
    )

    trocas = pd.read_excel(
        arquivo_trocas,
        sheet_name=SHEET_TROCAS,
        header=7,
    )

    colunas_cta = [
        "No.Chamado",
        "eVoucher",
        "Cliente",
        "Dt.Agenda",
        "Valor",
    ]

    colunas_trocas = [
        "Numero",
        "Qru",
        "Cliente",
        "Valor",
    ]

    faltantes_cta = [
        coluna
        for coluna in colunas_cta
        if coluna not in cta.columns
    ]

    if faltantes_cta:
        raise ValueError(
            f"Colunas ausentes na CTA: {faltantes_cta}"
        )

    faltantes_trocas = [
        coluna
        for coluna in colunas_trocas
        if coluna not in trocas.columns
    ]

    if faltantes_trocas:
        raise ValueError(
            f"Colunas ausentes na planilha de TROCAS: "
            f"{faltantes_trocas}"
        )

    return cta, trocas


# ============================================================
# PREPARAÇÃO DAS CHAVES
# ============================================================

def preparar_bases(cta, trocas):
    """
    Cria as chaves compostas e aplica a regra de
    última ocorrência.
    """

    cta = cta.copy()
    trocas = trocas.copy()

    # CTA:
    # No.Chamado + eVoucher
    cta["_CHAVE"] = criar_chave(
        cta["No.Chamado"],
        cta["eVoucher"],
    )

    # TROCAS:
    # Numero + Qru
    trocas["_CHAVE"] = criar_chave(
        trocas["Numero"],
        trocas["Qru"],
    )

    # Remove chaves completamente vazias
    cta = cta[
        cta["_CHAVE"].ne("|")
    ].copy()

    trocas = trocas[
        trocas["_CHAVE"].ne("|")
    ].copy()

    # Última ocorrência vence
    cta = cta.drop_duplicates(
        subset="_CHAVE",
        keep="last",
    ).copy()

    trocas = trocas.drop_duplicates(
        subset="_CHAVE",
        keep="last",
    ).copy()

    return cta, trocas


# ============================================================
# COMPARAÇÃO
# ============================================================

def comparar_cta_trocas(cta, trocas):
    """
    Compara CTA x TROCAS utilizando as chaves compostas.

    Retorna:
        todos
        valores_iguais
        valores_diferentes
        nao_encontrados
        resumo
    """

    trocas_por_chave = trocas.set_index(
        "_CHAVE"
    )

    resultados = []

    valores_iguais = []
    valores_diferentes = []
    nao_encontrados = []

    for _, linha_cta in cta.iterrows():

        chave = linha_cta["_CHAVE"]

        codigo = normalizar_chave(
            linha_cta["No.Chamado"]
        )

        evoucher = normalizar_chave(
            linha_cta["eVoucher"]
        )

        cliente_cta = linha_cta["Cliente"]

        data_cta = linha_cta["Dt.Agenda"]

        valor_cta = normalizar_valor(
            linha_cta["Valor"]
        )

        # ----------------------------------------------------
        # NÃO ENCONTRADO
        # ----------------------------------------------------

        if chave not in trocas_por_chave.index:

            registro = {
                "No.Chamado": codigo,
                "eVoucher": evoucher,
                "Cliente": cliente_cta,
                "Data": data_cta,
                "Valor CTA": valor_cta,
                "Valor Trocas": None,
                "Diferença": None,
                "Status": "Não Encontrado",
            }

            resultados.append(registro)
            nao_encontrados.append(registro)

            continue

        # ----------------------------------------------------
        # ENCONTRADO
        # ----------------------------------------------------

        linha_troca = trocas_por_chave.loc[chave]

        valor_troca = normalizar_valor(
            linha_troca["Valor"]
        )

        diferenca = round(
            valor_troca - valor_cta,
            2,
        )

        registro = {
            "No.Chamado": codigo,
            "eVoucher": evoucher,
            "Cliente": cliente_cta,
            "Data": data_cta,
            "Valor CTA": valor_cta,
            "Valor Trocas": valor_troca,
            "Diferença": diferenca,
            "Status": (
                "Valor Igual"
                if diferenca == 0
                else "Valor Diferente"
            ),
        }

        resultados.append(registro)

        if diferenca == 0:
            valores_iguais.append(registro)
        else:
            valores_diferentes.append(registro)

    # --------------------------------------------------------
    # DATAFRAMES
    # --------------------------------------------------------

    df_todos = pd.DataFrame(resultados)

    df_iguais = pd.DataFrame(
        valores_iguais
    )

    df_diferentes = pd.DataFrame(
        valores_diferentes
    )

    df_nao_encontrados = pd.DataFrame(
        nao_encontrados
    )

    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    encontrados = (
        len(df_iguais)
        + len(df_diferentes)
    )

    resumo = {
        "total_cta": len(cta),
        "total_trocas": len(trocas),
        "encontrados": encontrados,
        "valores_iguais": len(df_iguais),
        "valores_diferentes": len(df_diferentes),
        "nao_encontrados": len(df_nao_encontrados),
    }

    return {
        "todos": df_todos,
        "valores_iguais": df_iguais,
        "valores_diferentes": df_diferentes,
        "nao_encontrados": df_nao_encontrados,
        "resumo": resumo,
    }


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def executar_comparacao_bytes(
    nome_cta,
    dados_cta,
    nome_trocas,
    dados_trocas,
):
    """
    Executa a comparação CTA x TROCAS a partir dos
    arquivos selecionados pelo Flet.
    """

    import io

    extensao_cta = nome_cta.lower().split(".")[-1]
    extensao_trocas = nome_trocas.lower().split(".")[-1]

    if extensao_cta not in ["xlsx", "xls"]:
        raise ValueError(
            "A BASE CTA deve estar em formato XLS ou XLSX."
        )

    if extensao_trocas not in ["xlsx", "xls"]:
        raise ValueError(
            "A planilha de TROCAS deve estar em formato XLS ou XLSX."
        )

    cta = pd.read_excel(
        io.BytesIO(dados_cta),
        sheet_name=SHEET_CTA,
        header=2,
    )

    trocas = pd.read_excel(
        io.BytesIO(dados_trocas),
        sheet_name=SHEET_TROCAS,
        header=7,
    )

    colunas_cta = [
        "No.Chamado",
        "eVoucher",
        "Cliente",
        "Dt.Agenda",
        "Valor",
    ]

    colunas_trocas = [
        "Numero",
        "Qru",
        "Cliente",
        "Valor",
    ]

    faltantes_cta = [
        coluna
        for coluna in colunas_cta
        if coluna not in cta.columns
    ]

    if faltantes_cta:
        raise ValueError(
            f"Colunas ausentes na CTA: {faltantes_cta}"
        )

    faltantes_trocas = [
        coluna
        for coluna in colunas_trocas
        if coluna not in trocas.columns
    ]

    if faltantes_trocas:
        raise ValueError(
            "Colunas ausentes na planilha de TROCAS: "
            f"{faltantes_trocas}"
        )

    cta, trocas = preparar_bases(
        cta,
        trocas,
    )

    return comparar_cta_trocas(
        cta,
        trocas,
    )