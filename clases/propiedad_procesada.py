# Clase para representar una propiedad preprocesada y guardar en la base de datos
import sqlite3

class PropiedadPreprocesada:
    def __init__(self, **kwargs):
        """
        Inicializa una nueva instancia de PropiedadPreprocesada.
        Args:
            **kwargs: Diccionario de atributos y valores para la propiedad.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def insertar_en_db(self, conn, tabla="entrenamiento_preprocesado"):
        """
        Inserta la instancia actual en la base de datos.
        Args:
            conn: Conexión a la base de datos SQLite
            tabla: Nombre de la tabla donde insertar los datos
        """
        # Escapar los nombres de las columnas con comillas dobles
        columnas = ', '.join(f'"{k}"' for k in self.__dict__.keys())
        valores = tuple(self.__dict__.values())
        placeholders = ', '.join(['?'] * len(valores))
        sql = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
        conn.execute(sql, valores)