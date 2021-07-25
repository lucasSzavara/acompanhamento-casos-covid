# Acompanhamento de casos de COVID-19

O projeto usa Python 3.8, que pode ser instalado [aqui](https://www.python.org/downloads/release/python-3810/). Para
rodar o projeto é necessário instalar também o [Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today).

Após a instalação do Pipenv, instale os pacotes necessários para execução:

```bash
pipenv install
```

E rode o projeto:

```bash
cd covid_ved
gunicorn index:server
```
