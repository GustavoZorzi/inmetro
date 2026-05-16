import requests
import subprocess
import sys
import os

URL = "https://dados.inmetro.gov.br/registro/SISTEMAS_E_EQUIPAMENTOS_PARA_ENERGIA_FOTOVOLTAICA_(MODULO_CONTROLADOR_DE_CARGA_INVERSOR_E_BATERIA).csv"
DESTINO = "dados_fotovoltaico.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/csv,text/plain,*/*",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://dados.inmetro.gov.br/"
}

def baixar_com_requests():
    print("Tentativa 1: requests...")
    r = requests.get(URL, headers=HEADERS, timeout=60)
    print(f"Status HTTP: {r.status_code}")
    print(f"Headers resposta: {dict(r.headers)}")
    r.raise_for_status()
    with open(DESTINO, "wb") as f:
        f.write(r.content)
    print(f"✅ requests OK! {len(r.content)/1024:.1f} KB")

def baixar_com_curl():
    print("Tentativa 2: curl...")
    cmd = [
        "curl", "-L", "-o", DESTINO,
        "--max-time", "60",
        "--retry", "3",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "-H", "Accept: text/csv,text/plain,*/*",
        "-H", "Accept-Language: pt-BR,pt;q=0.9",
        "-H", "Referer: https://dados.inmetro.gov.br/",
        "-v",  # verbose para ver o erro completo
        URL
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        raise Exception(f"curl falhou com código {result.returncode}")
    tamanho = os.path.getsize(DESTINO)
    print(f"✅ curl OK! {tamanho/1024:.1f} KB")

# Tenta requests primeiro, depois curl
try:
    baixar_com_requests()
except Exception as e:
    print(f"❌ requests falhou: {e}")
    try:
        baixar_com_curl()
    except Exception as e2:
        print(f"❌ curl falhou: {e2}")
        sys.exit(1)
