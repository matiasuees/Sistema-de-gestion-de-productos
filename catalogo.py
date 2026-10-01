from producto import Producto
import json
import os


class Catalogo:
    """Administra los productos utilizando list, dict y set."""

    def __init__(self):
        # LIST: almacena todos los productos
        self.productos = []

        # DICT: permite buscar rápidamente por código
        self.indice = {}

        # SET: evita códigos duplicados
        self.codigos = set()

        # Archivo donde se guardan los productos
        self.archivo = "productos.json"

        # Cargar productos guardados al iniciar
        self.cargar_productos()

    # =========================
    # PERSISTENCIA
    # =========================

    def guardar_productos(self):
        datos = []

        for producto in self.productos:
            datos.append({
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "precio": producto.precio
            })

        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def cargar_productos(self):
        if not os.path.exists(self.archivo):
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            for dato in datos:
                producto = Producto(
                    dato["codigo"],
                    dato["nombre"],
                    dato["precio"]
                )

                self.productos.append(producto)
                self.indice[producto.codigo] = producto
                self.codigos.add(producto.codigo)

        except (json.JSONDecodeError, KeyError, TypeError):
            self.productos = []
            self.indice = {}
            self.codigos = set()

    # =========================
    # CREATE
    # =========================

    def agregar(self, producto):
        if producto.codigo in self.codigos:
            return False, "Ya existe un producto con ese código."

        self.productos.append(producto)
        self.indice[producto.codigo] = producto
        self.codigos.add(producto.codigo)

        # Guardar automáticamente
        self.guardar_productos()

        return True, "Producto agregado correctamente."

    # =========================
    # READ
    # =========================

    def buscar(self, codigo):
        return self.indice.get(codigo)

    def listar(self):
        return self.productos.copy()

    # =========================
    # UPDATE
    # =========================

    def actualizar(self, codigo, nombre, precio):
        producto = self.buscar(codigo)

        if producto is None:
            return False, "No se encontró el producto."

        producto.actualizar(nombre, precio)

        # Guardar cambios
        self.guardar_productos()

        return True, "Producto actualizado correctamente."

    # =========================
    # DELETE
    # =========================

    def eliminar(self, codigo):
        producto = self.buscar(codigo)

        if producto is None:
            return False, "No se encontró el producto."

        self.productos.remove(producto)
        del self.indice[codigo]
        self.codigos.remove(codigo)

        # Guardar cambios
        self.guardar_productos()

        return True, "Producto eliminado correctamente."