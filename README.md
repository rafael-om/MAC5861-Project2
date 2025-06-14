# Projeto 2 - MAC5861: Análise de Desempenho de Consultas MongoDB

Este repositório contém os dados e programas utilizados no Projeto 2 da disciplina MAC5861, focado na análise de desempenho de consultas em MongoDB.

## Estrutura do Projeto

- `gerador_dados.py`: Script para geração de dados sintéticos
- `testar_consultas.py`: Script para execução e medição de desempenho das consultas
- `consultas.js`: Arquivo contendo as consultas MongoDB a serem testadas
- `carregar_mongodb.py`: Script para carregar os dados gerados no MongoDB
- Arquivos de dados:
  - `index-*.txt`: Arquivos de resultados de espaço e tempo de criação dos índices
  - `avg-std-*.txt`: Arquivos com resultados de média e desvio padrão das consultas

## Requisitos

- Python 3.x
- MongoDB
- Bibliotecas Python:
  - pymongo
  - faker
  - tqdm
  - numpy

## Como Usar

1. **Geração de Dados**:
   ```bash
   python gerador_dados.py [quantidade] [tamanho_bloco]
   ```
   - `quantidade`: Número total de registros a serem gerados (padrão: 10^8)
   - `tamanho_bloco`: Tamanho de cada bloco de dados (padrão: 10^6)

2. **Carregar Dados no MongoDB**:
   ```bash
   python carregar_mongodb.py [pasta]
   ```
   - `pasta`: Diretório onde estão os dados a serem carregados (padrão: './data/10**8/')

3. **Executar Testes de Consulta**:
   ```bash
   python testar_consultas.py [nome_documento] [numero_execucoes]
   ```
   - `nome_documento`: Nome do arquivo de saída (padrão: timestamp atual)
   - `numero_execucoes`: Número de execuções para cada consulta (padrão: 2)

## Estrutura dos Dados

Os dados gerados contêm os seguintes campos:
- `name`: Nome da pessoa
- `age`: Idade
- `birth_date`: Data de nascimento
- `wage`: Salário atual
- `description`: Descrição textual
- `house_location_sphere`: Localização geográfica (formato GeoJSON)
- `house_location_plane`: Coordenadas planas
- `old_wage`: Salário anterior
- `cellphones`: Lista de números de telefone
- `products_prices`: Lista de preços de produtos

## Resultados

Os resultados das análises são salvos em arquivos no formato:
- `avg-std-{nome_documento}.txt`: Contém médias e desvios padrão dos tempos de execução
- `index-{nome_documento}.txt`: Contém informações sobre os índices utilizados

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.