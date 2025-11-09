from datetime import datetime

class MetricaModelo:
    def __init__(self, model_type, r2_score_log, rmse_log, mae_log, r2_score_usd, rmse_usd, mae_usd, n_samples, features_used):
        self.timestamp = datetime.now()
        self.model_type = model_type
        self.r2_score_log = r2_score_log
        self.rmse_log = rmse_log
        self.mae_log = mae_log
        self.r2_score_usd = r2_score_usd
        self.rmse_usd = rmse_usd
        self.mae_usd = mae_usd
        self.n_samples = n_samples
        self.features_used = features_used

    def insertar_en_db(self, conn, tabla="model_metrics"):
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO {tabla} (
            timestamp, model_type, r2_score_log, rmse_log, mae_log,
            r2_score_usd, rmse_usd, mae_usd, n_samples, features_used
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.timestamp,
            self.model_type,
            self.r2_score_log,
            self.rmse_log,
            self.mae_log,
            self.r2_score_usd,
            self.rmse_usd,
            self.mae_usd,
            self.n_samples,
            self.features_used
        ))
        conn.commit()