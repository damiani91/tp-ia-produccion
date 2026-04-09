"""Entry point de entrenamiento. Uso: python scripts/train.py --date 2024-01-01"""
import argparse

from src.features.feature_store import materialize_features
from src.models.train import train_model


def main():
    parser = argparse.ArgumentParser(description="Pipeline de entrenamiento")
    parser.add_argument(
        "--date",
        required=True,
        help="Fecha de corte para el entrenamiento (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--raw-data",
        default="data/raw/producciones.csv",
        help="Path al CSV de producción",
    )
    args = parser.parse_args()
    print(f"=== Materializando features hasta {args.date} ===")
    materialize_features(raw_data_path=args.raw_data, up_to_date=args.date)
    print(f"=== Entrenando modelo con datos hasta {args.date} ===")
    run_id = train_model(training_date=args.date)
    print(f"=== Entrenamiento completo. MLflow Run ID: {run_id} ===")


if __name__ == "__main__":
    main()
