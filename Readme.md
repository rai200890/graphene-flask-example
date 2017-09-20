#graphene-flask-example

Exemplo de uma API [GraphQL](http://graphql.org/) usando [Graphene](http://docs.graphene-python.org/en/latest/quickstart/), [Flask GraphQL](https://github.com/graphql-python/flask-graphql) e [Graphene-SQLAlchemy](http://docs.graphene-python.org/projects/sqlalchemy/en/latest/).

##Instalação

###Virtualenv

[Instalação](https://virtualenv.pypa.io/en/stable/installation/)

```
  virtualenv --python python3 venv
  source venv/bin/activate
  pip install -U pip
  pip install -r requirements-dev.txt
```

###Tox

[Instalação](https://tox.readthedocs.io/en/latest/)

```
tox
```

###Docker-Compose

[Instalação](https://docs.docker.com/compose/install/)

```
docker-compose up #cria e executa os containers web e db
docker-compose run --service-ports --name user_api_flask_web web --rm #permite que o servidor da aplicação pare em breakpoints
docker-compose exec web bash #abre o terminal do container web
docker-compose exec db mysql #abre o CLI do mysql no container db
```

##Configuração do ambiente local

Crie um arquivo local .env baseado no arquivo .env.sample.

##Execução do servidor local

```
  python run.py #executa o servidor local na porta 3000
```

##Versionamento do banco de dados

A aplicação usa o [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) para fazer o versionamento do banco de dados.

Primeiramente crie o banco de dados dos ambientes de desenvolvimento e teste.

```
mysql -e "create database user_db;"
mysql -e "create database user_db_test;"
```

Em seguida:

```
python manage.py db migrate #cria migração caso haja mudança no schema do banco de dados
python manage.py db upgrade #executa as migrações do banco de dados
```

###Rotas

```

GET /api/healthcheck

GET /api/graphql

```

##Execução dos testes unitários

```
pytest
```

###Linter

```
flake8 tests user_api
```
