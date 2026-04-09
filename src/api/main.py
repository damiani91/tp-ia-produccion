"""Aplicación FastAPI — API REST de pronóstico de producción de pozos."""
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI

from src.api.routes import forecast, wells
from src.models.predict import ForecastService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el modelo productivo al iniciar la app."""
    app.state.forecast_service = ForecastService()
    # Cargar features para serving
    app.state.features_df = pd.read_parquet("feast_repo/data/well_features.parquet")
    yield


app = FastAPI(
    title="Oil & Gas Forecast API",
    version="1.0.0",
    description=(
        "API simple para consultar el listado de pozos y sus "
        "pronósticos de producción."
    ),
    lifespan=lifespan,
)
app.include_router(forecast.router, prefix="/api/v1")
app.include_router(wells.router, prefix="/api/v1")
