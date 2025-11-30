# Tutorial Simples - PythonAnywhere GRÁTIS

## O que você precisa fazer em 5 passos

### PASSO 1: Criar conta (5 minutos)

1. Vá para https://www.pythonanywhere.com
2. Clique em "Sign up now"
3. Escolha "Beginner" (é grátis)
4. Preencha o formulário com seus dados
5. Confirme o email

**Pronto! Você tem uma conta.**

---

### PASSO 2: Fazer upload dos arquivos (10 minutos)

Depois que criar a conta:

1. Você vai ver um painel chamado "Dashboard"
2. No lado esquerdo, procure por "Files"
3. Clique em "Files"
4. Vá para a pasta "mysite"
5. Delete tudo que tiver lá (arquivos que não são seus)

Agora você precisa copiar seus arquivos do Replit:

6. Abra uma aba com o Replit (seu projeto)
7. Veja a lista de arquivos à esquerda
8. Selecione e copie estes arquivos:
   - `app.py`
   - `extensions.py`
   - `models.py`
   - `forms.py`
   - `requirements.txt`
   - Pasta `routes` (com auth.py, admin.py, etc)
   - Pasta `templates` (com todos os HTML)
   - Pasta `static` (com CSS e JavaScript)

9. No PythonAnywhere, faça upload deles na pasta "mysite"

**Pronto! Seus arquivos estão lá.**

---

### PASSO 3: Instalar dependências (10 minutos)

1. No PythonAnywhere, procure por "Consoles" (no topo)
2. Clique em "Bash"
3. Digite estes comandos (um por um, aperte Enter):

```bash
pip install flask flask-login flask-sqlalchemy flask-wtf email-validator trafilatura werkzeug
```

Espere terminar (pode levar alguns minutos).

**Pronto! Tudo instalado.**

---

### PASSO 4: Configurar o Banco de Dados (5 minutos)

O plano gratuito do PythonAnywhere vem com SQLite (banco de dados simples).

Você não precisa fazer NADA! O código já funciona com ele.

---

### PASSO 5: Ativar o Web App (10 minutos)

1. Volte ao Dashboard
2. Procure por "Web" (no topo)
3. Clique em "Add a new web app"
4. Quando pedir, escolha:
   - "Manual configuration"
   - Python 3.10
5. Clique em "Next"

Agora você vai ver um arquivo chamado "WSGI" na página:

6. Clique no link WSGI (geralmente na cor azul)
7. Delete TUDO que estiver no arquivo
8. Cole isto:

```python
import sys
import os

# Caminho para seus arquivos
path = '/home/seu-usuario/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Importar sua aplicação
from app import app as application
```

**IMPORTANTE:** Mude "seu-usuario" para o nome de usuário que você criou no PythonAnywhere!

9. Clique em "Save"
10. Volte para a página de Web
11. Procure pelo botão verde "Reload" e clique nele

**PRONTO! Sua plataforma está ONLINE!**

---

## Como acessar sua plataforma

Depois que clicar em Reload, você vai ver um link tipo:

```
https://seu-usuario.pythonanywhere.com
```

Clique neste link!

---

## Fazer login

Use estas credenciais:
- **Email:** admin@nerdsplantao.com
- **Senha:** admin123

---

## Problemas comuns

### "Error 500" ou "502 Bad Gateway"

Significa que algo deu errado. Para descobrir o quê:

1. Vá em "Web"
2. Procure por "Error log"
3. Leia o que está escrito (geralmente diz o problema)
4. Comum: Você digitou errado o "seu-usuario" no arquivo WSGI

### Arquivo não encontrado

Verifique que os arquivos estão MESMO na pasta "mysite" (use "Files" para confirmar)

### "Database locked"

Ignore isso. É normal no SQLite (banco de dados gratuito).

---

## Próximos passos

Depois que funcionar, você pode:

1. Criar mais contas de alunos
2. Adicionar disciplinas, videoaulas, simulados
3. Usar o painel de admin para gerenciar tudo

---

## Se tiver dúvida

Chama! A gente resolve junto.
