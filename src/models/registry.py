# src/models/registry.py
from typing import Optional

from mlflow.tracking import MlflowClient

import mlflow


def promote_model_to_production(
    model_name: str = "well_production_model",
    run_id: Optional[str] = None,
    mlflow_tracking_uri: str = "http://mlflow:5000",
) -> None:
    """Promueve la última versión (o una específica) del modelo a Production."""
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    client = MlflowClient()
    if run_id:
        # Buscar la versión del modelo asociada a este run
        versions = client.search_model_versions(f"name='{model_name}'")
        target = [v for v in versions if v.run_id == run_id]
        if not target:
            raise ValueError(f"No se encontró versión para run_id={run_id}")
        version = target[0].version
    else:
        # Usar la última versión
        versions = client.get_latest_versions(model_name)
        version = versions[-1].version
    # Transicionar a Production
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production",
        archive_existing_versions=True,
    )
    print(f"Modelo {model_name} v{version} → Production")
