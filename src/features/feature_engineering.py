"""Pipeline de generación de features a partir de datos crudos."""
import pandas as pd


def compute_features(df: pd.DataFrame, target_col: str = "prod_pet") -> pd.DataFrame:
    """Genera features por pozo a partir de la serie temporal de producción.
    Features generadas:
    - Lags: t-1, t-2, t-3
    - Rolling mean: ventanas de 3 y 6 meses
    - Rolling std: ventana de 3 meses
    - Ratios: gas/oil, water cut
    - Meses produciendo (conteo acumulado)
    """
    df = df.sort_values(["well_id", "fecha"]).copy()
    # Lags
    for lag in [1, 2, 3]:
        df[f"{target_col}_lag{lag}"] = df.groupby("well_id")[target_col].shift(lag)
    # Rolling statistics
    for window in [3, 6]:
        df[f"{target_col}_rolling_mean_{window}"] = df.groupby("well_id")[
            target_col
        ].transform(lambda x: x.rolling(window, min_periods=1).mean())
    df[f"{target_col}_rolling_std_3"] = df.groupby("well_id")[target_col].transform(
        lambda x: x.rolling(3, min_periods=1).std()
    )
    # Ratios
    df["gas_oil_ratio"] = df["prod_gas"] / df[target_col].replace(0, float("nan"))
    df["water_cut"] = df["prod_agua"] / (df[target_col] + df["prod_agua"]).replace(
        0, float("nan")
    )
    # Meses produciendo
    df["months_producing"] = df.groupby("well_id").cumcount() + 1
    # Eliminar filas con NaN por lags (primeros meses de cada pozo)
    df = df.dropna(subset=[f"{target_col}_lag3"])
    return df
