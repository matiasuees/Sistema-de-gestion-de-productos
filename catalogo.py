from producto import Producto


class Catalogo:
    """Administra los productos utilizando list, dict y set."""

    def __init__(self):
        # LIST: almacena todos los productos
        self.productos = []

        # DICT: permite buscar rápidamente por código
        self.indice = {}

        # SET: evita códigos duplicados
        self.codigos = set()

    # CREATE
    def agregar(self, producto):
        if producto.codigo in self.codigos:
            return False, "Ya existe un producto con ese código."

        self.productos.append(producto)
        self.indice[producto.codigo] = producto
        self.codigos.add(producto.codigo)

        return True, "Producto agregado correctamente."

    # READ
    def buscar(self, codigo):
        return self.indice.get(codigo)

    def listar(self):
        return self.productos.copy()

    # UPDATE
    def actualizar(self, codigo, nombre, precio):
        producto = self.buscar(codigo)

        if producto is None:
            return False, "No se encontró el producto."

        producto.actualizar(nombre, precio)

        return True, "Producto actualizado correctamente."

    # DELETE
    def eliminar(self, codigo):
        producto = self.buscar(codigo)

        if producto is None:
            return False, "No se encontró el producto."

        self.productos.remove(producto)
        del self.indice[codigo]
        self.codigos.remove(codigo)

        return True, "Producto eliminado correctamente."