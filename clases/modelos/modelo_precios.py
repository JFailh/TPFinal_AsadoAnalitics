import sqlite3
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
from .metrica_modelo import MetricaModelo
from .prediccion_modelo import PrediccionModelo

class ModeloPrecios:
    def __init__(self, pipeline, model_type="LinearRegression"):
        self.pipeline = pipeline
        self.model_type = model_type
        
    def crear_tablas(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla para métricas del modelo (ahora incluye MAE)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            model_type TEXT,
            r2_score_log REAL,
            rmse_log REAL,
            mae_log REAL,
            r2_score_usd REAL,
            rmse_usd REAL,
            mae_usd REAL,
            n_samples INTEGER,
            features_used TEXT
        )
        ''')

        # Crear tabla para predicciones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            real_price REAL,
            predicted_price REAL,
            error_percentage REAL,
            property_id INTEGER
        )
        ''')

        conn.commit()
        conn.close()

    def evaluar_y_guardar(self, X_test, y_test, features_used, db_path, max_predictions=100):
        # Hacer predicciones
        y_pred = self.pipeline.predict(X_test)
        
        # Convertir predicciones de log a valores reales
        y_test_real = np.expm1(y_test)
        y_pred_real = np.expm1(y_pred)
        
        # Calcular métricas (incluyendo MAE)
        from sklearn.metrics import mean_absolute_error
        mae_log = mean_absolute_error(y_test, y_pred)
        mae_usd = mean_absolute_error(y_test_real, y_pred_real)

        metrica = MetricaModelo(
            model_type=self.model_type,
            r2_score_log=r2_score(y_test, y_pred),
            rmse_log=np.sqrt(mean_squared_error(y_test, y_pred)),
            mae_log=mae_log,
            r2_score_usd=r2_score(y_test_real, y_pred_real),
            rmse_usd=np.sqrt(mean_squared_error(y_test_real, y_pred_real)),
            mae_usd=mae_usd,
            n_samples=len(y_test),
            features_used=features_used
        )
        
        # Guardar en base de datos
        conn = sqlite3.connect(db_path)
        
        try:
            # Guardar métricas
            metrica.insertar_en_db(conn)
            
            # Guardar predicciones
            for real, pred in zip(y_test_real[:max_predictions], y_pred_real[:max_predictions]):
                prediccion = PrediccionModelo(real, pred)
                prediccion.insertar_en_db(conn)
                
            print("Resultados guardados exitosamente en la base de datos.")
            
        except Exception as e:
            print(f"Error al guardar en la base de datos: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
            
        return metrica