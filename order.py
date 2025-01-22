import flet as ft

def Order():
    # Daftar untuk menyimpan order
    orders = []
    total_payment_text = ft.Text(value="", size=16, weight=ft.FontWeight.BOLD, visible=False)
    bayar_button = ft.ElevatedButton(
        "Bayar",
        visible=False,
        on_click=lambda e: calculate_total_payment(e),
    )
    bayar_textfield = ft.TextField(
        label="Bayar",
        keyboard_type=ft.KeyboardType.NUMBER,
        visible=False,
    )
    kembalian_text = ft.Text(value="", size=16, visible=False)

    # Harga default untuk setiap produk
    product_prices = {
        "Nasi Goreng": 25000.0,
        "Mie Goreng": 20000.0,
        "Ayam Bakar": 30000.0,
        "Es Teh": 5000.0,
        "Jus Alpukat": 15000.0,
    }

    # Tabel untuk detail order
    order_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Product Name")),
            ft.DataColumn(ft.Text("Quantity")),
            ft.DataColumn(ft.Text("Price")),
            ft.DataColumn(ft.Text("Total")),
        ],
        rows=[],
        visible=False,
    )

    # Tabel untuk total pembayaran dan kembalian
    payment_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Total Payment")),
            ft.DataColumn(ft.Text("Kembalian")),
        ],
        rows=[],
        visible=False,
    )

    # Dropdown untuk pilihan produk
    product_dropdown = ft.Dropdown(
        label="Product Name",
        options=[ft.dropdown.Option("Nasi Goreng"),
                 ft.dropdown.Option("Mie Goreng"),
                 ft.dropdown.Option("Ayam Bakar"),
                 ft.dropdown.Option("Es Teh"),
                 ft.dropdown.Option("Jus Alpukat")],
        expand=True,
        on_change=lambda e: update_price_field(e),
    )

    # Fields untuk input quantity dan price
    quantity_field = ft.TextField(label="Quantity", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    price_field = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER, expand=True, read_only=True)

    def format_currency(value):
        return f"Rp. {int(value):,}".replace(",", ".")

    def update_price_field(e):
        # Update harga berdasarkan produk yang dipilih
        selected_product = product_dropdown.value
        if selected_product in product_prices:
            price_field.value = format_currency(product_prices[selected_product])
        else:
            price_field.value = ""
        e.page.update()

    def submit_order(e):
        try:
            # Ambil nilai dari input
            product_name = product_dropdown.value
            quantity = int(quantity_field.value or 0)
            price = product_prices.get(product_name, 0.0)

            if not product_name or quantity <= 0 or price <= 0:
                raise ValueError("Invalid input values")

            # Tambahkan ke daftar order
            total = quantity * price
            orders.append((product_name, quantity, price, total))

            # Tambahkan detail ke tabel order
            order_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(product_name)),
                    ft.DataCell(ft.Text(str(quantity))),
                    ft.DataCell(ft.Text(format_currency(price))),
                    ft.DataCell(ft.Text(format_currency(total))),
                ])
            )
            order_table.visible = True
            bayar_textfield.visible = True
            bayar_button.visible = True  
            total_payment_text.visible = False  

            # Reset input fields
            product_dropdown.value = None
            quantity_field.value = ""
            price_field.value = ""
            e.page.update()

        except ValueError:
            # Tampilkan error jika input tidak valid
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Please enter valid values for Product Name, Quantity, and Price."),
                open=True,
                bgcolor=ft.Colors.RED,
            )
            e.page.update()

    def calculate_total_payment(e):
        kembalian_text.visible = False
        total_payment = sum(order[3] for order in orders)

        try:
            amount_paid = float(bayar_textfield.value or 0)
            if amount_paid >= total_payment:
                change = amount_paid - total_payment
                # Update tabel pembayaran dengan total payment dan kembalian
                payment_table.rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(format_currency(total_payment))),
                        ft.DataCell(ft.Text(format_currency(change))),
                    ])
                ]
                payment_table.visible = True
                order_table.visible = False
                bayar_textfield.value = ""  
            else:
                kembalian_text.value = "Uang Tidak Cukup"
                kembalian_text.color = ft.Colors.RED
                kembalian_text.visible = True
                payment_table.visible = False  
                order_table.visible = True
                bayar_textfield.value = "" 

        except ValueError:
            payment_table.visible = False

        e.page.update()

    return ft.Column(
        controls=[
            ft.Text("This is the Order Page", size=20, weight=ft.FontWeight.BOLD),
            product_dropdown,
            quantity_field,
            price_field,
            ft.ElevatedButton("Submit Order", on_click=submit_order),
            order_table,
            bayar_textfield,
            kembalian_text,
            bayar_button,
            total_payment_text,
            payment_table, 
        ],
        spacing=16,
        alignment="center",
        horizontal_alignment="center",
    )
