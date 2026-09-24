class Producto:
    """Representa un producto del catálogo."""

    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    def actualizar(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.codigo} | {self.nombre} | ${self.precio:.2f}"