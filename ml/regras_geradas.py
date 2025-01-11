import pandas as pd
from collections import defaultdict
import pickle
import logging
import os
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def carregar_e_processar_dataset(caminho_dataset, tamanho_chunk=100000):
    """Carrega e processa o dataset em chunks."""
    faixas_por_playlist = defaultdict(set)
    for chunk in pd.read_csv(caminho_dataset, chunksize=tamanho_chunk, usecols=['pid', 'track_name', 'artist_name']):
        chunk['musica'] = chunk['artist_name'] + ' - ' + chunk['track_name']
        for pid, musica in zip(chunk['pid'], chunk['musica']):
            faixas_por_playlist[pid].add(musica)
    return faixas_por_playlist

def gerar_regras(faixas_por_playlist, suporte_minimo=10, confianca_minima=0.5):
    """Gera regras de associação com base nas playlists."""
    contagem_itens = defaultdict(int)
    contagem_pares = defaultdict(int)

    for faixas in tqdm(faixas_por_playlist.values(), desc="Contando itens e pares"):
        for faixa in faixas:
            contagem_itens[faixa] += 1
        for faixa1 in faixas:
            for faixa2 in faixas:
                if faixa1 < faixa2:
                    contagem_pares[(faixa1, faixa2)] += 1

    regras = defaultdict(dict)
    for (faixa1, faixa2), contagem_par in tqdm(contagem_pares.items(), desc="Gerando regras"):
        if contagem_par >= suporte_minimo:
            confianca1 = contagem_par / contagem_itens[faixa1]
            confianca2 = contagem_par / contagem_itens[faixa2]
            if confianca1 >= confianca_minima:
                regras[faixa1][faixa2] = confianca1
            if confianca2 >= confianca_minima:
                regras[faixa2][faixa1] = confianca2

    return dict(regras)

def gerar_modelo(caminhos_datasets, caminho_saida, caminho_musicas_dataset=None):
    """Gera e salva o modelo baseado nos datasets fornecidos."""
    faixas_por_playlist_total = defaultdict(set)
    faixas_total = set()

    for caminho_dataset in caminhos_datasets:
        faixas_por_playlist = carregar_e_processar_dataset(caminho_dataset)
        for pid, faixas in faixas_por_playlist.items():
            faixas_por_playlist_total[pid].update(faixas)
        faixas_total.update(set.union(*faixas_por_playlist.values()))

    if caminho_musicas_dataset:
        musicas_df = pd.read_csv(caminho_musicas_dataset)
        musicas_df['musica'] = musicas_df['artist_name'] + ' - ' + musicas_df['track_name']
        faixas_total.update(musicas_df['musica'])

    regras_geradas = gerar_regras(faixas_por_playlist_total)

    modelo = {
        'regras': regras_geradas,
        'num_regras': sum(len(r) for r in regras_geradas.values()),
        'num_musicas_unicas': len(faixas_total)
    }

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with open(caminho_saida, 'wb') as f:
        pickle.dump(modelo, f)

if __name__ == "__main__":
    caminhos_datasets = [
        '/app/datasets/2023_spotify_ds1.csv',
        '/app/datasets/2023_spotify_ds2.csv'
    ]
    caminho_musicas_dataset = '/app/datasets/2023_spotify_songs.csv'
    caminho_saida = '/app/data/rules.pkl'

    os.makedirs('/app/data', exist_ok=True)

    gerar_modelo(caminhos_datasets, caminho_saida, caminho_musicas_dataset)
    print(f"Modelo gerado e salvo em {caminho_saida}")
