#!/usr/bin/env python
# coding: utf-8

import json
import random
from datetime import datetime, timedelta

import os
import numpy as np
from faker import Faker
from shapely.geometry import Point
import geopandas as gpd
from pyproj import Transformer
fake = Faker('pt_BR')

# Configurações para localização
# Limites aproximados de latitude e longitude da cidade de São Paulo
LAT_RANGE = (-23.8, -23.4)
LON_RANGE = (-46.9, -46.3)

# Sistema de projeção plano (UTM Zona 23S, que cobre São Paulo)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:31983", always_xy=True)


fake2 = Faker('en_US')


# Gera um array de inteiros entre 0 e Z, com tamanho entre X e Y
def gerar_array_inteiros(x_min, y_max, z_max):
    tamanho = random.randint(x_min, y_max)
    return [random.randint(0, z_max) for _ in range(tamanho)]


# Gera um array de floats entre 0 e Z, com tamanho entre X e Y
def gerar_array_floats(x_min, y_max, z_max):
    tamanho = random.randint(x_min, y_max)
    return [random.uniform(0, z_max) for _ in range(tamanho)]


# Gera um inteiro entre 0 e Z
def gerar_inteiro(z_max):
    return random.randint(0, z_max)


# Gera um float entre 0 e Z
def gerar_float(z_max):
    return random.uniform(0, z_max)


# Gera um array de strings (palavras em inglês) com tamanho entre X e Y
def gerar_array_palavras(x_min, y_max):
    tamanho = random.randint(x_min, y_max)
    return [fake2.word() for _ in range(tamanho)]


# Função para gerar idade com distribuição normal truncada
def gerar_idade():
    idade = int(np.random.normal(loc=35, scale=20))  # Média 35 anos, desvio 20
    return max(0, min(100, idade))  # Trunca entre 0 e 100

# Função para gerar salário com distribuição exponencial
def gerar_salario():
    salario = np.random.exponential(scale=20000)  # Média aproximada 20000
    return round(min(salario, 100000), 2)  # Limita até 100000

# Função para gerar data de nascimento a partir da idade
def gerar_data_nascimento(idade):
    hoje = datetime.now()
    data_nascimento = hoje - timedelta(days=idade * 365 + random.randint(0, 364))
    return data_nascimento.strftime('%Y-%m-%d')

# Função para gerar ponto geográfico em São Paulo
def gerar_localizacao():
    lat = random.uniform(*LAT_RANGE)
    lon = random.uniform(*LON_RANGE)
    return lon, lat

# Função para gerar descrição aleatória
def gerar_descricao():
    return fake2.paragraph(nb_sentences=2, variable_nb_sentences=True)[:500]
    #return fake.text(max_nb_chars=100)


def gerar_descricao():
    # Gera uma descrição de até 100 caracteres com frases curtas em português
    descricao = ''
    while len(descricao) < 300:
        frase = fake2.sentence()
        if len(descricao) + len(frase) + 1 > 300:
            break
        descricao += frase + ' '
    return descricao.strip()

# Função principal para gerar um registro
def gerar_registro():
    nome = fake.name()
    idade = gerar_idade()
    desc = gerar_descricao()
    salario = gerar_salario()

    lon, lat = gerar_localizacao()
    x, y = transformer.transform(lon, lat)  # Conversão para plano

    registro = {
        # Index
        "nome": nome,
        "idade": idade,
        "data_nascimento": {"$date": gerar_data_nascimento(idade)},
        "salario": gerar_salario(),
        "descricao": desc,
        "localizacao_casa": {
            "type": "Point",
            "coordinates": [lon, lat]
        },
        "localizacao_casa_plano": {
            "x": x,
            "y": y
        },
        # Non-index
        "nome2": nome,
        "descricao2": desc,
        "salario2": salario,
        "idade2": idade,
        "array_int": gerar_array_inteiros(1, 15, 100000),
        "array_float": gerar_array_floats(1, 15, 10000),
        "array_str": gerar_array_palavras(1, 15),
    }
    return registro

def gerar_dados_sinteticos(start, end, pasta='./data/'):
    os.makedirs(pasta, exist_ok=True)

    for i in range(start, end):
        registro = gerar_registro()
        caminho_arquivo = os.path.join(pasta, f'registro_{i}.json')
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(registro, f, ensure_ascii=False, indent=4)

    print(f'{end - start} registros gerados na pasta "{pasta}"')


#gerar_dados_sinteticos(0, 200000)
gerar_dados_sinteticos(200000, 200020)
