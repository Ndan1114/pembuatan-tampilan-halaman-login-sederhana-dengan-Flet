import flet as ft
from home import Home
from order import Order
from oz import Contact_us
from login_form import Login


def main(page: ft.Page):
    # Fungsi untuk navigasi menu
    def select_menu(menu_item):
        if menu_item == "Home":
            main_content.content = Home()
        elif menu_item == "Order":
            main_content.content = Order()
        elif menu_item == "Contact_us":
            main_content.content = Contact_us()
        elif menu_item == "Logout":
            main_content.content = ft.Text("Your Session Finished")
            page.session.remove("is_logged_in")  # Hapus status login dari sesi
            page.session.remove("user_role")  
            update_ui()
        page.update()

    def handle_login(username):
        if username == "admin": 
            page.session.set("user_role", "2")
        elif username == "personal":
            page.session.set("user_role", "1")
        
        page.session.set("is_logged_in", True)
        update_ui()

    def update_ui():
        is_logged_in = page.session.get("is_logged_in") == True
        user_role = page.session.get("user_role")  

        # Update konten utama
        if is_logged_in:
            main_content.content = Home()
        else:
            main_content.content = Login(handle_login)

        nav_destinations = [
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="Home",
                disabled=not is_logged_in or user_role == "1",  
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SHOP,
                label="Order",
                disabled=not is_logged_in or user_role == "1",  
            ),
        ]

        if user_role == "1" or user_role == "2":
            nav_destinations.append(
                ft.NavigationBarDestination(
                    icon=ft.Icons.SHOP_2,
                    label="contact us",
                    disabled=not is_logged_in,
                )
            )

        # Tambahkan Log Out hanya jika sudah login
        if is_logged_in:
            nav_destinations.append(
                ft.NavigationBarDestination(
                    icon=ft.Icons.LOGOUT,
                    label="Log Out",
                )                
            )

        page.navigation_bar.destinations = nav_destinations
        page.update()

    # Periksa sesi login awal
    if not page.session.get("is_logged_in"):
        page.session.set("is_logged_in", False)

    page.appbar = ft.AppBar(
        leading=ft.Row(
            controls=[ft.Icon(ft.Icons.HOME), ft.Text("UNIBA STORE", weight=ft.FontWeight.BOLD)],
            alignment="start",
            spacing=8,
        ),
        center_title=False,
        bgcolor=ft.Colors.BLUE,
        automatically_imply_leading=False,
    )

    # Kontainer utama untuk konten
    main_content = ft.Container(expand=True)

    # Navigasi bar
    page.navigation_bar = ft.NavigationBar(destinations=[], selected_index=0)
    page.navigation_bar.on_change = lambda event: select_menu(
        ["Home", "Order", "Contact_us", "Logout"][event.control.selected_index]
    )

    # Tambahkan komponen ke halaman
    page.add(page.navigation_bar)
    page.add(main_content)

    # Perbarui UI pertama kali
    update_ui()

ft.app(main)