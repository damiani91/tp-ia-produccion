"""Endpoint GET /api/v1/wells"""
import pandas as pd
from fastapi import APIRouter, Query, Request

from src.api.schemas import WellInfo

router = APIRouter()


@router.get("/wells", response_model=list[WellInfo])
def get_wells(
    request: Request,
    date_query: str = Query(..., description="Fecha para la cual se hace la consulta"),
):
    """Obtiene el listado de pozos con producción a la fecha indicada."""
    features_df = request.app.state.features_df
    cutoff = pd.Timestamp(date_query)
    # Pozos que tienen registros hasta la fecha consultada
    active_wells = features_df[features_df["fecha"] <= cutoff]["well_id"].unique()
    return [WellInfo(well_id=w) for w in sorted(active_wells)]
