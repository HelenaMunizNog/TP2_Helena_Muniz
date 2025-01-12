import requests

# URL base da API
BASE_URL = "http://localhost:40401"

def testar_home():
    """Testa a rota de saúde da API (GET /)."""
    print("Testando rota de saúde (GET /)...")
    try:
        response = requests.get(BASE_URL + "/")
        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"Erro ao testar a rota de saúde: {e}")

def testar_recomendacao():
    """Testa a rota de recomendação de músicas (POST /api/recomendar)."""
    print("\nTestando recomendação de músicas (POST /api/recomendar)...")
    
    # Corpo da requisição com músicas de exemplo
    payload = {
        "musicas": ["Imagine", "Bohemian Rhapsody", "Hotel California"]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(BASE_URL + "/api/recomendar", json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Resposta JSON: {response.json()}")
        else:
            print(f"Erro: {response.json()}")
    except Exception as e:
        print(f"Erro ao testar recomendação de músicas: {e}")

if __name__ == "__main__":
    print("Iniciando testes na API de Recomendação...\n")
    
    # Testa as rotas necessárias
    testar_home()
    testar_recomendacao()