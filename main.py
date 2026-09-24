import flet as ft
from producto import Producto
from catalogo import Catalogo


def main(page: ft.Page):

    # --------------------------------------------------
    # CONFIGURACIÓN DE LA VENTANA
    # --------------------------------------------------

    page.title = "Catálogo de Productos - Semanas 5 y 6"
    page.window_width = 900
    page.window_height = 700
    page.padding = 25
    page.theme_mode = ft.ThemeMode.LIGHT

    # Crear catálogo
    catalogo = Catalogo()

    # --------------------------------------------------
    # CAMPOS DE ENTRADA
    # --------------------------------------------------

    codigo = ft.TextField(
        label="Código",
        hint_text="Ej.: P001",
        width=180
    )

    nombre = ft.TextField(
        label="Nombre",
        hint_text="Ej.: Laptop",
        width=250
    )

    precio = ft.TextField(
        label="Precio",
        hint_text="Ej.: 899.99",
        width=180
    )

    # Mensaje para el usuario
    mensaje = ft.Text(size=15)

    # --------------------------------------------------
    # TABLA
    # --------------------------------------------------

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Precio")),
        ],
        rows=[]
    )

    # --------------------------------------------------
    # MOSTRAR MENSAJES
    # --------------------------------------------------

    def mostrar_mensaje(texto, correcto=True):

        mensaje.value = texto

        if correcto:
            mensaje.color = ft.Colors.GREEN
        else:
            mensaje.color = ft.Colors.RED

        page.update()

    # --------------------------------------------------
    # VALIDAR DATOS
    # --------------------------------------------------

    def validar_datos():

        cod = codigo.value.strip().upper()
        nom = nombre.value.strip()
        pre = precio.value.strip().replace(",", ".")

        # Validar código
        if not cod:
            mostrar_mensaje(
                "Ingrese un código.",
                False
            )
            return None

        # Validar nombre
        if not nom:
            mostrar_mensaje(
                "Ingrese el nombre del producto.",
                False
            )
            return None

        # Validar precio
        try:
            valor = float(pre)
        except ValueError:
            mostrar_mensaje(
                "El precio debe ser numérico.",
                False
            )
            return None

        # Validar precio positivo
        if valor <= 0:
            mostrar_mensaje(
                "El precio debe ser mayor que 0.",
                False
            )
            return None

        return cod, nom, valor

    # --------------------------------------------------
    # ACTUALIZAR TABLA
    # --------------------------------------------------

    def refrescar_tabla():

        tabla.rows = []

        for producto in catalogo.listar():

            fila = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(producto.codigo)
                    ),
                    ft.DataCell(
                        ft.Text(producto.nombre)
                    ),
                    ft.DataCell(
                        ft.Text(
                            f"${producto.precio:.2f}"
                        )
                    ),
                ]
            )

            tabla.rows.append(fila)

        page.update()

    # --------------------------------------------------
    # LIMPIAR CAMPOS
    # --------------------------------------------------

    def limpiar_campos(e=None):

        codigo.value = ""
        nombre.value = ""
        precio.value = ""
        mensaje.value = ""

        page.update()

    # --------------------------------------------------
    # AGREGAR PRODUCTO
    # --------------------------------------------------

    def agregar(e):

        datos = validar_datos()

        if datos is None:
            return

        cod, nom, valor = datos

        producto = Producto(
            cod,
            nom,
            valor
        )

        exito, texto = catalogo.agregar(producto)

        mostrar_mensaje(
            texto,
            exito
        )

        if exito:
            refrescar_tabla()
            limpiar_campos()

    # --------------------------------------------------
    # BUSCAR PRODUCTO
    # --------------------------------------------------

    def buscar(e):

        cod = codigo.value.strip().upper()

        if not cod:
            mostrar_mensaje(
                "Ingrese un código para buscar.",
                False
            )
            return

        producto = catalogo.buscar(cod)

        if producto is None:

            mostrar_mensaje(
                "Producto no encontrado.",
                False
            )

            return

        nombre.value = producto.nombre
        precio.value = f"{producto.precio:.2f}"

        mostrar_mensaje(
            "Producto encontrado correctamente.",
            True
        )

    # --------------------------------------------------
    # ACTUALIZAR PRODUCTO
    # --------------------------------------------------

    def actualizar(e):

        cod = codigo.value.strip().upper()
        nom = nombre.value.strip()
        pre = precio.value.strip().replace(",", ".")

        if not cod:
            mostrar_mensaje(
                "Ingrese el código del producto.",
                False
            )
            return

        if not nom:
            mostrar_mensaje(
                "Ingrese el nombre del producto.",
                False
            )
            return

        try:
            valor = float(pre)

        except ValueError:
            mostrar_mensaje(
                "El precio debe ser numérico.",
                False
            )
            return

        if valor <= 0:
            mostrar_mensaje(
                "El precio debe ser mayor que 0.",
                False
            )
            return

        exito, texto = catalogo.actualizar(
            cod,
            nom,
            valor
        )

        mostrar_mensaje(
            texto,
            exito
        )

        if exito:
            refrescar_tabla()
            limpiar_campos()

    # --------------------------------------------------
    # ELIMINAR PRODUCTO
    # --------------------------------------------------

    def eliminar(e):

        cod = codigo.value.strip().upper()

        if not cod:
            mostrar_mensaje(
                "Ingrese el código del producto.",
                False
            )
            return

        exito, texto = catalogo.eliminar(cod)

        mostrar_mensaje(
            texto,
            exito
        )

        if exito:
            refrescar_tabla()
            limpiar_campos()

    # --------------------------------------------------
    # DATOS DE PRUEBA
    # --------------------------------------------------

    def cargar_prueba(e):

        datos = [
            ("P001", "Laptop", 899.99),
            ("P002", "Mouse inalámbrico", 25.50),
            ("P003", "Teclado mecánico", 65.00)
        ]

        agregados = 0

        for cod, nom, valor in datos:

            producto = Producto(
                cod,
                nom,
                valor
            )

            exito, _ = catalogo.agregar(producto)

            if exito:
                agregados += 1

        refrescar_tabla()

        mostrar_mensaje(
            f"Se agregaron {agregados} productos de prueba.",
            True
        )

    # --------------------------------------------------
    # TÍTULOS
    # --------------------------------------------------

    titulo = ft.Text(
        "CATÁLOGO DE PRODUCTOS",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text(
        "Semanas 5 y 6 - Colecciones, CRUD, "
        "Flet y manejo de eventos",
        size=15
    )

    # --------------------------------------------------
    # BOTONES
    # --------------------------------------------------

    botones = ft.Row(
        controls=[

            ft.ElevatedButton(
                "Agregar",
                icon=ft.Icons.ADD,
                on_click=agregar
            ),

            ft.ElevatedButton(
                "Buscar",
                icon=ft.Icons.SEARCH,
                on_click=buscar
            ),

            ft.ElevatedButton(
                "Actualizar",
                icon=ft.Icons.EDIT,
                on_click=actualizar
            ),

            ft.ElevatedButton(
                "Eliminar",
                icon=ft.Icons.DELETE,
                on_click=eliminar
            ),

            ft.OutlinedButton(
                "Limpiar",
                icon=ft.Icons.CLEAR,
                on_click=limpiar_campos
            ),

            ft.OutlinedButton(
                "Datos de prueba",
                on_click=cargar_prueba
            )
        ],

        wrap=True
    )

    # --------------------------------------------------
    # INTERFAZ
    # --------------------------------------------------

    page.add(

        titulo,

        subtitulo,

        ft.Divider(),

        ft.Row(
            [
                codigo,
                nombre,
                precio
            ],
            wrap=True
        ),

        botones,

        mensaje,

        ft.Divider(),

        ft.Text(
            "Productos registrados",
            size=20,
            weight=ft.FontWeight.BOLD
        ),

        ft.Column(
            [tabla],
            scroll=ft.ScrollMode.AUTO
        )
    )


# --------------------------------------------------
# EJECUTAR APLICACIÓN
# --------------------------------------------------

if __name__ == "__main__":
    ft.app(target=main)