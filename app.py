"""
Formulario de Clientes - CRUD con Tkinter y SQL Server
Campos: nombre, apellido, edad, teléfono, dirección
Jesus Encarnacion 100590273
"""

import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox


SERVIDOR = r"DESKTOP-G3TEB62\MOISES"     
BASE_DATOS = "GestionClientes"
DRIVER = "ODBC Driver 17 for SQL Server"  
USUARIO = None
CLAVE = None


# ---------------------------------------------------------------
# BASE DE DATOS
# ---------------------------------------------------------------
def cadena_conexion(base):
    cadena = f"DRIVER={{{DRIVER}}};SERVER={SERVIDOR};DATABASE={base};TrustServerCertificate=yes;"
    if USUARIO and CLAVE:
        cadena += f"UID={USUARIO};PWD={CLAVE};"
    else:
        cadena += "Trusted_Connection=yes;"
    return cadena


def conectar():
    return pyodbc.connect(cadena_conexion(BASE_DATOS))


def crear_base_y_tabla():
    """Crea la base de datos y la tabla si todavía no existen."""
    con = pyodbc.connect(cadena_conexion("master"), autocommit=True)
    con.execute(f"IF DB_ID('{BASE_DATOS}') IS NULL CREATE DATABASE {BASE_DATOS}")
    con.close()

    with conectar() as con:
        con.execute(
            """
            IF OBJECT_ID('clientes', 'U') IS NULL
            CREATE TABLE clientes (
                id INT IDENTITY(1,1) PRIMARY KEY,
                nombre NVARCHAR(50) NOT NULL,
                apellido NVARCHAR(50) NOT NULL,
                edad INT NOT NULL,
                telefono NVARCHAR(20) NOT NULL,
                direccion NVARCHAR(150) NOT NULL
            )
            """
        )


def insertar_cliente(nombre, apellido, edad, telefono, direccion):
    with conectar() as con:
        con.execute(
            "INSERT INTO clientes (nombre, apellido, edad, telefono, direccion) "
            "VALUES (?, ?, ?, ?, ?)",
            (nombre, apellido, edad, telefono, direccion),
        )


def modificar_cliente(id_cliente, nombre, apellido, edad, telefono, direccion):
    with conectar() as con:
        con.execute(
            "UPDATE clientes SET nombre=?, apellido=?, edad=?, telefono=?, direccion=? "
            "WHERE id=?",
            (nombre, apellido, edad, telefono, direccion, id_cliente),
        )


def borrar_cliente(id_cliente):
    with conectar() as con:
        con.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))


def consultar_clientes(filtro=""):
    with conectar() as con:
        like = f"%{filtro}%"
        cur = con.execute(
            "SELECT id, nombre, apellido, edad, telefono, direccion FROM clientes "
            "WHERE nombre LIKE ? OR apellido LIKE ? OR telefono LIKE ? "
            "ORDER BY id DESC",
            (like, like, like),
        )
        return [tuple(fila) for fila in cur.fetchall()]


