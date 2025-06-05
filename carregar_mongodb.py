#!/usr/bin/env python
# coding: utf-8

import os
import json
import time
from pymongo import MongoClient, ASCENDING, DESCENDING, GEOSPHERE
from datetime import datetime

port = 27017


# 🔗 Conexão com o MongoDB (ajuste a URI conforme sua configuração)
client = MongoClient("mongodb://localhost:" + str(port) + "/")

# 🗄️ Criação do banco de dados e coleção
db = client["bd_mac5861"]
collection = db["collection"]

# 📥 Função para carregar arquivos JSON até um limite especificado
def carregar_dados(pasta="dados"):
    arquivos = sorted([
        arq for arq in os.listdir(pasta) if arq.startswith("registro_") and arq.endswith(".json")
    ])
    arquivos = arquivos[:limite]

    documentos = []
    for arq in arquivos:
        caminho = os.path.join(pasta, arq)
        with open(caminho, 'r', encoding='utf-8') as f:
            dado = json.load(f)

            # Conversão do campo de data (MongoDB aceita datetime)
            if "data_nascimento" in dado and "$date" in dado["data_nascimento"]:
                dado["data_nascimento"] = datetime.fromisoformat(dado["data_nascimento"]["$date"])

            documentos.append(dado)

    if documentos:
        collection.insert_many(documentos)
        print(f"Inseridos {len(documentos)} documentos.")
    else:
        print("Nenhum documento foi carregado.")


# In[10]:


# 🔧 Criação dos índices
def criar_indices():
    # Índices simples
    collection.create_index([("nome", ASCENDING)])
    collection.create_index([("idade", ASCENDING)])
    collection.create_index([("salario", ASCENDING)])
    collection.create_index([("data_nascimento", ASCENDING)])
    collection.create_index([("descricao", ASCENDING)])
    collection.create_index([("localizacao_casa", GEOSPHERE)])  # Índice geoespacial esférico
    collection.create_index([("localizacao_casa_plano.x", ASCENDING), ("localizacao_casa_plano.y", ASCENDING)])

    # Índices compostos
    collection.create_index([("idade", ASCENDING), ("salario", DESCENDING)])
    collection.create_index([("idade", ASCENDING), ("data_nascimento", ASCENDING)])
    collection.create_index([("salario", DESCENDING), ("descricao", ASCENDING)])

    print("Índices criados.")


collection.delete_many({})
print("Coleção limpa.")

# 2. Carregar dados
carregar_dados(pasta="data", limite=200000)

# 3. Criar índices
criar_indices()