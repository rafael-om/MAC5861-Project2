python3 carregar_mongodb.py "./data/10**5/"         
echo python3 testar_consultas.py 100K         
python3 testar_consultas.py 100K 5

echo 

python3 carregar_mongodb.py "./data/10**6/"         
echo python3 testar_consultas.py 1M         
python3 testar_consultas.py 1M 2

echo 

python3 carregar_mongodb.py "./data/10**7/"         
echo python3 testar_consultas.py 10M         
python3 testar_consultas.py 10M 2