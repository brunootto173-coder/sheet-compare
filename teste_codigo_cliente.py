import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO
# ============================================================

ARQUIVO_CTA = "BASE CTA.xlsx"
ARQUIVO_TROCAS = "18-08-2026 - troca.xls"
ARQUIVO_RESULTADO = "resultado_comparacao.xlsx"

SHEET_CTA = 0
SHEET_TROCAS = "Recuperada_Planilha1"

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def normalizar_chave(valor):
    """
    Normaliza os campos usados nas chaves.
    Mantém o conteúdo como texto e remove espaços.
    """
    if pd.isna(valor):
        return ""

    texto = str(valor).strip()

    # Corrige valores que o Excel/pandas transforma em 123.0
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
    Cria a chave composta.
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

        # Trata formato brasileiro, caso apareça como texto
        if "," in valor:
            valor = valor.replace(".", "").replace(",", ".")

    return float(valor)


# ============================================================
# LEITURA CTA
# ============================================================

print("=" * 70)
print("LENDO BASE CTA")
print("=" * 70)

cta = pd.read_excel(
    ARQUIVO_CTA,
    sheet_name=SHEET_CTA,
    header=2
)

print(f"Dimensão CTA: {cta.shape}")

# Verificação das colunas necessárias
colunas_cta = [
    "No.Chamado",
    "eVoucher",
    "Cliente",
    "Dt.Agenda",
    "Valor"
]

faltantes_cta = [
    col for col in colunas_cta
    if col not in cta.columns
]

if faltantes_cta:
    raise ValueError(
        f"Colunas ausentes na CTA: {faltantes_cta}\n"
        f"Colunas disponíveis: {list(cta.columns)}"
    )

# ============================================================
# LEITURA TROCAS
# ============================================================

print()
print("=" * 70)
print("LENDO BASE DE TROCAS")
print("=" * 70)

trocas = pd.read_excel(
    ARQUIVO_TROCAS,
    sheet_name=SHEET_TROCAS,
    header=7
)

print(f"Dimensão da base de trocas: {trocas.shape}")

colunas_trocas = [
    "Numero",
    "Qru",
    "Cliente",
    "Valor"
]

faltantes_trocas = [
    col for col in colunas_trocas
    if col not in trocas.columns
]

if faltantes_trocas:
    raise ValueError(
        f"Colunas ausentes na base de trocas: {faltantes_trocas}\n"
        f"Colunas disponíveis: {list(trocas.columns)}"
    )

# ============================================================
# CRIAÇÃO DAS CHAVES
# ============================================================

print()
print("=" * 70)
print("CRIANDO CHAVES")
print("=" * 70)

cta["_CHAVE"] = criar_chave(
    cta["No.Chamado"],
    cta["eVoucher"]
)

trocas["_CHAVE"] = criar_chave(
    trocas["Numero"],
    trocas["Qru"]
)

# ============================================================
# REMOVER CHAVES VAZIAS
# ============================================================

cta_validas = cta[
    cta["_CHAVE"].ne("|")
].copy()

trocas_validas = trocas[
    trocas["_CHAVE"].ne("|")
].copy()

print(f"CTA com chave válida: {len(cta_validas)}")
print(f"Trocas com chave válida: {len(trocas_validas)}")

# ============================================================
# DUPLICIDADES
# REGRA: A ÚLTIMA OCORRÊNCIA DA PLANILHA VENCE
# ============================================================

print()
print("=" * 70)
print("TRATANDO CHAVES DUPLICADAS")
print("=" * 70)

duplicadas_cta = cta_validas["_CHAVE"].duplicated(keep=False).sum()
duplicadas_trocas = trocas_validas["_CHAVE"].duplicated(keep=False).sum()

print(f"Registros CTA envolvidos em duplicidades: {duplicadas_cta}")
print(f"Registros Trocas envolvidos em duplicidades: {duplicadas_trocas}")

# keep="last" = mantém a última linha encontrada na planilha
cta_unica = cta_validas.drop_duplicates(
    subset="_CHAVE",
    keep="last"
).copy()

trocas_unicas = trocas_validas.drop_duplicates(
    subset="_CHAVE",
    keep="last"
).copy()

print(f"CTA após regra da última ocorrência: {len(cta_unica)}")
print(f"Trocas após regra da última ocorrência: {len(trocas_unicas)}")

# ============================================================
# ÍNDICES
# ============================================================

print()
print("=" * 70)
print("CRIANDO ÍNDICES")
print("=" * 70)

# Índice da base de trocas
trocas_por_chave = trocas_unicas.set_index("_CHAVE")

# ============================================================
# PROCESSAMENTO
# ============================================================

print()
print("=" * 70)
print("PROCESSANDO")
print("=" * 70)

resultados = []

valores_iguais = []
valores_diferentes = []
nao_encontrados = []

