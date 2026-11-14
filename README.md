# Gestión de Clientes

Formulario de escritorio con acceso a base de datos que permite **insertar, modificar, borrar y consultar** clientes.

## Tecnologías
- Python 3
- Tkinter (interfaz gráfica)
- SQL Server (base de datos) con `pyodbc`

## Campos
| Campo | Tipo en SQL Server |
|-------|------|
| id | INT IDENTITY (clave primaria) |
| nombre | NVARCHAR(50) |
| apellido | NVARCHAR(50) |
| edad | INT |
| telefono | NVARCHAR(20) |
| direccion | NVARCHAR(150) |

## Requisitos
1. Python 3 (https://www.python.org)
2. SQL Server (o SQL Server Express) instalado y en ejecución
3. ODBC Driver 17 o 18 for SQL Server
4. Instalar la librería:
   ```
   pip install -r requirements.txt
   ```

## Configuración
Abre `app.py` y ajusta al inicio las variables `SERVIDOR`, `DRIVER`, `USUARIO` y `CLAVE`
según tu instalación. La base de datos `GestionClientes` y la tabla `clientes`
se crean automáticamente al ejecutar (también está el script `schema.sql`).

## Ejecutar
```
python app.py
```

## Funciones
- **Guardar**: inserta un nuevo cliente.
- **Modificar**: selecciona un cliente en la tabla, edita los datos y presiona Modificar.
- **Eliminar**: selecciona un cliente en la tabla y presiona Eliminar.
- **Consultar**: la tabla muestra todos los clientes; el buscador filtra por nombre, apellido o teléfono.

## Uso de Inteligencia Artificial
Este proyecto se desarrolló con apoyo de Claude (Anthropic) para generar la estructura del código y las validaciones.

## Autor
Tu nombre aquí
