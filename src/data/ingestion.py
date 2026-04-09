import pandas as pd


def load_production_data(raw_data_path: str) -> pd.DataFrame:
    """
    Carga los datos crudos de producción y retorna un DataFrame
    con las columnas esperadas: well_id, fecha, prod_pet,
    prod_gas, prod_agua.

    Según el dataset original, las columnas pueden llamarse
    'idpozo', 'fecha', 'prod_pet', 'prod_gas', 'prod_agua'.
    Se renombrará 'idpozo' a 'well_id' para mantener
    consistencia con el feature store.
    """
    df = pd.read_csv(raw_data_path)

    # Renombrar idpozo a well_id si existe, según lo dice el EDA y la entidad de Feast
    if "idpozo" in df.columns:
        df = df.rename(columns={"idpozo": "well_id"})

    # Asegurar que 'well_id' sea string ya que Feast Entity es String
    if "well_id" in df.columns:
        df["well_id"] = df["well_id"].astype(str)

    # Convertir 'fecha' a datetime
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])

    # Filtrar solo las columnas necesarias
    cols = ["well_id", "fecha", "prod_pet", "prod_gas", "prod_agua"]
    # Mantener solo las columnas especificadas que realmente existan en el CSV
    cols_existentes = [col for col in cols if col in df.columns]

    return df[cols_existentes]
