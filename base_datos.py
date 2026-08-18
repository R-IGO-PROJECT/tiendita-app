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

# Permite ejecutar la función directamente desde la terminal
if __name__ == "__main__":
    inicializar_base_datos()