# ---------------------------------------------------------------
# INTERFAZ (FORMULARIO)
# ---------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Clientes")
        self.geometry("760x520")
        self.resizable(False, False)

        self.id_seleccionado = None  # id del cliente que se está editando

        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_edad = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_direccion = tk.StringVar()
        self.var_buscar = tk.StringVar()

        self.crear_formulario()
        self.crear_tabla_visual()
        self.cargar_tabla()

    # ----- Formulario -----
    def crear_formulario(self):
        marco = ttk.LabelFrame(self, text="Datos del cliente", padding=10)
        marco.pack(fill="x", padx=10, pady=10)

        campos = [
            ("Nombre:", self.var_nombre),
            ("Apellido:", self.var_apellido),
            ("Edad:", self.var_edad),
            ("Teléfono:", self.var_telefono),
            ("Dirección:", self.var_direccion),
        ]
        for fila, (texto, variable) in enumerate(campos):
            ttk.Label(marco, text=texto).grid(row=fila, column=0, sticky="w", pady=3)
            ttk.Entry(marco, textvariable=variable, width=50).grid(
                row=fila, column=1, padx=10, pady=3, sticky="w"
            )

        botones = ttk.Frame(marco)
        botones.grid(row=0, column=2, rowspan=5, padx=20)
        ttk.Button(botones, text="Guardar", width=14, command=self.guardar).pack(pady=3)
        ttk.Button(botones, text="Modificar", width=14, command=self.modificar).pack(pady=3)
        ttk.Button(botones, text="Eliminar", width=14, command=self.eliminar).pack(pady=3)
        ttk.Button(botones, text="Limpiar", width=14, command=self.limpiar).pack(pady=3)

    # ----- Tabla de consulta -----
    def crear_tabla_visual(self):
        marco = ttk.LabelFrame(self, text="Clientes registrados", padding=10)
        marco.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        buscador = ttk.Frame(marco)
        buscador.pack(fill="x", pady=(0, 8))
        ttk.Label(buscador, text="Buscar:").pack(side="left")
        entrada = ttk.Entry(buscador, textvariable=self.var_buscar, width=30)
        entrada.pack(side="left", padx=8)
        entrada.bind("<KeyRelease>", lambda e: self.cargar_tabla())

        columnas = ("id", "nombre", "apellido", "edad", "telefono", "direccion")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=10)
        anchos = (40, 110, 110, 50, 110, 250)
        for col, ancho in zip(columnas, anchos):
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=ancho, anchor="w")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    # ----- Utilidades -----
    def cargar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for cliente in consultar_clientes(self.var_buscar.get().strip()):
            self.tabla.insert("", "end", values=cliente)

    def limpiar(self):
        self.id_seleccionado = None
        for v in (self.var_nombre, self.var_apellido, self.var_edad,
                  self.var_telefono, self.var_direccion):
            v.set("")
        self.tabla.selection_remove(self.tabla.selection())

    def obtener_datos(self):
        """Valida y devuelve los datos del formulario, o None si hay error."""
        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        edad = self.var_edad.get().strip()
        telefono = self.var_telefono.get().strip()
        direccion = self.var_direccion.get().strip()

        if not all([nombre, apellido, edad, telefono, direccion]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return None
        if not edad.isdigit() or not (0 < int(edad) < 120):
            messagebox.showwarning("Edad inválida", "La edad debe ser un número entre 1 y 119.")
            return None
        if not telefono.replace("-", "").replace(" ", "").isdigit():
            messagebox.showwarning("Teléfono inválido", "El teléfono solo debe tener números.")
            return None
        return nombre, apellido, int(edad), telefono, direccion

    # ----- Acciones -----
    def guardar(self):
        datos = self.obtener_datos()
        if datos:
            insertar_cliente(*datos)
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            self.limpiar()
            self.cargar_tabla()

    def seleccionar(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        self.id_seleccionado = valores[0]
        self.var_nombre.set(valores[1])
        self.var_apellido.set(valores[2])
        self.var_edad.set(valores[3])
        self.var_telefono.set(valores[4])
        self.var_direccion.set(valores[5])

    def modificar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla primero.")
            return
        datos = self.obtener_datos()
        if datos:
            modificar_cliente(self.id_seleccionado, *datos)
            messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
            self.limpiar()
            self.cargar_tabla()

    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Atención", "Selecciona un cliente de la tabla primero.")
            return
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este cliente?"):
            borrar_cliente(self.id_seleccionado)
            self.limpiar()
            self.cargar_tabla()


if __name__ == "__main__":
    try:
        crear_base_y_tabla()
    except pyodbc.Error as error:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error de conexión",
            "No se pudo conectar a SQL Server.\n"
            "Revisa SERVIDOR y DRIVER al inicio de app.py.\n\n" + str(error),
        )
        raise SystemExit(1)
    App().mainloop()
