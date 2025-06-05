#!/usr/bin/env python
# coding: utf-8


#Testar com:
# Sem índice
# Índice simples (ex: sobre o campo timestamp)
# Índice composto (ex: {"user_id": 1, "timestamp": -1})
# Índice de texto (para buscas em descrições)

#Medir:
# Tempo de consulta
# Tempo de criação de índice
# Espaço ocupado pelos índices

import os
import json
import time
import statistics 
from pymongo import MongoClient, ASCENDING, DESCENDING, GEOSPHERE
from datetime import datetime
from pprint import pprint

port = 27017


# 🔗 Conexão com o MongoDB (ajuste a URI conforme sua configuração)
client = MongoClient("mongodb://localhost:" + str(port) + "/")

# 🗄️ Criação do banco de dados e coleção
db = client["bd_mac5861"]
collection = db["collection"]


# ⏱️ Medição do tempo de resposta das consultas
def medir_tempo(func, n=20):
    tempos = []
    resultado = []
    for i in range(0, n):
        inicio = time.time()
        r = func()
        fim = time.time()
        tempo = fim - inicio
        tempos.append(tempo)
        resultado.append(r)
    if n > 1:
        avg = statistics.mean(tempos)
        std = statistics.stdev(tempos)
        print(f"Tempo de resposta: {avg:.6f} +- {std:.6f} segundos")
        return tempos, resultado
    else:
        print(f"Tempo de resposta: {tempos[0]:.6f} segundos")
        return tempos[0], resultado[0]


def adicionar_registros(start=200000, end=200020):
    print("\nMedindo tempo adição de registro:")
    tempos = []
    nomes = []

    for i in range(start, end):
        path = os.path.join("data", f"registro_{i}.json")
        with open(path, 'r', encoding='utf-8') as f:
            dado = json.load(f)
            if "data_nascimento" in dado and "$date" in dado["data_nascimento"]:
                dado["data_nascimento"] = datetime.fromisoformat(dado["data_nascimento"]["$date"])
            t, r = medir_tempo(lambda : collection.insert_one(dado), 1)
            tempos.append(t)
            nomes.append(dado["nome"])

    avg = statistics.mean(tempos)
    std = statistics.stdev(tempos)
    print(f"Tempo de resposta (Criação): {avg:.6f} +- {std:.6f} segundos")

    return nomes


def deletar_registros(nomes):
    print("\nMedindo tempo remoção de registro:")
    tempos = []

    for nome in nomes:
        t, r = medir_tempo(lambda : collection.delete_one({"nome" : nome}), 1)
        tempos.append(t)
    avg = statistics.mean(tempos)
    std = statistics.stdev(tempos)
    print(f"Tempo de resposta (Remoção): {avg:.6f} +- {std:.6f} segundos")


collection.drop_indexes()
print("\nMedindo tempo adição/remoção (sem índices):")
nomes = adicionar_registros()
deletar_registros(nomes)

collection.drop_indexes()
collection.create_index([("nome", ASCENDING)])
collection.create_index([("idade", ASCENDING)])
collection.create_index([("salario", ASCENDING)])
collection.create_index([("data_nascimento", ASCENDING)])
collection.create_index([("descricao", ASCENDING)])
collection.create_index([("localizacao_casa", GEOSPHERE)])  # Índice geoespacial esférico
collection.create_index([("localizacao_casa_plano.x", ASCENDING), ("localizacao_casa_plano.y", ASCENDING)])
print("\nMedindo tempo adição/remoção (índices simples):")
nomes = adicionar_registros()
deletar_registros(nomes)

collection.drop_indexes()
collection.create_index([("idade", ASCENDING), ("salario", DESCENDING)])
collection.create_index([("idade", ASCENDING), ("data_nascimento", ASCENDING)])
collection.create_index([("salario", DESCENDING), ("descricao", ASCENDING)])
print("\nMedindo tempo adição/remoção (índices compostos):")
nomes = adicionar_registros()
deletar_registros(nomes)

collection.drop_indexes()
collection.create_index([("nome", ASCENDING)])
collection.create_index([("idade", ASCENDING)])
collection.create_index([("salario", ASCENDING)])
collection.create_index([("data_nascimento", ASCENDING)])
collection.create_index([("descricao", ASCENDING)])
collection.create_index([("localizacao_casa", GEOSPHERE)])  # Índice geoespacial esférico
collection.create_index([("localizacao_casa_plano.x", ASCENDING), ("localizacao_casa_plano.y", ASCENDING)])
print("\nMedindo tempo adição/remoção (todos os índices):")
nomes = adicionar_registros()
deletar_registros(nomes)