for _, linha_cta in cta_unica.iterrows():

    chave = linha_cta["_CHAVE"]

    codigo = normalizar_chave(linha_cta["No.Chamado"])
    evoucher = normalizar_chave(linha_cta["eVoucher"])

    cliente_cta = linha_cta["Cliente"]
    data_cta = linha_cta["Dt.Agenda"]

    valor_cta = normalizar_valor(linha_cta["Valor"])

    # --------------------------------------------------------
    # NÃO ENCONTRADO
    # --------------------------------------------------------

    if chave not in trocas_por_chave.index:

        registro = {
            "No.Chamado": codigo,
            "eVoucher": evoucher,
            "Cliente": cliente_cta,
            "Data": data_cta,
            "Valor CTA": valor_cta,
            "Valor Trocas": None,
            "Diferença": None,
            "Status": "Não Encontrado"
        }

        resultados.append(registro)
        nao_encontrados.append(registro)

        continue

    # --------------------------------------------------------
    # ENCONTRADO
    # --------------------------------------------------------

    linha_troca = trocas_por_chave.loc[chave]

    valor_troca = normalizar_valor(
        linha_troca["Valor"]
    )

    diferenca = round(
        valor_troca - valor_cta,
        2
    )

    # --------------------------------------------------------
    # CLIENTE E DATA SÃO APENAS INFORMAÇÕES
    # --------------------------------------------------------

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
        )
    }

    resultados.append(registro)

    if diferenca == 0:
        valores_iguais.append(registro)
    else:
        valores_diferentes.append(registro)


# ============================================================
# DATAFRAMES DOS RESULTADOS
# ============================================================

df_todos = pd.DataFrame(resultados)

df_iguais = pd.DataFrame(valores_iguais)

df_diferentes = pd.DataFrame(valores_diferentes)

df_nao_encontrados = pd.DataFrame(nao_encontrados)

# ============================================================
# RESUMO
# ============================================================

print()
print("=" * 70)
print("RESUMO")
print("=" * 70)

print(
    f"Registros CTA considerados:   {len(cta_unica)}"
)

print(
    f"Chaves encontradas:            "
    f"{len(df_iguais) + len(df_diferentes)}"
)

print(
    f"Valores iguais:                {len(df_iguais)}"
)

print(
    f"Valores diferentes:            {len(df_diferentes)}"
)

print(
    f"Não encontrados:               {len(df_nao_encontrados)}"
)

# ============================================================
# MOSTRAR VALORES DIFERENTES
# ============================================================

print()
print("=" * 70)
print(f"VALORES DIFERENTES: {len(df_diferentes)}")
print("=" * 70)

if len(df_diferentes) > 0:

    print(
        df_diferentes[
            [
                "No.Chamado",
                "eVoucher",
                "Cliente",
                "Data",
                "Valor CTA",
                "Valor Trocas",
                "Diferença"
            ]
        ]
        .to_string(index=False)
    )

else:

    print("NENHUM VALOR DIFERENTE.")

# ============================================================
# MOSTRAR NÃO ENCONTRADOS
# ============================================================

print()
print("=" * 70)
print(f"NÃO ENCONTRADOS: {len(df_nao_encontrados)}")
print("=" * 70)

if len(df_nao_encontrados) > 0:

    print(
        df_nao_encontrados[
            [
                "No.Chamado",
                "eVoucher",
                "Cliente",
                "Data",
                "Valor CTA"
            ]
        ]
        .head(100)
        .to_string(index=False)
    )

    if len(df_nao_encontrados) > 100:
        print(
            f"\n... e mais "
            f"{len(df_nao_encontrados) - 100} registros."
        )

else:

    print("TODOS OS CÓDIGOS FORAM ENCONTRADOS.")

# ============================================================
# SALVAR EXCEL
# ============================================================

print()
print("=" * 70)
print("SALVANDO RESULTADO")
print("=" * 70)

with pd.ExcelWriter(
    ARQUIVO_RESULTADO,
    engine="openpyxl"
) as writer:

    df_todos.to_excel(
        writer,
        sheet_name="Todos",
        index=False
    )

    df_iguais.to_excel(
        writer,
        sheet_name="Valores Iguais",
        index=False
    )

    df_diferentes.to_excel(
        writer,
        sheet_name="Valores Diferentes",
        index=False
    )

    df_nao_encontrados.to_excel(
        writer,
        sheet_name="Nao Encontrados",
        index=False
    )

# ============================================================
# FINAL
# ============================================================

print()
print("=" * 70)
print("FINALIZADO")
print("=" * 70)

print(
    f"Arquivo criado: {ARQUIVO_RESULTADO}"
)

print()
print("Abas criadas:")
print("  1. Todos")
print("  2. Valores Iguais")
print("  3. Valores Diferentes")
print("  4. Nao Encontrados")
