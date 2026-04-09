"""Definiciones de entidades y feature views para Feast.

Módulo canónico del lado Python (src/). Las definiciones aquí son
importadas por feature_store.py para registrarlas vía fs.apply().
"""
from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float64, Int64, String

# ---------------------------------------------------------------------------
# Entidad principal
# ---------------------------------------------------------------------------
well_entity = Entity(
    name="well_id",
    description="Identificador único del pozo (str(idpozo) según EDA)",
    value_type=String,
)

# ---------------------------------------------------------------------------
# Fuente offline: parquet generado por compute_features()
# La ruta es relativa al feast_repo_path que se pasa a FeatureStore()
# ---------------------------------------------------------------------------
well_features_source = FileSource(
    path="data/well_features.parquet",
    timestamp_field="fecha",
)

# ---------------------------------------------------------------------------
# Feature View: features generadas por compute_features(target_col="prod_pet")
# ---------------------------------------------------------------------------
well_features_view = FeatureView(
    name="well_features",
    entities=[well_entity],
    ttl=timedelta(days=365),
    schema=[
        # Lags del objetivo (prod_pet)
        Field(name="prod_pet_lag1", dtype=Float64),
        Field(name="prod_pet_lag2", dtype=Float64),
        Field(name="prod_pet_lag3", dtype=Float64),
        # Rolling statistics
        Field(name="prod_pet_rolling_mean_3", dtype=Float64),
        Field(name="prod_pet_rolling_mean_6", dtype=Float64),
        Field(name="prod_pet_rolling_std_3", dtype=Float64),
        # Ratios de producción
        Field(name="gas_oil_ratio", dtype=Float64),
        Field(name="water_cut", dtype=Float64),
        # Tiempo produciendo (siempre entero: cumcount + 1)
        Field(name="months_producing", dtype=Int64),
    ],
    source=well_features_source,
    online=True,
)
