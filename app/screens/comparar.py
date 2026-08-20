import flet as ft

from services.excel_reader import ler_planilha
from services.excel_comparator import comparar_planilhas
from screens.selecao import selecao_screen


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
# TELA DE COMPARAÇÃO
# ==========================================

def comparar_screen(page: ft.Page, ir_dashboard):

    # ======================================
    # ARQUIVOS
    # ======================================

    arquivo_a = None
    arquivo_b = None

    # ======================================
    # TEXTOS
    # ======================================

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
        text_align=ft.TextAlign.CENTER,
    )

    # ======================================
    # RESULTADO / SELEÇÃO DA COLUNA
    # ======================================

    def mostrar_resultado(df_a, df_b):

        # ==================================
        # VOLTAR PARA A TELA DE SELEÇÃO
        # ==================================

        def voltar(e):

            page.clean()

            page.add(
                comparar_screen(
                    page,
                    ir_dashboard,
                )
            )

            page.update()

        # ==================================
        # MOSTRAR RESULTADO DA COMPARAÇÃO
        # ==================================

        def mostrar_resultado_comparacao(
            resultado,
            coluna,
        ):

            adicionados = resultado["adicionados"]
            removidos = resultado["removidos"]
            alterados = resultado["alterados"]
            iguais = resultado["iguais"]

            # ------------------------------
            # VOLTAR
            # ------------------------------

            def voltar_resultado(e):

                page.clean()

                page.add(
                    comparar_screen(
                        page,
                        ir_dashboard,
                    )
                )

                page.update()

            # ------------------------------
            # CARD IGUAIS
            # ------------------------------

            card_iguais = ft.Container(
                expand=True,
                bgcolor="#E8F5E9",
                border_radius=12,
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "IGUAIS",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=VERDE,
                        ),

                        ft.Text(
                            str(len(iguais)),
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=GRAFITE,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )

            # ------------------------------
            # CARD ALTERADOS
            # ------------------------------

            card_alterados = ft.Container(
                expand=True,
                bgcolor="#FFF3CD",
                border_radius=12,
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "ALTERADOS",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="#B7791F",
                        ),

                        ft.Text(
                            str(len(alterados)),
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=GRAFITE,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )

            # ------------------------------
            # CARD ADICIONADOS
            # ------------------------------

            card_adicionados = ft.Container(
                expand=True,
                bgcolor="#E3F2FD",
                border_radius=12,
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "ADICIONADOS",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color="#1976D2",
                        ),

                        ft.Text(
                            str(len(adicionados)),
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=GRAFITE,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )

            # ------------------------------
            # CARD REMOVIDOS
            # ------------------------------

            card_removidos = ft.Container(
                expand=True,
                bgcolor="#FFEBEE",
                border_radius=12,
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "REMOVIDOS",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=VERMELHO,
                        ),

                        ft.Text(
                            str(len(removidos)),
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=GRAFITE,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )

            # ------------------------------
            # RESUMO
            # ------------------------------

            resumo = ft.Container(
                bgcolor=BRANCO,
                border=ft.Border.all(
                    1,
                    BORDA,
                ),
                border_radius=12,
                padding=25,
                content=ft.Column(
                    controls=[

                        ft.Text(
                            "Resumo da comparação",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=GRAFITE,
                        ),

                        ft.Text(
                            f"{len(iguais)} registros permaneceram iguais.",
                            size=14,
                            color=CINZA,
                        ),

                        ft.Text(
                            f"{len(alterados)} registros foram alterados.",
                            size=14,
                            color=CINZA,
                        ),

                        ft.Text(
                            f"{len(adicionados)} registros foram adicionados.",
                            size=14,
                            color=CINZA,
                        ),

                        ft.Text(
                            f"{len(removidos)} registros foram removidos.",
                            size=14,
                            color=CINZA,
                        ),
                    ],
                    spacing=8,
                ),
            )

            # ------------------------------
            # TELA DE RESULTADO
            # ------------------------------

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
                                    on_click=voltar_resultado,
                                ),

                                ft.Container(
                                    expand=True
                                ),

                                ft.Text(
                                    "Resultado da comparação",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color=GRAFITE,
                                ),

                                ft.Container(
                                    expand=True
                                ),

                            ],
                        ),

                        ft.Container(
                            height=10
                        ),

                        ft.Text(
                            f"Coluna utilizada: {coluna}",
                            size=14,
                            color=CINZA,
                        ),

                        ft.Container(
                            height=20
                        ),

                        ft.Row(
                            controls=[
                                card_iguais,
                                card_alterados,
                                card_adicionados,
                                card_removidos,
                            ],
                            spacing=15,
                        ),

                        ft.Container(
                            height=25
                        ),

                        resumo,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            )

            page.clean()

            page.add(pagina)

            page.update()

        # ==================================
        # INICIAR COMPARAÇÃO
        # ==================================

        def iniciar_comparacao(coluna):

            try:

                resultado = comparar_planilhas(
                    df_a,
                    df_b,
                    coluna,
                )

                mostrar_resultado_comparacao(
                    resultado,
                    coluna,
                )

            except Exception as erro:

                page.clean()

                pagina_erro = ft.Container(
                    expand=True,
                    bgcolor=FUNDO,
                    padding=40,
                    content=ft.Column(
                        controls=[

                            ft.Text(
                                "Erro na comparação",
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
                                on_click=voltar,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )

                page.add(pagina_erro)

                page.update()

        # ==================================
        # ABRIR TELA DE SELEÇÃO
        # ==================================

        page.clean()

        page.add(
            selecao_screen(
                page=page,
                df_a=df_a,
                df_b=df_b,
                iniciar_comparacao=iniciar_comparacao,
                voltar=voltar,
            )
        )

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
    # COMPARAR
    # ======================================

    def comparar(e):

        if arquivo_a is None:

            status.value = (
                "Selecione a Planilha A primeiro."
            )

            status.color = VERMELHO

            page.update()

            return

        if arquivo_b is None:

            status.value = (
                "Selecione a Planilha B primeiro."
            )

            status.color = VERMELHO

            page.update()

            return

        try:

            df_a = ler_planilha(
                arquivo_a.name,
                arquivo_a.bytes,
            )

            df_b = ler_planilha(
                arquivo_b.name,
                arquivo_b.bytes,
            )

            mostrar_resultado(
                df_a,
                df_b,
            )

        except Exception as erro:

            status.value = (
                f"Erro ao ler as planilhas: "
                f"{type(erro).__name__}: {erro}"
            )

            status.color = VERMELHO

            page.update()

    # ======================================
    # VOLTAR AO DASHBOARD
    # ======================================

    def voltar_dashboard(e):

        ir_dashboard()

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
    # CRIAR CARD
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
    # CARDS
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

    # ======================================
    # ÁREA DOS ARQUIVOS
    # ======================================

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
