import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CUITS = [
    "30511521498",
    "27304456345",
    "30708658819",
    # agregá más acá
]

base_url = "https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/ChequesRechazados"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
})
session.verify = False

for cuit in CUITS:
    print(f"\n{'='*50}")
    print(f"CUIT: {cuit}")
    try:
        r = session.get(f"{base_url}/{cuit}", timeout=15)
        print(f"Status: {r.status_code}")
        print(f"Respuesta cruda:\n{json.dumps(r.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
