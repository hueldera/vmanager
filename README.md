# Vulnerability Manager

## Instruções

### Poetry
Instale as dependências do app Django utilizando [Poetry](https://python-poetry.org/)
```shell
$ poetry shell
$ poetry install
```

### Django
Rode o app Django localmente e execute os testes (configuração padrão com sqlite):
```shell
$ python manage.py migrate
$ python manage.py test
$ python manage.py runserver
```
Agora basta acessar a aplicação pelo endereço: `http://127.0.0.1:8000/` e carregar o arquivo CSV de exemplo na raiz do projeto.



### Frontend (Dev)
O frontend React está sendo hospedado pelo próprio Django com os templates, para iniciar o webpack em modo `--watch` execute:
```shell
$ cd frontend
$ npm install
$ npm run dev
```



