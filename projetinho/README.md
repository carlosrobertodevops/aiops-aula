# projetinho

Quickstart para preparar o ambiente, validar o projeto e rodar localmente.

## Requisitos

- Python 3.14+

## Quickstart

### Copiar e colar (bootstrap completo)

```bash
python3 -m venv .venv
. .venv/bin/activate
cp .env.example .env
export DJANGO_SECRET_KEY="$(grep '^DJANGO_SECRET_KEY=' .env | cut -d'=' -f2-)"
python -m pip install --upgrade pip
python -m pip install django
python manage.py check
python manage.py migrate
python manage.py runserver
```

### Copy and paste (full bootstrap)

```bash
python3 -m venv .venv
. .venv/bin/activate
cp .env.example .env
export DJANGO_SECRET_KEY="$(grep '^DJANGO_SECRET_KEY=' .env | cut -d'=' -f2-)"
python -m pip install --upgrade pip
python -m pip install django
python manage.py check
python manage.py migrate
python manage.py runserver
```

### 1) Criar ambiente virtual e instalar dependencias

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install django
```

### 2) Validar o projeto

```bash
. .venv/bin/activate
python manage.py check
```

Se o comando retornar `exit code 0`, o ambiente esta pronto.

### 3) Rodar localmente

```bash
. .venv/bin/activate
python manage.py runserver
```

## Comandos uteis

```bash
. .venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
```

## Troubleshooting

### ModuleNotFoundError: No module named 'django'

```bash
. .venv/bin/activate
python -m pip install django
```

### .venv/bin/activate nao encontrado

```bash
python3 -m venv .venv
. .venv/bin/activate
```

### Erro de permissao ao instalar pacote

```bash
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install django
```
