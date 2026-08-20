import flet as ft

from app.screens.login import login_screen
from app.screens.dashboard import dashboard_screen
from app.screens.comparar import comparar_screen


def main(page: ft.Page):

    page.title = "Sheet Compare"
    page.bgcolor = "#F5F6F8"
    page.padding = 0

    page.window.width = 1100
    page.window.height = 700
    page.window.min_width = 900
    page.window.min_height = 600

    def mostrar_login():
        page.clean()
        page.add(login_screen(page, mostrar_dashboard))
        page.update()

    def mostrar_dashboard():
        page.clean()
        page.add(dashboard_screen(page, mostrar_comparar, mostrar_login))
        page.update()

    def mostrar_comparar():
        page.clean()
        page.add(comparar_screen(page, mostrar_dashboard))
        page.update()

    mostrar_login()


if __name__ == "__main__":
    ft.run(main)
