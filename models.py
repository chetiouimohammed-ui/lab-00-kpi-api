from decimal import Decimal

from pydantic import BaseModel


class KpiVentes(BaseModel):
    mois: str
    nb_commandes: int
    chiffre_affaires: Decimal
    quantite: int
