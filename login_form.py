import flet as ft

def Login(on_login):
    username_field = ft.TextField(label="Username", expand=True)
    password_field = ft.TextField(label="Password", password=True, expand=True)
    error_message = ft.Text(visible=False, color=ft.Colors.RED)

    # Menambahkan data password yang benar untuk setiap user
    akun = {
        "admin": "2",  
        "personal": "1",
    }

    def handle_login(e):
        if username_field.value == "" or password_field.value == "":
            error_message.value = "Masukan Akun Anda!"
            error_message.visible = True
        elif username_field.value in akun and password_field.value == akun[username_field.value]:
            on_login(username_field.value)
            error_message.visible = False
        else:
            error_message.value = "Masukan Username/Kata Sandi Yang Benar!"
            error_message.visible = True
        e.page.update()

    def kel(e):
        e.page.window_close()

    return ft.Column(
        controls=[
            ft.Text(
                "Login Page", 
                size=24, 
                weight=ft.FontWeight.BOLD, 
                text_align="center"
            ),
            ft.Container(
                content=username_field,
                padding=ft.Padding(0, 8, 0, 8),  # Jarak atas dan bawah
            ),
            ft.Container(
                content=password_field,
                padding=ft.Padding(0, 8, 0, 8),  # Jarak atas dan bawah
            ),
            ft.Container(
                content=error_message,
                padding=ft.Padding(0, 8, 0, 16),  # Jarak bawah lebih besar untuk tombol
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Login",
                        on_click=handle_login,
                        style=ft.ButtonStyle(
                            padding=ft.Padding(12, 16, 12, 16),
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                    ft.ElevatedButton(
                        "Exit", 
                        on_click=kel,
                        style=ft.ButtonStyle(
                            padding=ft.Padding(12, 16, 12, 16),
                            shape=ft.RoundedRectangleBorder(radius=8),
                            bgcolor=ft.Colors.RED,  # Background merah
                            color=ft.Colors.WHITE,  # Warna teks putih
                        ),
                    ),
                ],
                alignment="center",  # Mengatur tombol agar berada di tengah
                spacing=16,  # Jarak antar tombol
            ),
        ],
        spacing=8,  # Jarak antar elemen dalam kolom
        alignment="center",
        horizontal_alignment="center",
        expand=True,
    )
