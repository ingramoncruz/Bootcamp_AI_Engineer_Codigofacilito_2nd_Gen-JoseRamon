"""Reporte de llamadas al LLM a partir de logs/llm_calls.jsonl.

Uso:
    uv run scripts/report.py [ruta/al/archivo.jsonl]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import statistics
import argparse
from collections import Counter

DEFAULT_PATH = Path("logs/llm_calls.jsonl")

def load_events(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        sys.exit(f"No hay llamadas registradas todavia. Corre main.py primero.")
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]

def percentiles(values: list[float]) -> tuple[float, float]:
    """p50 y p90 quantiles() exige al menos 2 datos"""
    if len(values) == 1:
        return values[0], values[0]
    q = statistics.quantiles(values, n=100, method="inclusive")
    return q[49], q[94]

def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = Path(argv[0]) if argv else DEFAULT_PATH

    lines = path.read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in lines if line.strip()]
    print(f"Llamadas registradas: {len(events)}")

    events = load_events(args.path)
    ok = [e for e in events if e["success"]]
    total_cost = sum(e["cost"] for e in events)
    print(f"Eventos en el log:  {len(events)}   ({len(ok)} respuestas)")
    print("Costo total: ${:.2f}".format(total_cost))
    if ok:
        latencies = [e["latency_ms"] for e in ok]
        p50, p95 = percentiles(latencies)
        print("Latencia p50: {:.2f} ms".format(p50))
        print("Latencia p95: {:.2f} ms".format(p95))
    else:
        print("No hay llamadas exitosas")


    # TODO(clase-1): completa el reporte. Debe imprimir:
    #   - costo total en USD,
    #   - latencia p50 y p95 (solo llamadas exitosas; usa statistics.quantiles),
    #   - % de llamadas con fallback,
    #   - número de llamadas por proveedor.
    # Usa solo la librería estándar y maneja con un mensaje el caso de que el archivo
    # no exista o esté vacío.
    return 0


if __name__ == "__main__":
    sys.exit(main())
