"""Definiciones de entidades y feature views para Feast (CLI feast apply).

Este archivo es equivalente a src/features/feature_definitions/wells_features.py
y debe mantenerse sincronizado con él. Se usa cuando se ejecuta `feast apply`
desde la línea de comandos en el directorio feast_repo/.
"""
from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float64, Int64, String

# Entidad principal
well_entity = Entity(
    name="well_id",
    description="Identificador único del pozo (str(idpozo) según EDA)",
    value_type=String,
)

# Source: archivo parquet con features computadas
well_features_source = FileSource(
    path="data/well_features.parquet",
    timestamp_field="fecha",
)

# Feature View
well_features_view = FeatureView(
    name="well_features",
    entities=[well_entity],
    ttl=timedelta(days=365),
    schema=[
        Field(name="prod_pet_lag1", dtype=Float64),
        Field(name="prod_pet_lag2", dtype=Float64),
        Field(name="prod_pet_lag3", dtype=Float64),
        Field(name="prod_pet_rolling_mean_3", dtype=Float64),
        Field(name="prod_pet_rolling_mean_6", dtype=Float64),
        Field(name="prod_pet_rolling_std_3", dtype=Float64),
        Field(name="gas_oil_ratio", dtype=Float64),
        Field(name="water_cut", dtype=Float64),
        Field(name="months_producing", dtype=Int64),
    ],
    source=well_features_source,
    online=True,
)
