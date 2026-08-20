import flet as ft


AMARELO = "#F5C518"
GRAFITE = "#1E2329"
GRAFITE_ESCURO = "#15181C"
FUNDO = "#F5F6F8"
BRANCO = "#FFFFFF"
CINZA = "#666666"


def dashboard_screen(page: ft.Page, ir_comparar, ir_login):

    def criar_card(titulo, descricao, cor, acao=None):

        conteudo = ft.Container(
            width=250,
            height=150,
            bgcolor=BRANCO,
            border_radius=12,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        titulo,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        descricao,
                        size=13,
                        color=CINZA,
                    ),

                    ft.Container(expand=True),

                    ft.Container(
                        height=5,
                        bgcolor=cor,
                        border_radius=5,
                    ),
                ],
                spacing=8,
            ),
        )

        if acao:
            return ft.Button(
                content=conteudo,
                width=250,
                height=150,
                on_click=acao,
            )

        return conteudo

    menu = ft.Container(
        width=240,
        bgcolor=GRAFITE_ESCURO,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "SHEET",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=AMARELO,
                ),

                ft.Text(
                    "COMPARE",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=BRANCO,
                ),

                ft.Divider(
                    color="#3A3F45",
                    height=30,
                ),

                ft.Container(
                    content=ft.Text(
                        "Dashboard",
                        color=GRAFITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    bgcolor=AMARELO,
                    padding=15,
                    border_radius=8,
                    width=210,
                ),

                ft.Button(
                    content="Comparar Planilhas",
                    width=210,
                    bgcolor=GRAFITE_ESCURO,
                    color=BRANCO,
                    on_click=lambda e: ir_comparar(),
                ),

                ft.Button(
                    content="Organizar Planilhas",
                    width=210,
                    bgcolor=GRAFITE_ESCURO,
                    color=BRANCO,
                ),

                ft.Button(
                    content="Histórico",
                    width=210,
                    bgcolor=GRAFITE_ESCURO,
                    color=BRANCO,
                ),

                ft.Button(
                    content="Configurações",
                    width=210,
                    bgcolor=GRAFITE_ESCURO,
                    color=BRANCO,
                ),

                ft.Container(expand=True),

                ft.Button(
                    content="Sair",
                    width=210,
                    bgcolor=GRAFITE_ESCURO,
                    color=BRANCO,
                    on_click=lambda e: ir_login(),
                ),
            ],
            spacing=8,
        ),
    )

    cabecalho = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text(
                        "Dashboard",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=GRAFITE,
                    ),

                    ft.Text(
                        "Visão geral do sistema",
                        size=14,
                        color=CINZA,
                    ),
                ],
                spacing=3,
            ),

            ft.Container(expand=True),

            ft.Text(
                "Admin",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=GRAFITE,
            ),
        ]
    )

    boas_vindas = ft.Container(
        bgcolor=AMARELO,
        border_radius=12,
        padding=25,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Olá, Admin! 👋",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=GRAFITE,
                ),

                ft.Text(
                    "O que você deseja fazer hoje?",
                    size=15,
                    color=GRAFITE,
                ),
            ],
            spacing=5,
        ),
    )

    cards = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    criar_card(
                        "Comparar Planilhas",
                        "Compare duas ou mais planilhas.",
                        AMARELO,
                        lambda e: ir_comparar(),
                    ),

                    criar_card(
                        "Organizar Planilhas",
                        "Organize seus arquivos e dados.",
                        GRAFITE,
                    ),
                ],
                spacing=20,
            ),

            ft.Row(
                controls=[
                    criar_card(
                        "Histórico",
                        "Consulte comparações anteriores.",
                        AMARELO,
                    ),

                    criar_card(
                        "Configurações",
                        "Configure o sistema.",
                        GRAFITE,
                    ),
                ],
                spacing=20,
            ),
        ],
        spacing=20,
    )

    conteudo = ft.Container(
        expand=True,
        padding=35,
        content=ft.Column(
            controls=[
                cabecalho,

                ft.Container(height=20),

                boas_vindas,

                ft.Container(height=20),

                cards,
            ],
            spacing=15,
        ),
    )

    return ft.Row(
        controls=[
            menu,
            conteudo,
        ],
        spacing=0,
        expand=True,
    )
