# Sistema de Gerenciamento de Testes

Permite ao QA gerenciar a execução dos testes de diversos sistemas. Ideal para fabricas que entregam vários projetos. Proporciona uma visão gerencial com indicadores de qualidade e prazo de entrega.

## Getting Started

### Prerequisites

Requisitos básicos para a instalação

```
python 3.6+
```

### Installing

Virtualenv

```
pip install virtualenv
```

Criar ambiente virtual dentro de um diretório do projeto

```
virtualenv --python='/usr/local/bin/python3' .venv
```

Clonar o repositório.
Acessar o diretorio onde ficará o projeto e executar o comando

```
git clone https://github.com/prdioliveira/SGTESTE.git
```

Instalando as dependências do proeto

```
pip install requirements/requirements/.txt

Serão instalados:
Django==2.1.3
Pillow==6.2.1
psycopg2==2.7.5
python-http-client==3.2.1
pytz==2019.3
reportlab==3.5.32
selenium==3.141.0
urllib3==1.25.6
```

### Enviar email:

```
Criar as variaveis de ambiente:

EMAIL_HOST=HOST_DO_EMAIL
EMAIL_HOST_PASSWORD=PASSWORD_DO_EMAIL
EMAIL_HOST_USER=ENDERECO_DO_EMAIL
EMAIL_PORT=PORT_SMTP_EMAIL
```


## Running the tests

```
python manage.py test --settings=SGTESTE.settings.teste
```

## Running the project

### Execução inicial
Após a criação da base de testes, conforme settings.local da aplicação, executar os comandos abaixo para a criação das tabelas e carregamento das fixtures do projeto.
*Obs.: Executar apenas uma unica vez*  

```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data.json
```

### Running the project

Para executar o projeto em ambiente local
```
python manage.py runserver 0.0.0.0:8000
```
