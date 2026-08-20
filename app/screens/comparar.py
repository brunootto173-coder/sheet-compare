import flet as ft
import pandas as pd

from app.services.cta_trocas import executar_comparacao_bytes


# ==========================================
# CORES
# ==========================================

AMARELO = "#F5C518"
AMARELO_CLARO = "#FFF8D6"
GRAFITE = "#1E2329"
FUNDO = "#F5F6F8"
BRANCO = "#FFFFFF"
CINZA = "#667085"
BORDA = "#E4E7EC"
VERMELHO = "#D64545"
VERDE = "#2E9D59"


# ==========================================
# TELA PRINCIPAL
# ==========================================

def comparar_screen(page: ft.Page, ir_dashboard):

    arquivo_a = None
    arquivo_b = None

    nome_arquivo_a = ft.Text(
        "Nenhum arquivo selecionado",
        size=13,
        color=CINZA,
        text_align=ft.TextAlign.CENTER,
    )

    nome_arquivo_b = ft.Text(
        "Nenhum arquivo selecionado",
        size=13,
        color=CINZA,
        text_align=ft.TextAlign.CENTER,
    )

    status = ft.Text(
        "",
        size=14,
        color=VERMELHO,
        text_align=ft.TextAlign.CENTER,
    )

    # ======================================
    # VOLTAR PARA TELA INICIAL
    # ======================================

    def voltar_dashboard(e=None):
        ir_dashboard()

    # ======================================
    # MOSTRAR TABELA
    # ======================================

    def mostrar_registros(titulo, df, voltar_resultado):

        def voltar(e):
            voltar_resultado()

        colunas = list(df.columns)

        if len(colunas) == 0:

            conteudo_tabela = ft.Text(
                "Nenhum registro para exibir.",
                size=16,
                color=CINZA,
            )

        else:

            cabecalho = [
                ft.DataColumn(
                    ft.Text(
                        str(coluna),
                        weight=ft.FontWeight.BOLD,
                    )
                )
                for coluna in colunas
            ]

            linhas = []

            for _, linha in df.iterrows():

                celulas = []

                for coluna in colunas:

                    valor = linha[coluna]

                    if pd.isna(valor):
                        texto = ""
                    else:
                        texto = str(valor)

                    celulas.append(
                        ft.DataCell(
                            ft.Text(
                                texto,
                                size=12,
                            )
                        )
                    )

                linhas.append(
                    ft.DataRow(
                        cells=celulas
                    )
                )

            tabela = ft.DataTable(
                columns=cabecalho,
                rows=linhas,
                border=ft.Border.all(
                    1,
                    BORDA,
                ),
                heading_row_color=AMARELO_CLARO,
                column_spacing=25,
            )

            conteudo_tabela = ft.Row(
                controls=[tabela],
                scroll=ft.ScrollMode.ALWAYS,
            )

        pagina = ft.Container(
            expand=True,
            bgcolor=FUNDO,
            padding=30,
            content=ft.Column(
                controls=[

                    ft.Row(
                        controls=[

                            ft.Button(
                                content="← Voltar",
                                bgcolor=GRAFITE,
                                color=BRANCO,
                                on_click=voltar,
                            ),

                            ft.Container(
                                expand=True
                            ),

                            ft.Text(
                                titulo,
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=GRAFITE,
                            ),

                            ft.Container(
                                expand=True
                            ),

                            ft.Container(
                                width=80
                            ),
                        ],

                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.Container(
                        height=15
                    ),

                    ft.Text(
                        f"{len(df)} registros",
                        size=14,
                        color=CINZA,
                    ),

                    ft.Container(
                        height=15
                    ),

                    conteudo_tabela,
                ],

                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        page.clean()
        page.add(pagina)
        page.update()

    # ======================================
    # MOSTRAR RESULTADO CTA X TROCAS
    # ======================================

    def mostrar_resultado(resultado):

        resumo = resultado["resumo"]

        df_iguais = resultado["valores_iguais"]
        df_diferentes = resultado["valores_diferentes"]
        df_nao_encontrados = resultado["nao_encontrados"]

        # ----------------------------------
        # VOLTAR PARA TELA DE ARQUIVOS
        # ----------------------------------

        def voltar(e=None):

            page.clean()

            page.add(
                comparar_screen(
                    page,
                    ir_dashboard,
                )
            )

            page.update()

        # ----------------------------------
        # CARDS SIMPLES
        # ----------------------------------

        card_total_cta = ft.Container(
            expand=True,
            bgcolor=BRANCO,
            border=ft.Border.all(1, BORDA),
            border_radius=12,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "TOTAL CTA",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        str(resumo["total_cta"]),
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        card_total_trocas = ft.Container(
            expand=True,
            bgcolor=BRANCO,
            border=ft.Border.all(1, BORDA),
            border_radius=12,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "TOTAL TROCAS",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        str(resumo["total_trocas"]),
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        card_encontrados = ft.Container(
            expand=True,
            bgcolor="#E3F2FD",
            border_radius=12,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "ENCONTRADOS",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color="#1976D2",
                    ),

                    ft.Text(
                        str(resumo["encontrados"]),
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ----------------------------------
        # FUNÇÃO PARA VOLTAR AO RESULTADO
        # ----------------------------------

        def voltar_resultado():
            mostrar_resultado(resultado)

        # ----------------------------------
        # CARD IGUAIS
        # ----------------------------------

        card_iguais = ft.Container(
            expand=True,
            bgcolor="#E8F5E9",
            border_radius=12,
            padding=20,
            ink=True,
            on_click=lambda e: mostrar_registros(
                "Valores Iguais",
                df_iguais,
                voltar_resultado,
            ),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "VALORES IGUAIS",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=VERDE,
                    ),

                    ft.Text(
                        str(resumo["valores_iguais"]),
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        "Clique para visualizar",
                        size=12,
                        color=CINZA,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ----------------------------------
        # CARD DIFERENTES
        # ----------------------------------

        card_diferentes = ft.Container(
            expand=True,
            bgcolor="#FFF3CD",
            border_radius=12,
            padding=20,
            ink=True,
            on_click=lambda e: mostrar_registros(
                "Valores Diferentes",
                df_diferentes,
                voltar_resultado,
            ),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "VALORES DIFERENTES",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color="#B7791F",
                    ),

                    ft.Text(
                        str(resumo["valores_diferentes"]),
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        "Clique para visualizar",
                        size=12,
                        color=CINZA,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ----------------------------------
        # CARD NÃO ENCONTRADOS
        # ----------------------------------

        card_nao_encontrados = ft.Container(
            expand=True,
            bgcolor="#FFEBEE",
            border_radius=12,
            padding=20,
            ink=True,
            on_click=lambda e: mostrar_registros(
                "Não Encontrados",
                df_nao_encontrados,
                voltar_resultado,
            ),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "NÃO ENCONTRADOS",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=VERMELHO,
                    ),

                    ft.Text(
                        str(resumo["nao_encontrados"]),
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        "Clique para visualizar",
                        size=12,
                        color=CINZA,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        # ----------------------------------
        # PÁGINA DE RESULTADO
        # ----------------------------------

        pagina = ft.Container(
            expand=True,
            bgcolor=FUNDO,
            padding=30,
            content=ft.Column(
                controls=[

                    ft.Row(
                        controls=[

                            ft.Button(
                                content="← Voltar",
                                bgcolor=GRAFITE,
                                color=BRANCO,
                                on_click=voltar,
                            ),

                            ft.Container(
                                expand=True
                            ),

                            ft.Text(
                                "Resultado CTA × TROCAS",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                color=GRAFITE,
                            ),

                            ft.Container(
                                expand=True
                            ),

                            ft.Container(
                                width=80
                            ),
                        ],
                    ),

                    ft.Container(
                        height=20
                    ),

                    ft.Text(
                        f"CTA: {arquivo_a.name}",
                        size=14,
                        color=CINZA,
                    ),

                    ft.Text(
                        f"TROCAS: {arquivo_b.name}",
                        size=14,
                        color=CINZA,
                    ),

                    ft.Container(
                        height=20
                    ),

                    ft.Row(
                        controls=[
                            card_total_cta,
                            card_total_trocas,
                            card_encontrados,
                        ],
                        spacing=15,
                    ),

                    ft.Container(
                        height=15
                    ),

                    ft.Row(
                        controls=[
                            card_iguais,
                            card_diferentes,
                            card_nao_encontrados,
                        ],
                        spacing=15,
                    ),

                ],

                spacing=8,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        page.clean()
        page.add(pagina)
        page.update()

    # ======================================
    # EXECUTAR COMPARAÇÃO
    # ======================================

    def comparar(e=None):

        if arquivo_a is None:

            status.value = "Selecione a Planilha A primeiro."
            status.color = VERMELHO

            page.update()

            return

        if arquivo_b is None:

            status.value = "Selecione a Planilha B primeiro."
            status.color = VERMELHO

            page.update()

            return

        try:

            status.value = "Comparando planilhas..."
            status.color = GRAFITE

            page.update()

            resultado = executar_comparacao_bytes(
                arquivo_a.name,
                arquivo_a.bytes,
                arquivo_b.name,
                arquivo_b.bytes,
            )

            mostrar_resultado(resultado)

        except Exception as erro:

            page.clean()

            pagina_erro = ft.Container(
                expand=True,
                bgcolor=FUNDO,
                padding=40,
                content=ft.Column(
                    controls=[

                        ft.Text(
                            "Erro na comparação CTA × TROCAS",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=VERMELHO,
                        ),

                        ft.Container(
                            height=15
                        ),

                        ft.Text(
                            f"{type(erro).__name__}: {erro}",
                            size=15,
                            color=GRAFITE,
                        ),

                        ft.Container(
                            height=20
                        ),

                        ft.Button(
                            content="← Voltar",
                            bgcolor=GRAFITE,
                            color=BRANCO,
                            on_click=voltar_dashboard,
                        ),
                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )

            page.add(pagina_erro)
            page.update()

    # ======================================
    # SELECIONAR PLANILHA A
    # ======================================

    async def selecionar_a(e):

        nonlocal arquivo_a

        arquivos = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=[
                "xlsx",
                "xls",
                "csv",
            ],
        )

        if not arquivos:
            return

        arquivo_a = arquivos[0]

        nome_arquivo_a.value = arquivo_a.name
        nome_arquivo_a.color = GRAFITE

        status.value = ""

        page.update()

    # ======================================
    # SELECIONAR PLANILHA B
    # ======================================

    async def selecionar_b(e):

        nonlocal arquivo_b

        arquivos = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=[
                "xlsx",
                "xls",
                "csv",
            ],
        )

        if not arquivos:
            return

        arquivo_b = arquivos[0]

        nome_arquivo_b.value = arquivo_b.name
        nome_arquivo_b.color = GRAFITE

        status.value = ""

        page.update()

    # ======================================
    # CABEÇALHO
    # ======================================

    cabecalho = ft.Row(
        controls=[

            ft.Button(
                content="← Voltar",
                bgcolor=GRAFITE,
                color=BRANCO,
                on_click=voltar_dashboard,
            ),

            ft.Container(
                expand=True
            ),

            ft.Column(
                controls=[

                    ft.Text(
                        "Comparar Planilhas",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        "Compare duas planilhas e encontre diferenças.",
                        size=13,
                        color=CINZA,
                    ),
                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3,
            ),

            ft.Container(
                expand=True
            ),

            ft.Container(
                width=80
            ),
        ],

        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ======================================
    # CRIAR CARD DE ARQUIVO
    # ======================================

    def criar_card(
        titulo,
        descricao,
        nome_arquivo,
        selecionar,
    ):

        icone = ft.Container(
            width=64,
            height=64,
            bgcolor=AMARELO_CLARO,
            border_radius=32,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                "XLS",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=GRAFITE,
            ),
        )

        return ft.Container(
            expand=True,
            bgcolor=BRANCO,
            border=ft.Border.all(
                1,
                BORDA,
            ),
            border_radius=16,
            padding=28,
            content=ft.Column(
                controls=[

                    ft.Text(
                        titulo,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        descricao,
                        size=13,
                        color=CINZA,
                    ),

                    ft.Container(
                        height=12
                    ),

                    icone,

                    ft.Container(
                        height=10
                    ),

                    ft.Container(
                        width=280,
                        height=45,
                        bgcolor=FUNDO,
                        border_radius=8,
                        padding=10,
                        alignment=ft.Alignment.CENTER,
                        content=nome_arquivo,
                    ),

                    ft.Container(
                        height=10
                    ),

                    ft.Button(
                        content="Selecionar arquivo",
                        width=240,
                        height=45,
                        bgcolor=GRAFITE,
                        color=BRANCO,
                        on_click=selecionar,
                    ),
                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
        )

    # ======================================
    # CARDS A E B
    # ======================================

    card_a = criar_card(
        "Planilha A",
        "Selecione a primeira planilha.",
        nome_arquivo_a,
        selecionar_a,
    )

    card_b = criar_card(
        "Planilha B",
        "Selecione a segunda planilha.",
        nome_arquivo_b,
        selecionar_b,
    )

    area_arquivos = ft.Row(
        controls=[
            card_a,
            card_b,
        ],
        spacing=20,
        expand=True,
    )

    # ======================================
    # BOTÃO COMPARAR
    # ======================================

    botao_comparar = ft.Button(
        content="Comparar planilhas",
        width=300,
        height=52,
        bgcolor=AMARELO,
        color=GRAFITE,
        on_click=comparar,
    )

    # ======================================
    # INFORMAÇÃO
    # ======================================

    informacao = ft.Container(
        bgcolor=AMARELO_CLARO,
        border_radius=10,
        padding=12,
        content=ft.Text(
            "Formatos aceitos: XLSX, XLS e CSV",
            size=13,
            color=GRAFITE,
            text_align=ft.TextAlign.CENTER,
        ),
    )

    # ======================================
    # CONTEÚDO
    # ======================================

    conteudo = ft.Column(
        controls=[

            cabecalho,

            ft.Container(
                height=20
            ),

            area_arquivos,

            ft.Container(
                height=15
            ),

            informacao,

            ft.Container(
                height=15
            ),

            botao_comparar,

            status,
        ],

        spacing=8,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ======================================
    # RETORNO
    # ======================================

    return ft.Container(
        expand=True,
        bgcolor=FUNDO,
        padding=30,
        content=conteudo,
    )