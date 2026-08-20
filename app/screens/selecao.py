import flet as ft


AMARELO = "#F5C518"
AMARELO_CLARO = "#FFF8D6"
GRAFITE = "#1E2329"
FUNDO = "#F5F6F8"
BRANCO = "#FFFFFF"
CINZA = "#667085"
BORDA = "#E4E7EC"
VERMELHO = "#D64545"


def selecao_screen(
    page: ft.Page,
    df_a,
    df_b,
    iniciar_comparacao,
    voltar,
):

    # ======================================
    # COLUNAS EM COMUM
    # ======================================

    colunas_a = list(df_a.columns)
    colunas_b = list(df_b.columns)

    colunas_comuns = [
        coluna
        for coluna in colunas_a
        if coluna in colunas_b
    ]

    # ======================================
    # MENSAGEM
    # ======================================

    mensagem = ft.Text(
        "",
        size=14,
        color=VERMELHO,
        text_align=ft.TextAlign.CENTER,
    )

    # ======================================
    # DROPDOWN
    # ======================================

    opcoes = [
        ft.DropdownOption(
            key=str(coluna),
            text=str(coluna),
        )
        for coluna in colunas_comuns
    ]

    coluna_selecionada = ft.Dropdown(
        label="Coluna que identifica cada registro",
        hint_text="Selecione uma coluna",
        options=opcoes,
        width=450,
    )

    # ======================================
    # CONTINUAR
    # ======================================

    def continuar(e):

        if coluna_selecionada.value is None:
            mensagem.value = (
                "Selecione uma coluna para continuar."
            )

            page.update()
            return

        iniciar_comparacao(
            coluna_selecionada.value
        )

    # ======================================
    # CABEÇALHO
    # ======================================

    cabecalho = ft.Row(
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

            ft.Column(
                controls=[
                    ft.Text(
                        "Identificar registros",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        "Escolha a coluna usada para identificar cada registro.",
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
    # INFORMAÇÕES
    # ======================================

    info_a = ft.Container(
        expand=True,
        bgcolor=BRANCO,
        border=ft.Border.all(1, BORDA),
        border_radius=12,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "PLANILHA A",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=GRAFITE,
                ),

                ft.Text(
                    f"{len(df_a)} registros",
                    size=14,
                    color=CINZA,
                ),

                ft.Text(
                    f"{len(df_a.columns)} colunas",
                    size=14,
                    color=CINZA,
                ),
            ],
            spacing=5,
        ),
    )

    info_b = ft.Container(
        expand=True,
        bgcolor=BRANCO,
        border=ft.Border.all(1, BORDA),
        border_radius=12,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "PLANILHA B",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=GRAFITE,
                ),

                ft.Text(
                    f"{len(df_b)} registros",
                    size=14,
                    color=CINZA,
                ),

                ft.Text(
                    f"{len(df_b.columns)} colunas",
                    size=14,
                    color=CINZA,
                ),
            ],
            spacing=5,
        ),
    )

    # ======================================
    # AVISO
    # ======================================

    aviso = ft.Container(
        bgcolor=AMARELO_CLARO,
        border_radius=10,
        padding=18,
        content=ft.Text(
            "A coluna escolhida precisa existir nas duas "
            "planilhas e identificar cada registro de forma única.",
            size=14,
            color=GRAFITE,
            text_align=ft.TextAlign.CENTER,
        ),
    )

    # ======================================
    # BOTÃO
    # ======================================

    botao = ft.Button(
        content="Continuar para comparação",
        width=320,
        height=52,
        bgcolor=AMARELO,
        color=GRAFITE,
        on_click=continuar,
    )

    # ======================================
    # LAYOUT
    # ======================================

    conteudo = ft.Column(
        controls=[
            cabecalho,

            ft.Container(
                height=25
            ),

            ft.Row(
                controls=[
                    info_a,
                    info_b,
                ],
                spacing=20,
            ),

            ft.Container(
                height=25
            ),

            aviso,

            ft.Container(
                height=25
            ),

            ft.Text(
                "Coluna-chave",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=GRAFITE,
            ),

            coluna_selecionada,

            mensagem,

            ft.Container(
                height=10
            ),

            botao,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.Container(
        expand=True,
        bgcolor=FUNDO,
        padding=30,
        content=conteudo,
    )
