from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_kpi_ventes_ok():
    r = client.get("/kpi/ventes", params={"mois": "2013-06"})
    assert r.status_code == 200
    data = r.json()
    assert data["mois"] == "2013-06"
    assert data["nb_commandes"] > 0
    assert float(data["chiffre_affaires"]) > 0

def test_kpi_ventes_format_invalide():
    r = client.get("/kpi/ventes", params={"mois": "2013-13"})
    assert r.status_code == 422

def test_kpi_ventes_mois_sans_vente():
    r = client.get("/kpi/ventes", params={"mois": "2030-01"})
    assert r.status_code == 404