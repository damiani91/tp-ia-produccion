# TP IA en Producción

Sistema completo de ML en producción para pronóstico de pozos, incluyendo feature engineering, training, serving y monitoring.

## Arquitectura

- **Data**: Ingestion y validación de datos
- **Features**: Feast para feature store
- **Models**: Entrenamiento y registry con MLflow
- **API**: FastAPI para servir predicciones
- **Orchestration**: Airflow para DAGs de training y monitoring
- **Serving**: Ray Serve para inference
- **Monitoring**: Evidently para drift detection

## Estructura del Proyecto

```
tp-ia-produccion/
├── data/              # Datos crudos y scripts de descarga
├── src/               # Código principal
├── tests/             # Tests unitarios e integración
├── notebooks/         # EDA y prototipado
├── configs/           # Archivos de configuración
├── feast_repo/        # Feature store definitions
├── docker/            # Dockerfiles para cada servicio
└── orchestration/     # DAGs de Airflow
```

## Requisitos

- Docker & Docker Compose
- Python 3.9+
- Make

## Inicio Rápido

```bash
# Configurar variables de entorno
cp .env.example .env

# Levantar servicios
make up

# Entrenar modelo
make train

# Levantar API
make serve

# Ver logs
make logs
```

## Decisiones de Diseño

### 1. Feature Store (Feast)
- Centralización de features para entrenamiento e inferencia
- Consistencia entre training y serving

### 2. Model Registry (MLflow)
- Tracking de experimentos
- Versionado de modelos
- Reproducibilidad

### 3. Orchestration (Airflow)
- DAG de retraining automático
- DAG de monitoring y drift detection

### 4. Serving (Ray Serve)
- Scaling automático
- GPU support
- Batch inference

## Contributing

1. Instalar pre-commit hooks: `pre-commit install`
2. Crear rama: `git checkout -b feature/nombre`
3. Hacer commit: `git commit -m "descripción"`
4. Push: `git push origin feature/nombre`
5. PR para merge

## Licencia

MIT
