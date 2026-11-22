from contextlib import closing
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from db import get_connection
from models import KpiVentes

app = FastAPI(title="KPI API", version="0.2.0")

MOIS_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"

SQL_KPI_VENTES = """
SELECT
    COUNT(DISTINCT f.SalesOrderNumber) AS nb_commandes,
    SUM(f.SalesAmount)                 AS chiffre_affaires,
    SUM(f.OrderQuantity)               AS quantite
FROM dbo.FactInternetSales f
JOIN dbo.DimDate d ON d.DateKey = f.OrderDateKey
WHERE d.CalendarYear = ? AND d.MonthNumberOfYear = ?;
"""

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/kpi/ventes", response_model=KpiVentes)
def kpi_ventes(
    mois: Annotated[str, Query(pattern=MOIS_PATTERN, examples=["2013-06"])],
) -> KpiVentes:
    annee, num_mois = map(int, mois.split("-"))
    with closing(get_connection()) as conn:
        row = conn.cursor().execute(SQL_KPI_VENTES, annee, num_mois).fetchone()
    if row is None or row.nb_commandes == 0:
        raise HTTPException(status_code=404, detail=f"Aucune vente pour {mois}")
    return KpiVentes(
        mois=mois,
        nb_commandes=row.nb_commandes,
        chiffre_affaires=row.chiffre_affaires,
        quantite=row.quantite,
    )