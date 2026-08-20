import flet as ft


AMARELO = "#F5C518"
GRAFITE = "#1E2329"
FUNDO = "#F5F6F8"
CINZA = "#666666"
VERMELHO = "#D64545"


def login_screen(page: ft.Page, ir_dashboard):

    usuario = ft.TextField(
        label="Usuário",
        width=320,
        border_color=GRAFITE,
        focused_border_color=AMARELO,
    )

    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=320,
        border_color=GRAFITE,
        focused_border_color=AMARELO,
    )

    mensagem_erro = ft.Text(
        "Usuário ou senha incorretos.",
        color=VERMELHO,
        size=13,
        visible=False,
    )

    def entrar(e):

        if usuario.value == "admin" and senha.value == "1234":
            ir_dashboard()
        else:
            mensagem_erro.visible = True
            page.update()

    botao_entrar = ft.Button(
        content="ENTRAR",
        width=320,
        height=50,
        bgcolor=AMARELO,
        color=GRAFITE,
        on_click=entrar,
    )

    conteudo = ft.Column(
        controls=[
            ft.Text(
                "SHEET COMPARE",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=GRAFITE,
            ),

            ft.Text(
                "Comparação e organização de planilhas",
                size=14,
                color=CINZA,
            ),

            ft.Container(height=30),

            usuario,
            senha,

            mensagem_erro,

            ft.Container(height=10),

            botao_entrar,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    return ft.Container(
        content=conteudo,
        alignment=ft.Alignment.CENTER,
        expand=True,
        bgcolor=FUNDO,
    )
