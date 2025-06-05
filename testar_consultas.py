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
def medir_tempo_consulta(consulta):
    tempos = []
    for i in range(0, 20):
        inicio = time.time()
        resultado = list(consulta)
        fim = time.time()
        tempo = fim - inicio
        tempos.append(tempo)
    avg = statistics.mean(tempos)
    std = statistics.stdev(tempos)
    print(f"Tempo de resposta: {avg:.6f} +- {std:.6f} segundos")
    return tempos


def print_stats():
    stats = db.command("collStats", "collection")

    print(stats)

    print("\n📊 Tamanho de cada índice:")
    for indice, tamanho in stats['indexSizes'].items():
        print(f" - {indice}: {tamanho / 1024:.2f} KB")
    print(f"Index Size: {stats['totalIndexSize']/1024/1024:.2f} MB")
    print(f"Storage Size: {stats['storageSize']/1024/1024:.2f} MB")


def consultas_sem_index():
    print("\nMedindo tempos de consultas - Sem Index:")
    tempos = []

    print("Idade entre 30 e 50")
    consulta = collection.find({"idade2": {"$gte": 30, "$lte": 50}})
    tempos += medir_tempo_consulta(consulta)

    print("Salário acima de 50k")
    consulta = collection.find({"salario2": {"$gt": 50000}})
    tempos += medir_tempo_consulta(consulta)

    print("Array de inteiros")
    consulta = collection.find({"array_int": 12522})
    tempos += medir_tempo_consulta(consulta)

    print("Array de float")
    consulta = collection.find({"array_float": 5329.944047697353})
    tempos += medir_tempo_consulta(consulta)

    print("Array de string")
    consulta = collection.find({"array_str": "environment"})
    tempos += medir_tempo_consulta(consulta)

    avg = statistics.mean(tempos)
    std = statistics.stdev(tempos)
    print(f"Tempo de resposta (Sem Index): {avg:.6f} +- {std:.6f} segundos")


def consultas_simples(nome):
    print("\nMedindo tempos de consultas - Index Simples:")
    tempos = []

    print("Nome exato")
    consulta = collection.find({"nome": nome})
    tempos += medir_tempo_consulta(consulta)

    print("Idade entre 30 e 50")
    consulta = collection.find({"idade": {"$gte": 30, "$lte": 50}})
    tempos += medir_tempo_consulta(consulta)

    print("Salário acima de 50k")
    consulta = collection.find({"salario": {"$gt": 50000}})
    tempos += medir_tempo_consulta(consulta)

    print("Geoespacial - próximos ao centro de SP")
    ponto = {"type": "Point", "coordinates": [-46.633309, -23.55052]}
    consulta = collection.find({
        "localizacao_casa": {
            "$near": {
                "$geometry": ponto,
                "$maxDistance": 5000
            }
        }
    })
    tempos += medir_tempo_consulta(consulta)

    print("Data de nascimento entre 1975 e 2005, salário acima de 50k")
    consulta = collection.find({
        "data_nascimento": {"$gte": "1975-01-01", "$lte": "2005-12-31"}, 
        "salario": {"$gt": 50000}
    })
    tempos += medir_tempo_consulta(consulta)

    avg = statistics.mean(tempos)
    std = statistics.stdev(tempos)
    print(f"Tempo de resposta (Index Simples): {avg:.6f} +- {std:.6f} segundos")


def consultas_composto():
    print("\nMedindo tempos de consultas - Index Composto:")

    print("Idade entre 30 e 50, data de nascimento entre 1975 e 2005")
    consulta = collection.find({
        "idade": {"$gte": 30, "$lte": 50}, 
        "data_nascimento": {"$gte": "1975-01-01", "$lte": "2005-12-31"}
    })
    medir_tempo_consulta(consulta)

    print("Idade entre 30 e 50, salário acima de 50k")
    consulta = collection.find({
        "idade": {"$gte": 30, "$lte": 50}, 
        "salario": {"$gt": 50000}
    })
    medir_tempo_consulta(consulta)


def consultas_regex(desc):
    print("\nMedindo tempos de consultas - Regex:")
    tempos = []

    print("Descrição")
    consulta = collection.find({"descricao": {"$regex": desc}})
    tempos += medir_tempo_consulta(consulta)

    print("Descrição e salário")
    consulta = collection.find({
        "descricao": {"$regex": desc}, 
        "salario": {"$gt": 50000}
    })
    tempos += medir_tempo_consulta(consulta)

    avg = statistics.mean(tempos)
    std = statistics.stdev(tempos)
    print(f"Tempo de resposta (Regex): {avg:.6f} +- {std:.6f} segundos")


path = os.path.join("data", "registro_100000.json")
with open(path, 'r', encoding='utf-8') as f:
    dado = json.load(f)
    consultas_sem_index()
    consultas_simples(dado["nome"])
    consultas_composto()
    consultas_regex(dado["descricao"][:30])