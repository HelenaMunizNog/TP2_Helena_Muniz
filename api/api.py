import logging
from flask import Flask, request, jsonify
import pickle
import os
from datetime import datetime
from collections import Counter

from flask_cors import CORS

app = Flask(name)
CORS(app)

logging.basicConfig(level=logging.INFO)

modelo_ultima_modificacao = None
modelo = None
CAMINHO_MODELO = os.environ.get('CAMINHO_MODELO', '/app/data/rules.pkl')


@app.route('/')
def home():
    """Rota de saúde da API."""
    return "API de Recomendação de Playlist está funcionando!"


@app.route('/api/recomendar', methods=['POST'])
def recomendar():
    """Rota de recomendação de músicas."""
    if modelo is None:
        carregar_modelo()
    
    if modelo is None:
        return jsonify({"erro": "Modelo não disponível"}), 500

    musicas = request.json.get('musicas', [])
    if not musicas:
        return jsonify({"erro": "Nenhuma música fornecida"}), 400

    logging.info(f"Recebido pedido de músicas: {musicas}")

    recomendacoes = Counter()
    
    # Recomenda músicas com base nas regras do modelo
    for musica in musicas:
        recomendacoes.update(modelo['regras'].get(musica, []))

    # Remove as músicas de entrada das recomendações
    recomendacoes.subtract(musicas)
    
    # Retorna as 5 músicas mais recomendadas
    top_recomendacoes = [musica for musica, _ in recomendacoes.most_common(5)]

    return jsonify({
        "recomendacoes": top_recomendacoes,
        "versao_modelo": "1.6",
        "data_modelo": datetime.fromtimestamp(modelo_ultima_modificacao).isoformat() if modelo_ultima_modificacao else None,
    })


@app.route('/api/saude', methods=['GET'])
def verificar_saude():
    """Rota de verificação de saúde da API."""
    if modelo is None:
        carregar_modelo()

    return jsonify({
        "status": "saudável" if modelo is not None else "não saudável",
        "modelo_carregado": modelo is not None,
        "data_modelo": datetime.fromtimestamp(modelo_ultima_modificacao).isoformat() if modelo_ultima_modificacao else None,
    })


def carregar_modelo():
    """Carrega o modelo de recomendação se necessário."""
    global modelo, modelo_ultima_modificacao
    logging.info(f"Tentando carregar o modelo de {CAMINHO_MODELO}")
    
    if os.path.exists(CAMINHO_MODELO):
        ultima_modificacao_atual = os.path.getmtime(CAMINHO_MODELO)
        
        # Carrega o modelo somente se houve modificações no arquivo
        if modelo is None or ultima_modificacao_atual != modelo_ultima_modificacao:
            try:
                with open(CAMINHO_MODELO, 'rb') as f:
                    modelo = pickle.load(f)
                modelo_ultima_modificacao = ultima_modificacao_atual
                logging.info(f"Modelo carregado com sucesso. Número de músicas: {len(modelo)}")
                logging.info(f"Amostra do conteúdo do modelo: {list(modelo.items())[:2]}")
            except Exception as e:
                logging.error(f"Erro ao carregar o modelo: {str(e)}", exc_info=True)
                modelo = None
    else:
        logging.error(f"Arquivo do modelo não encontrado em {CAMINHO_MODELO}")


if __name__ == "__main__":
    carregar_modelo()
    app.run(host='0.0.0.0', port=5000)
