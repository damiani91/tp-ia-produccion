# src/models/predict.py
import pandas as pd

import mlflow


class ForecastService:
    """Servicio de inferencia que carga el modelo productivo desde MLflow."""

    def __init__(
        self,
        model_name: str = "well_production_model",
        mlflow_tracking_uri: str = "http://mlflow:5000",
    ):
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        self.model_name = model_name
        self.model = None
        self._load_production_model()

    def _load_production_model(self):
        """Carga el modelo en stage 'Production' desde el registry."""
        model_uri = f"models:/{self.model_name}/Production"
        self.model = mlflow.sklearn.load_model(model_uri)
        print(f"Modelo cargado: {model_uri}")

    def predict(
        self,
        well_id: str,
        date_start: str,
        date_end: str,
        features_df: pd.DataFrame,
    ) -> list[dict]:
        """Genera pronóstico para un pozo en un rango de fechas.
        Para simplificar, se genera un forecast iterativo:
        se predice mes a mes, usando la predicción anterior como input
        para el lag siguiente (auto-regresivo).
        """
        # Filtrar features del pozo
        well_data = features_df[features_df["well_id"] == well_id].copy()
        well_data = well_data.sort_values("fecha")
        # Generar rango de fechas
        dates = pd.date_range(start=date_start, end=date_end, freq="MS")
        results = []

        for target_date in dates:
            # Si tenemos datos reales, usamos esos features
            # Si no, hacemos forecast autoregresivo
            row = well_data[well_data["fecha"] == target_date]
            if not row.empty:
                feature_cols = [
                    "prod_pet_lag1",
                    "prod_pet_lag2",
                    "prod_pet_lag3",
                    "prod_pet_rolling_mean_3",
                    "prod_pet_rolling_mean_6",
                    "prod_pet_rolling_std_3",
                    "gas_oil_ratio",
                    "water_cut",
                    "months_producing",
                ]
                X = row[feature_cols]
                pred = float(self.model.predict(X)[0])
            else:
                # Forecast autoregresivo simplificado:
                # usar última fila conocida, desplazando lags
                pred = self._autoregressive_predict(well_data, target_date)

            results.append(
                {
                    "fecha": target_date.strftime("%Y-%m-%d"),
                    "prod": round(max(pred, 0), 2),  # producción no puede ser negativa
                }
            )
        return results

    def _autoregressive_predict(
        self, well_data: pd.DataFrame, target_date: pd.Timestamp
    ) -> float:
        """Predicción autoregresiva simple cuando no hay features materializadas."""
        # Implementar lógica de shift de lags con predicciones previas
        # (simplificación para el TP)
        if well_data.empty:
            return 0.0
        last = well_data.iloc[-1]
        # Usar las features de la última fila conocida como proxy
        feature_cols = [
            "prod_pet_lag1",
            "prod_pet_lag2",
            "prod_pet_lag3",
            "prod_pet_rolling_mean_3",
            "prod_pet_rolling_mean_6",
            "prod_pet_rolling_std_3",
            "gas_oil_ratio",
            "water_cut",
            "months_producing",
        ]
        X = pd.DataFrame([last[feature_cols].values], columns=feature_cols)
        return float(self.model.predict(X)[0])
