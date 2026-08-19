import sqlite3

def inicializar_base_datos():
    # 1. Abrir/Crear la conexión con el archivo de la base de datos
    conexion = sqlite3.connect("tiendita.db")
    cursor = conexion.cursor()

    # 2. Habilitar la verificación de Claves Foráneas (FK)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 3. Crear tabla de Categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
    """)

    # 4. Crear tabla de Productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        );
    """)

    # 5. Guardar los cambios y cerrar
    conexion.commit()
    conexion.close()
    print("¡Base de datos y tablas creadas con éxito!")

def agregar_categoria(nombre):
    """Inserta una nueva categoría utilizando consultas parametrizadas (?)"""
    conexion = sqlite3.connect("tiendita.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
        conexion.commit()
        print(f"Categoría '{nombre}' agregada con éxito.")
    except sqlite3.IntegrityError:
        print(f"Error: La categoría '{nombre}' ya existe.")
    finally:
        conexion.close()

def agregar_producto(nombre, precio, stock, categoria_id):
    """Inserta un nuevo producto en el inventario"""
    conexion = sqlite3.connect("tiendita.db")
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    try:
        cursor.execute("""
            INSERT INTO productos (nombre, precio, stock, categoria_id)
            VALUES (?, ?, ?, ?)
        """, (nombre, precio, stock, categoria_id))
        conexion.commit()
        print(f"Producto '{nombre}' agregado correctamente.")
    except sqlite3.IntegrityError:
        print("Error: La categoría asignada no existe.")
    finally:
        conexion.close()

def obtener_productos():
    """Devuelve la lista de productos unida a sus nombres de categoría (JOIN)"""
    conexion = sqlite3.connect("tiendita.db")
    cursor = conexion.cursor()
    
    # Hacemos un JOIN para traer el nombre de la categoría en lugar de solo su ID
    cursor.execute("""
        SELECT p.id, p.nombre, p.precio, p.stock, c.nombre 
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
    """)
    productos = cursor.fetchall()
    conexion.close()
    return productos

# Permite ejecutar la función directamente desde la terminal
if __name__ == "__main__":
    inicializar_base_datos()