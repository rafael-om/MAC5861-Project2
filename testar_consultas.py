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
import pprint
import re
import sys
from pymongo import MongoClient, ASCENDING, DESCENDING, GEOSPHERE
from datetime import datetime

PRINT = False
PROJECTION = False

def preprocess(lines):
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "db.pessoas.find" in lines[i]:
            line = lines[i]
            while ");" not in line:
                i += 1
                line += lines[i].strip()
        new_lines.append(line)
        if PRINT: print(line)
        i += 1
    return new_lines

def converter_json(text):
    if text:
        # Adiciona "" às chaves
        text = re.sub(r'([\w$]+): ', r'"\1": ', text)

        # Adiciona "" aos regex
        text = re.sub(r'(/[^/]+/i)', r'"\1"', text)

        # Calcula as divisões
        def eval_div(match):
            num1 = float(match.group(1))
            num2 = float(match.group(2))
            return str(num1 / num2)
        pattern = r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)'
        text = re.sub(pattern, eval_div, text)

        # Calcula as datas
        text = re.sub(r'ISODate\("([^"]+)"\)', r'{"$date":"\1"}', text)

        if PRINT: print(text)
        return json.loads(text)
    else:
        return None

def parse(lines, colecao, numero_exec):
    numero_consultas = 0 
    for line in lines:
        if "db.pessoas.find" in line:
            numero_consultas += 1
    inicio = datetime.now()
    indexes = dict()
    regions = dict()
    numero_consulta = 0
    region = None
    consultas = None
    for line in lines:
        line = line.rstrip()
        if "//" in line:
            if "#region" in line:
                # Nova categoria de consultas
                region = dict()
                title = line.replace("//#region", "").rstrip()
                regions[title] = region
                consultas = None
            elif not "#endregion" in line:
                # Sub cagetoria
                consultas = []
                title = line.replace("//", "").rstrip()
                region[title] = consultas
        elif "db.pessoas.find" in line:
            if numero_exec == 0:
                continue
            numero_consulta += 1
            fim = datetime.now()
            decorrido = str(fim - inicio).split('.')[0]
            print(f'\rRodando consultas ({numero_consulta}/{numero_consultas}) [{decorrido}]', end='', flush=True)

            line = line.replace("db.pessoas.find(", "").replace(");", "")
            if "hint(" in line:
                consulta = line.split(").hint(")
            else:
                consulta = [line, None]
            t, n = medir_tempo_consulta(colecao, consulta, numero_exec)
            if consultas is None:
                consultas = []
                region[""] = consultas
            consultas.append((consulta,t,n))
        elif "db.pessoas.createIndex" in line:
            line = line.replace("db.pessoas.createIndex(", "").replace(");", "")
            i, t, s = medir_criacao_index(colecao, line)
            if PRINT: print("Index criado: " + line)
            indexes[i] = (t, s)
        elif "db.pessoas.dropIndex" in line:
            line = line.replace("db.pessoas.dropIndex(", "").replace(");", "")
            colecao.drop_index(converter_json(line))
            if PRINT: print("Index excluído: " + line)
    if numero_exec > 0:
        print()
    return regions, indexes

# Medição de tamanho e tempo de criação dos índices
def medir_criacao_index(colecao, index):
    index = converter_json(index)
    name = "_".join(["%s_%s" % i for i in index.items()])
    t = time.time()
    colecao.create_index(index)
    t = time.time() - t
    stats = db.command("collStats", colecao.name)['indexSizes']
    return name, t, stats[name]

def criar_projecao(consulta):
    p = {"_id": 0}
    items = list(consulta.items())
    while items:
        (k, v) = items.pop()
        #if k[0] != '$' and k != "type" and k != "coordinates":
        #    p[k] = 1
        if isinstance(v, dict):
            items += list(v.items())
    return p

# Medição do tempo de resposta das consultas
def medir_tempo_consulta(colecao, args, numero_exec):
    # print('Número de execuções', numero_exec)
    f = converter_json(args[0])
    hint = converter_json(args[1])
    p = criar_projecao(f) if PROJECTION else None
    tempos = []
    n_resultados = []
    if PRINT: print(f)
    for _ in range(0, numero_exec):
        explicacao = colecao.find(f, p, hint=hint).explain()
        tempos.append(explicacao["executionStats"]["executionTimeMillis"]/1000)
        n_resultados.append(explicacao['executionStats']['nReturned'])
    avg = statistics.mean(tempos)
    std = statistics.stdev(tempos)
    if PRINT: print(f"Tempo de resposta: {avg:.6f} segundos com desvio padrão {std:.6f} ")
    return tempos, n_resultados

if __name__ == '__main__':
    db_name='bd_mac5861'
    colecao_name='pessoas'
    mongo_uri='mongodb://localhost:27017'

    client = MongoClient(mongo_uri)
    db = client[db_name]
    colecao = db[colecao_name]
    colecao.drop_indexes()

    nome_documento = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    numero_exec = 2

    if len(sys.argv) > 2:
        nome_documento = sys.argv[1]
        numero_exec = int(sys.argv[2])

    with open("consultas.js", "r") as f:
        lines = preprocess(f.read().splitlines())
        r, index = parse(lines, colecao, numero_exec)

    # Abre o arquivo para escrita antes do loop principal
    if numero_exec > 0:
        with open(f"avg-std-{nome_documento}.txt", "w") as f_out:
            for key, value in r.items():
                if PRINT: print(key)
                f_out.write(key + "\n")
                for key2, consultas in value.items():
                    if len(key2) > 0:
                        if PRINT: print(key2)
                        f_out.write(key2 + "\n")
                    tempos_total = []
                    i = 1
                    for consulta, tempos, result_sizes in consultas:
                        if PRINT:
                            print(consulta)
                            print(tempos)
                            print(result_sizes)
                        avg = statistics.mean(tempos)
                        std = statistics.stdev(tempos)
                        avg_n = int(statistics.mean(result_sizes))
                        f_out.write(f"{i:5d}: {avg:.6f} +- {std:.6f} -- {avg_n}\n")
                        tempos_total += tempos
                        i += 1
                    if tempos_total:
                        avg = statistics.mean(tempos_total)
                        std = statistics.stdev(tempos_total)
                        f_out.write(f"Total: {avg:.6f} +- {std:.6f}\n")
                if PRINT: print()
                f_out.write("\n")
        print(f"avg-std-{nome_documento}.txt criado")

    with open(f"index-{nome_documento}.txt", "w") as f_out:
        f_out.write("Tempo de criação, tamanho:\n")
        for key, value in index.items():
            time, size = value
            f_out.write(f"{key}:\n{time:.6f}s\t{size/1024}kb\n")
        print(f"index-{nome_documento}.txt criado")
