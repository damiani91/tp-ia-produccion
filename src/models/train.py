"""Pipeline de entrenamiento con logging a MLflow."""

import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

import mlflow


def train_model(
    training_date: str,
    feast_repo_path: str = "feast_repo",
    mlflow_tracking_uri: str = "http://mlflow:5000",
    experiment_name: str = "well_production_forecast",
) -> str:
    """Entrena un modelo de forecasting para todos los pozos.
    Args:
        training_date: Fecha de corte (YYYY-MM-DD).
        feast_repo_path: Path al repo de Feast.
        mlflow_tracking_uri: URI del servidor MLflow.
        experiment_name: Nombre del experimento en MLflow.
    Returns:
        run_id de MLflow.
    """
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name)
    # 1. Leer offline features (parquet subyacente)
    df = pd.read_parquet(f"{feast_repo_path}/data/well_features.parquet")
    df = df[df["fecha"] <= pd.Timestamp(training_date)]
    # 2. Preparar X e y
    target_col = "prod_pet"

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
    df_clean = df.dropna(subset=feature_cols + [target_col])
    X = df_clean[feature_cols]
    y = df_clean[target_col]
    # 3. Time-series cross-validation split
    # Usar los últimos N meses como validación
    cutoff = pd.Timestamp(training_date) - pd.DateOffset(months=3)
    train_mask = df_clean["fecha"] <= cutoff
    val_mask = df_clean["fecha"] > cutoff
    X_train, X_val = X[train_mask], X[val_mask]
    y_train, y_val = y[train_mask], y[val_mask]
    # 4. Entrenar con MLflow tracking
    with mlflow.start_run() as run:
        # Log de parámetros
        params = {
            "model_type": "GradientBoostingRegressor",
            "n_estimators": 200,
            "max_depth": 5,
            "learning_rate": 0.1,
            "training_date": training_date,
            "n_wells_train": df_clean[train_mask]["well_id"].nunique(),
            "n_samples_train": len(X_train),
            "n_samples_val": len(X_val),
            "features": str(feature_cols),
        }
        mlflow.log_params(params)
        # Entrenamiento
        model = GradientBoostingRegressor(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            learning_rate=params["learning_rate"],
            random_state=42,
        )
        model.fit(X_train, y_train)
        # Predicciones
        y_train_pred = model.predict(X_train)
        y_val_pred = model.predict(X_val)
        # Métricas
        metrics = {
            "train_mae": mean_absolute_error(y_train, y_train_pred),
            "train_rmse": mean_squared_error(y_train, y_train_pred, squared=False),
            "val_mae": mean_absolute_error(y_val, y_val_pred),
            "val_rmse": mean_squared_error(y_val, y_val_pred, squared=False),
        }
        # MAPE (evitar div/0)
        nonzero = y_val != 0
        if nonzero.any():
            metrics["val_mape"] = (
                abs(y_val[nonzero] - y_val_pred[nonzero]) / y_val[nonzero]
            ).mean()
        mlflow.log_metrics(metrics)
        # Log del modelo
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="well_production_model",
        )
        # Artefactos: feature importances
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))
        importance = pd.Series(
            model.feature_importances_, index=feature_cols
        ).sort_values()
        importance.plot.barh(ax=ax)
        ax.set_title("Feature Importances")
        fig.tight_layout()
        fig.savefig("/tmp/feature_importances.png", dpi=100)
        mlflow.log_artifact("/tmp/feature_importances.png")
        plt.close()
        # Log dataset info como artefacto
        dataset_info = {
            "training_date": training_date,
            "n_wells": int(df_clean["well_id"].nunique()),
            "date_range": (
                f"{df_clean['fecha'].min()} " f"→ {df_clean['fecha'].max()}"
            ),
            "n_rows": len(df_clean),
        }
        mlflow.log_dict(dataset_info, "dataset_info.json")
        print(f"Run ID: {run.info.run_id}")
        print(f"Métricas: {metrics}")
        return run.info.run_id
