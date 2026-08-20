import pandas as pd


def comparar_planilhas(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    coluna_chave: str,
):
    """
    Compara duas planilhas usando uma coluna como identificador.

    Retorna:
        adicionados
        removidos
        alterados
        iguais
    """

    # ==========================================
    # VALIDAR COLUNA-CHAVE
    # ==========================================

    if coluna_chave not in df_a.columns:
        raise ValueError(
            f"A coluna '{coluna_chave}' não existe na Planilha A."
        )

    if coluna_chave not in df_b.columns:
        raise ValueError(
            f"A coluna '{coluna_chave}' não existe na Planilha B."
        )

    # ==========================================
    # COPIAR DATAFRAMES
    # ==========================================

    a = df_a.copy()
    b = df_b.copy()

    # ==========================================
    # TRANSFORMAR CHAVE EM TEXTO
    # ==========================================

    a[coluna_chave] = a[coluna_chave].astype(str)
    b[coluna_chave] = b[coluna_chave].astype(str)

    # ==========================================
    # VERIFICAR CHAVES DUPLICADAS
    # ==========================================

    if a[coluna_chave].duplicated().any():

        raise ValueError(
            f"A coluna '{coluna_chave}' possui valores "
            "duplicados na Planilha A."
        )

    if b[coluna_chave].duplicated().any():

        raise ValueError(
            f"A coluna '{coluna_chave}' possui valores "
            "duplicados na Planilha B."
        )

    # ==========================================
    # INDEXAR PELA CHAVE
    # ==========================================

    a = a.set_index(coluna_chave)
    b = b.set_index(coluna_chave)

    # ==========================================
    # IDENTIFICAR REGISTROS
    # ==========================================

    chaves_a = set(a.index)
    chaves_b = set(b.index)

    adicionados_chaves = chaves_b - chaves_a
    removidos_chaves = chaves_a - chaves_b
    comuns_chaves = chaves_a & chaves_b

    # ==========================================
    # ADICIONADOS
    # ==========================================

    adicionados = b.loc[
        list(adicionados_chaves)
    ]

    # ==========================================
    # REMOVIDOS
    # ==========================================

    removidos = a.loc[
        list(removidos_chaves)
    ]

    # ==========================================
    # ALTERADOS E IGUAIS
    # ==========================================

    alterados = []
    iguais = []

    # Colunas existentes nas duas planilhas
    colunas_comuns = [
        coluna
        for coluna in a.columns
        if coluna in b.columns
    ]

    for chave in comuns_chaves:

        linha_a = a.loc[chave]
        linha_b = b.loc[chave]

        mudou = False

        for coluna in colunas_comuns:

            valor_a = linha_a[coluna]
            valor_b = linha_b[coluna]

            # Trata NaN como valores iguais
            if pd.isna(valor_a) and pd.isna(valor_b):
                continue

            if pd.isna(valor_a) != pd.isna(valor_b):

                mudou = True
                break

            if str(valor_a) != str(valor_b):

                mudou = True
                break

        if mudou:
            alterados.append(chave)
        else:
            iguais.append(chave)

    # ==========================================
    # DATAFRAME DE ALTERADOS
    # ==========================================

    alterados_df = b.loc[
        list(alterados)
    ]

    # ==========================================
    # DETALHES DAS ALTERAÇÕES
    # ==========================================

    detalhes_alteracoes = []

    for chave in alterados:

        linha_a = a.loc[chave]
        linha_b = b.loc[chave]

        mudancas = []

        for coluna in colunas_comuns:

            valor_a = linha_a[coluna]
            valor_b = linha_b[coluna]

            # Ambos vazios
            if pd.isna(valor_a) and pd.isna(valor_b):
                continue

            # Um vazio e outro preenchido
            if pd.isna(valor_a) != pd.isna(valor_b):

                mudancas.append(
                    {
                        "coluna": coluna,
                        "antes": valor_a,
                        "depois": valor_b,
                    }
                )

                continue

            # Valores diferentes
            if str(valor_a) != str(valor_b):

                mudancas.append(
                    {
                        "coluna": coluna,
                        "antes": valor_a,
                        "depois": valor_b,
                    }
                )

        detalhes_alteracoes.append(
            {
                "chave": chave,
                "mudancas": mudancas,
            }
        )

    # ==========================================
    # RETORNO
    # ==========================================

    return {
        "adicionados": adicionados,
        "removidos": removidos,
        "alterados": alterados_df,
        "iguais": b.loc[list(iguais)],
        "detalhes_alteracoes": detalhes_alteracoes,
    }
