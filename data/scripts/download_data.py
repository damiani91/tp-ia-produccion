"""Script para descargar los datasets de producción de pozos desde datos.gob.ar."""
from pathlib import Path

import requests

# Variables globales
URLS = {
    "produccion": (
        "https://datos.gob.ar/dataset/energia-produccion-petroleo-gas-por-pozo-"
        "capitarchivo/energia_b5b58cdc-9e07-41f9-b392-fb9ec68b0725"
    ),
    "pozos": (
        "https://datos.gob.ar/dataset/energia-produccion-petroleo-gas-por-pozo-"
        "capitarchivo/energia_cbfa4d79-ffb3-4096-bab5-eb0dde9a8385"
    ),
}

RAW_DIR = Path("data/raw")


def download_file(url: str, dest: Path) -> None:
    """Descarga un archivo desde una URL."""
    # Si la descarga automática falla, descargar manualmente y colocar en data/raw/.
    print(f"Descargando {url} → {dest}")
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f" ✓ {dest} ({dest.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    # Descargar o indicar descarga manual
    print("NOTA: Si la descarga automática falla, descargar manualmente desde:")
    for name, url in URLS.items():
        print(f" - {name}: {url}")
        print(f" y colocar los CSVs en {RAW_DIR}/")
