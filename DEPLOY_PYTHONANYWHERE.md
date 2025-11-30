# Guia de Deploy no PythonAnywhere - Nerds de Plantao

## Pre-requisitos

1. Conta no PythonAnywhere (gratuita ou paga)
2. Conhecimentos basicos de terminal Linux
3. Banco de dados PostgreSQL (disponivel apenas em contas pagas) ou MySQL

## Passo 1: Criar uma conta no PythonAnywhere

1. Acesse https://www.pythonanywhere.com
2. Clique em "Pricing & signup"
3. Escolha o plano adequado (recomendado: Hacker ou acima para PostgreSQL)

## Passo 2: Configurar o ambiente

### 2.1 Acessar o console Bash

1. No dashboard, clique em "Consoles"
2. Inicie um novo console "Bash"

### 2.2 Clonar o repositorio

```bash
git clone <url-do-seu-repositorio> nerds-plantao
cd nerds-plantao
```

### 2.3 Criar ambiente virtual

```bash
mkvirtualenv --python=/usr/bin/python3.10 nerdsenv
workon nerdsenv
```

### 2.4 Instalar dependencias

```bash
pip install -r requirements.txt
```

## Passo 3: Configurar o banco de dados

### Opcao A: PostgreSQL (Contas Pagas)

1. Va em "Databases" no dashboard
2. Crie um novo banco PostgreSQL
3. Anote as credenciais fornecidas

### Opcao B: MySQL (Todas as contas)

1. Va em "Databases" no dashboard
2. Inicie o servidor MySQL
3. Crie um banco de dados

Para MySQL, instale o conector:
```bash
pip install pymysql
```

E mude a DATABASE_URL para:
```
mysql+pymysql://username:password@username.mysql.pythonanywhere-services.com/username$databasename
```

## Passo 4: Configurar variaveis de ambiente

1. Crie um arquivo `.env` no diretorio do projeto:

```bash
nano .env
```

2. Adicione as variaveis:

```
DATABASE_URL=postgresql://user:password@host/database
SESSION_SECRET=sua-chave-secreta-muito-longa-e-aleatoria
```

3. Modifique o arquivo `app.py` para carregar o `.env`:

No inicio do arquivo app.py, adicione:
```python
from dotenv import load_dotenv
load_dotenv()
```

E instale o python-dotenv:
```bash
pip install python-dotenv
```

## Passo 5: Configurar o Web App

1. Va em "Web" no dashboard
2. Clique em "Add a new web app"
3. Escolha "Manual configuration" e Python 3.10

### 5.1 Configurar o virtualenv

No campo "Virtualenv", adicione:
```
/home/seu-usuario/.virtualenvs/nerdsenv
```

### 5.2 Configurar o WSGI

Clique no link do arquivo WSGI e substitua o conteudo por:

```python
import sys
import os
from dotenv import load_dotenv

# Caminho do projeto
project_home = '/home/seu-usuario/nerds-plantao'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Carregar variaveis de ambiente
load_dotenv(os.path.join(project_home, '.env'))

# Importar a aplicacao Flask
from app import app as application
```

### 5.3 Configurar arquivos estaticos

Na secao "Static files", adicione:

| URL | Directory |
|-----|-----------|
| /static | /home/seu-usuario/nerds-plantao/static |

## Passo 6: Inicializar o banco de dados

No console Bash:

```bash
workon nerdsenv
cd nerds-plantao
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## Passo 7: Criar usuario admin

O usuario admin eh criado automaticamente na primeira execucao.
Credenciais padrao:
- Email: admin@nerdsplantao.com
- Senha: admin123

**IMPORTANTE**: Altere a senha do admin apos o primeiro login!

## Passo 8: Recarregar o Web App

1. Va em "Web"
2. Clique no botao verde "Reload"
3. Acesse seu site em: https://seu-usuario.pythonanywhere.com

## Configuracoes Adicionais

### Agendar limpeza de sessoes (opcional)

1. Va em "Tasks"
2. Adicione uma tarefa agendada:
```bash
cd /home/seu-usuario/nerds-plantao && /home/seu-usuario/.virtualenvs/nerdsenv/bin/python -c "from app import app, db; print('Maintenance completed')"
```

### Configurar dominio personalizado (Contas Pagas)

1. Va em "Web" > "Add a new domain"
2. Adicione seu dominio
3. Configure o DNS do seu dominio para apontar para PythonAnywhere

### Backup do banco de dados

Para PostgreSQL:
```bash
pg_dump -h host -U user -d database > backup.sql
```

Para MySQL:
```bash
mysqldump -h host -u user -p database > backup.sql
```

## Solucao de Problemas

### Erro 500

1. Verifique os logs de erro em "Web" > "Error log"
2. Verifique se as variaveis de ambiente estao configuradas
3. Verifique se o banco de dados esta acessivel

### Arquivos estaticos nao carregam

1. Verifique a configuracao de arquivos estaticos
2. Confirme que os caminhos estao corretos

### Erro de conexao com banco de dados

1. Verifique as credenciais no arquivo .env
2. Confirme que o banco de dados esta ativo
3. Verifique se o IP do PythonAnywhere esta liberado (se usando banco externo)

## Contato e Suporte

Para duvidas sobre a plataforma "Nerds de Plantao", entre em contato com o administrador.
Para problemas com o PythonAnywhere, consulte a documentacao oficial: https://help.pythonanywhere.com/
