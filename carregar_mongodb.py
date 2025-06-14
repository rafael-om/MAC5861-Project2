#!/usr/bin/env python
# coding: utf-8

from concurrent.futures import ProcessPoolExecutor
import json
from tqdm import tqdm
import os
from pymongo import MongoClient
import sys

def conectar_db(mongo_uri, db_name, colecao_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    colecao = db[colecao_name]
    return colecao

def inserir_arquivo_mongodb_paralelo(args):
    caminho_arquivo, mongo_uri, db_name, colecao_name = args
    colecao = conectar_db(mongo_uri, db_name, colecao_name)
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        documentos = [json.loads(linha) for linha in f]
    if documentos:
        colecao.insert_many(documentos)
    return caminho_arquivo

def inserir_dados_da_pasta_mongodb_paralelo(pasta, mongo_uri, db_name, colecao_name, n_processos=4):
    arquivos = sorted([f for f in os.listdir(pasta) if f.endswith('.json')])
    caminhos = [(os.path.join(pasta, arquivo), mongo_uri, db_name, colecao_name) for arquivo in arquivos]

    with ProcessPoolExecutor(max_workers=n_processos) as executor:
        for _ in tqdm(executor.map(inserir_arquivo_mongodb_paralelo, caminhos), total=len(caminhos), desc='Inserindo arquivos'):
            pass

    print(f'Pasta "{pasta}" foi inserida na coleção "{colecao_name}" em "{db_name}".')

if __name__ == '__main__':
    db_name='bd_mac5861'
    colecao_name='pessoas'
    mongo_uri='mongodb://localhost:27017'
    colecao = conectar_db(mongo_uri, db_name, colecao_name)
    colecao.drop()
    if len(sys.argv) > 1:
        inserir_dados_da_pasta_mongodb_paralelo(sys.argv[1], mongo_uri, db_name, colecao_name, n_processos=8)
    else:
        inserir_dados_da_pasta_mongodb_paralelo('./data/10**8/', mongo_uri, db_name, colecao_name, n_processos=8)