"""Endpoint GET /api/v1/forecast"""
from fastapi import APIRouter, Query, Request

from src.api.schemas import ForecastResponse

router = APIRouter()


@router.get("/forecast", response_model=ForecastResponse)
def get_forecast(
    request: Request,
    well_id: str = Query(..., description="Identificador del pozo"),
    date_start: str = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    date_end: str = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
):
    """Obtiene el pronóstico de producción de un pozo."""
    service = request.app.state.forecast_service
    features_df = request.app.state.features_df
    data = service.predict(
        well_id=well_id,
        date_start=date_start,
        date_end=date_end,
        features_df=features_df,
    )
    return ForecastResponse(well_id=well_id, data=data)
