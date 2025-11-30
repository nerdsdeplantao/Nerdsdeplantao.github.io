# Nerds de Plantao - Plataforma EAD

## Visao Geral

Plataforma de ensino a distancia (EAD) para curso de reforco medico, desenvolvida em Flask/Python. O sistema oferece videoaulas, simulados interativos, materiais complementares e painel administrativo completo.

## Tecnologias

- **Backend**: Flask 3.0 (Python)
- **Banco de Dados**: PostgreSQL (via SQLAlchemy)
- **Autenticacao**: Flask-Login com aprovacao manual de cadastros
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Design**: Mobile-first, responsivo, paleta azul/roxo/verde

## Estrutura do Projeto

```
/
├── app.py                 # Aplicacao principal Flask
├── extensions.py          # Extensoes (db, login_manager, csrf)
├── models.py              # Modelos do banco de dados
├── forms.py               # Formularios WTForms
├── routes/
│   ├── auth.py           # Rotas de autenticacao
│   ├── main.py           # Rotas principais
│   ├── admin.py          # Painel administrativo
│   ├── videos.py         # Videoaulas
│   ├── simulados.py      # Simulados/Quizzes
│   └── materiais.py      # Materiais complementares
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── auth/             # Login, registro
│   ├── admin/            # Painel admin
│   ├── videos/           # Videoaulas
│   ├── simulados/        # Simulados
│   └── materiais/        # Materiais
├── static/
│   ├── css/style.css     # Estilos CSS
│   └── js/main.js        # JavaScript
├── uploads/              # Arquivos enviados
├── requirements.txt      # Dependencias Python
└── DEPLOY_PYTHONANYWHERE.md  # Guia de deploy
```

## Modelos de Dados

- **User**: Usuarios com sistema de aprovacao
- **Discipline**: Disciplinas do curso
- **Module**: Modulos dentro de cada disciplina
- **VideoLesson**: Aulas em video (YouTube/Vimeo)
- **Material**: Materiais complementares (PDFs, links)
- **Quiz**: Simulados com limite de tempo
- **Question**: Questoes de multipla escolha
- **QuizAttempt**: Tentativas de simulados
- **UserProgress**: Progresso do usuario nas aulas

## Funcionalidades

### Alunos
- Login com aprovacao manual do admin
- Dashboard com estatisticas de progresso
- Videoaulas organizadas por disciplina/modulo
- Simulados com cronometro e correcao automatica
- Materiais complementares para download
- Historico de simulados realizados

### Administradores
- Gestao de usuarios (aprovar, bloquear)
- CRUD de disciplinas, modulos, aulas
- Upload de materiais
- Criacao de simulados com questoes
- Visualizacao de estatisticas

## Credenciais Padrao

- **Admin**: admin@nerdsplantao.com / admin123

## Comandos Uteis

```bash
# Executar localmente
python app.py

# Executar em producao
gunicorn --bind 0.0.0.0:5000 app:app
```

## Deploy

O projeto esta otimizado para deploy no PythonAnywhere.
Consulte o arquivo `DEPLOY_PYTHONANYWHERE.md` para instrucoes detalhadas.

## Preferencias de Desenvolvimento

- Codigo em ingles, interface em portugues brasileiro
- Mobile-first responsive design
- Paleta de cores: branco, azul (#3b82f6), roxo (#7c3aed), verde (#10b981)
- Sem uso de emojis no codigo
- Modulos separados por funcionalidade

## Alteracoes Recentes

- **30/11/2025**: Criacao inicial da plataforma completa
  - Sistema de autenticacao com aprovacao manual
  - Modulo de videoaulas com player embed
  - Sistema de simulados interativos
  - Materiais complementares
  - Painel administrativo
  - Design responsivo mobile-first
