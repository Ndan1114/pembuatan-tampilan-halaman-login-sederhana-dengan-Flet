import flet as ft

def Contact_us():
    # Daftar untuk menyimpan pesan
    messages = []
    message_details = ft.Column(controls=[], spacing=8, visible=False)

    # Fields untuk input
    name_field = ft.TextField(label="Nama", expand=True)
    phone_field = ft.TextField(label="No HP", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    message_field = ft.TextField(label="Pesan", expand=True)

    def submit_message(e):
        try:
            # Ambil nilai dari input
            name = name_field.value.strip()
            phone = phone_field.value.strip()
            message = message_field.value.strip()

            # Validasi input
            if not name or not phone or not message:
                raise ValueError("Semua field harus diisi.")

            if not phone.isdigit():
                raise ValueError("Nomor HP harus berupa angka.")

            # Tambahkan ke daftar pesan
            messages.append((name, phone, message))

            # Tambahkan detail ke kolom detail pesan
            message_details.controls.append(
                ft.Text(f"Nama: {name}, No HP: {phone}, Pesan: {message}")
            )
            message_details.visible = True

            # Reset input fields
            name_field.value = ""
            phone_field.value = ""
            message_field.value = ""
            e.page.update()

        except ValueError as err:
            # Tampilkan error jika input tidak valid
            e.page.snack_bar = ft.SnackBar(
                ft.Text(str(err)),
                open=True,
                bgcolor=ft.Colors.RED,
            )
            e.page.update()

    return ft.Column(
        controls=[
            ft.Text("Hubungi Kami", size=20, weight=ft.FontWeight.BOLD),
            name_field,
            phone_field,
            message_field,
            ft.ElevatedButton("Kirim Pesan", on_click=submit_message),
            message_details,
        ],
        spacing=16,
        alignment="center",
        horizontal_alignment="center",
    )

# # Jalankan aplikasi
# def main(page: ft.Page):
#     page.title = "Contact Us"
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#     page.scroll = ft.ScrollMode.AUTO
#     page.add(Contact_us())
