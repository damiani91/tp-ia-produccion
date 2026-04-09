"""Modelos de respuesta Pydantic para la API."""
from pydantic import BaseModel


class ForecastPoint(BaseModel):
    fecha: str
    prod: float


class ForecastResponse(BaseModel):
    well_id: str
    data: list[ForecastPoint]


class WellInfo(BaseModel):
    well_id: str
