from datetime import datetime

class PrediccionModelo:
    def __init__(self, real_price, predicted_price):
        self.timestamp = datetime.now()
        self.real_price = float(real_price)
        self.predicted_price = float(predicted_price)
        self.error_percentage = ((self.predicted_price - self.real_price) / self.real_price) * 100

    def insertar_en_db(self, conn, tabla="model_predictions"):
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO {tabla} (
            timestamp, real_price, predicted_price, error_percentage
        ) VALUES (?, ?, ?, ?)
        ''', (
            self.timestamp,
            self.real_price,
            self.predicted_price,
            self.error_percentage
        ))
        conn.commit()