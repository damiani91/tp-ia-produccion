"""Script para materializar features en el feature store."""
# src/features/feature_store.py
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from feast import FeatureStore

from src.data.ingestion import load_production_data
from src.features.feature_definitions.wells_features import (
    well_entity,
    well_features_source,
    well_features_view,
)
from src.features.feature_engineering import compute_features


def materialize_features(
    raw_data_path: str,
    feast_repo_path: str = "feast_repo",
    output_parquet: str = "feast_repo/data/well_features.parquet",
    up_to_date: Optional[str] = None,
) -> None:
    """Pipeline completo: raw data → features → materialización en Feast."""
    # 1. Cargar datos crudos
    df = load_production_data(raw_data_path)
    # 2. Filtrar hasta la fecha indicada (simula "no tener datos del futuro")
    if up_to_date:
        df = df[df["fecha"] <= pd.Timestamp(up_to_date)]
    # 3. Computar features
    df_features = compute_features(df)
    # 4. Guardar como parquet (source para Feast)
    Path(output_parquet).parent.mkdir(parents=True, exist_ok=True)
    df_features.to_parquet(output_parquet, index=False)
    # 5. Registrar definiciones en Feast (entidad + source + feature view)
    fs = FeatureStore(repo_path=feast_repo_path)
    fs.apply([well_entity, well_features_source, well_features_view])
    # 6. Materializar para online store
    if up_to_date:
        end_date = datetime.fromisoformat(up_to_date)
    else:
        end_date = datetime.now()
    fs.materialize_incremental(end_date=end_date)
    print(f"Features materializadas hasta {end_date}")
