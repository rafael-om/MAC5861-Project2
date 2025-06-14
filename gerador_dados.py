#!/usr/bin/env python
# coding: utf-8

from concurrent.futures import ProcessPoolExecutor
import json
from tqdm import tqdm
from math import ceil
import random
from datetime import datetime, timedelta
import os
import numpy as np
import re
from faker import Faker
import sys

fake = Faker('pt_BR')
fake2 = Faker('en_US')

LAT_RANGE = (-90, 90)
LON_RANGE = (-180, 180)


def gerar_array_inteiros(x_min, y_max, z_max):
    tamanho = random.randint(x_min, y_max)
    return [random.randint(0, z_max) for _ in range(tamanho)]

def gerar_array_floats(x_min, y_max, z_max):
    tamanho = random.randint(x_min, y_max)
    return [random.uniform(0, z_max) for _ in range(tamanho)]

def gerar_inteiro(z_max):
    return random.randint(0, z_max)

def gerar_float(z_max):
    return random.uniform(0, z_max)

def gerar_array_palavras(x_min, y_max):
    tamanho = random.randint(x_min, y_max)
    return [fake2.word() for _ in range(tamanho)]

def gerar_idade():
    idade = int(np.random.normal(loc=55, scale=20))  
    return max(0, min(120, idade))  

def gerar_salario():
    salario = np.random.exponential(scale=20000)  
    return round(min(salario, 100000), 2)  

def gerar_data_nascimento(idade):
    hoje = datetime.now()
    data_nascimento = hoje - timedelta(days=idade * 365 + random.randint(0, 364))
    return data_nascimento.strftime('%Y-%m-%dT%H:%M:%SZ')

def gerar_localizacao():
    lat = random.uniform(*LAT_RANGE)
    lon = random.uniform(*LON_RANGE)
    return lon, lat

def gerar_descricao():
    return fake2.paragraph(nb_sentences=2, variable_nb_sentences=True)[:500]

def gerar_lista_telefones(x_min, y_max):
    telefones = []
    tamanho = random.randint(x_min, y_max)
    for _ in range(tamanho):
        telefone = fake.phone_number()
        numero_limpo = int(re.sub(r'\D', '', telefone))
        telefones.append(numero_limpo)
    return telefones

def gerar_lista_precos(x_min, y_max):
    tamanho = random.randint(x_min, y_max)
    precos = [round(random.uniform(1, 100000), 2) for _ in range(tamanho)]
    return precos

def gerar_descricao():    
    descricao = ''
    while len(descricao) < 300:
        frase = fake2.sentence()
        if len(descricao) + len(frase) + 1 > 300:
            break
        descricao += frase + ' '
    return descricao.strip()

def gerar_registro():
    nome = fake.name()
    idade = gerar_idade()
    salario = gerar_salario()
    salario2 = gerar_salario()
    data_nascimento = gerar_data_nascimento(idade)
    array_int = gerar_lista_telefones(0, 15)
    array_float = gerar_lista_precos(0, 15)
    lon, lat = gerar_localizacao()

    registro = {
        "name": nome,
        "age": idade,
        "birth_date": {"$date": data_nascimento},
        "wage": salario,
        "description": gerar_descricao(),
        "house_location_sphere": {
            "type": "Point",
            "coordinates": [lon, lat]
        },
        "house_location_plane": [lon, lat],
        "old_wage": salario2,
        "cellphones": array_int,
        "products_prices": array_float,        
    }
    return registro

def gerar_arquivo(start_idx, end_idx, pasta, indice_arquivo):
    dados = []
    for i in range(start_idx, end_idx):
        dados.append(gerar_registro())
    
    caminho_arquivo = os.path.join(pasta, f'bulk_{indice_arquivo:05d}.json')
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        for doc in dados:
            json.dump(doc, f, ensure_ascii=False)
            f.write('\n')  

def executar_gerar_arquivo(args):
    return gerar_arquivo(*args)

def gerar_dados_em_blocos(qtd=10**7, tamanho_bloco=10**5, pasta='./data/', n_processos=10):
    os.makedirs(pasta, exist_ok=True)
    
    total_blocos = ceil(qtd / tamanho_bloco)
    
    tarefas = []
    for i in range(total_blocos):
        start_idx = i * tamanho_bloco
        end_idx = min((i + 1) * tamanho_bloco, qtd)
        tarefas.append((start_idx, end_idx, pasta, i + 1))

    with ProcessPoolExecutor(max_workers=n_processos) as executor:
        list(tqdm(
            executor.map(executar_gerar_arquivo, tarefas),
            total=len(tarefas)
        ))

    print(f'{qtd} registros gerados em {total_blocos} arquivos na pasta "{pasta}"')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        gerar_dados_em_blocos(qtd=int(sys.argv[1]), tamanho_bloco=int(sys.argv[2]), pasta='./sintetico/')
    else:
        gerar_dados_em_blocos(qtd=10**8, tamanho_bloco=10**6, pasta='./sintetico/')