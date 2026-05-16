import requests
import sys

URL = "https://dados.inmetro.gov.br/registro/SISTEMAS_E_EQUIPAMENTOS_PARA_ENERGIA_FOTOVOLTAICA_(MODULO_CONTROLADOR_DE_CARGA_INVERSOR_E_BATERIA).csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/csv,text/plain,*/*",
    "Accept-Language": "pt-BR,pt;q=0.9"
}

print("Baixando CSV do INMETRO...")

response = requests.get(URL, headers=HEADERS, timeout=60)
response.raise_for_status()

with open("dados_fotovoltaico.csv", "wb") as f:
    f.write(response.content)

kb = len(response.content) / 1024
print(f"✅ Sucesso! {kb:.1f} KB salvos.")
