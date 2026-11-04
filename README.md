# IFNet — estudos de Redes de Computadores

Site de estudos desenvolvido com Python, Flask, SQLite e Bootstrap. O professor pode cadastrar, editar e excluir conteúdos, vídeos e exercícios. Estudantes podem visualizar os materiais.

## Requisitos
- Python 3.10 ou superior
- Acesso à internet para carregar Bootstrap e ícones do CDN

## Como executar no Windows (VS Code)

Abra o terminal na pasta `projeto_flask_sbadmin` e execute:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Acesse `http://127.0.0.1:5000` no navegador. O arquivo SQLite será criado automaticamente em `instance/ifnet.db`.

## Primeira conta
A primeira conta cadastrada recebe o perfil de professor/administrador. Todas as contas seguintes são estudantes. Por isso, cadastre primeiro a conta do professor. O professor pode alterar perfis no menu Administração → Gerenciar usuários.

## Funções
- Cadastro e login com senha protegida por hash.
- Página inicial com atalhos para conteúdos, vídeos e exercícios.
- Área administrativa para criar, editar e excluir materiais.
- Área administrativa para alterar o perfil dos usuários.
- SQLite local, sem necessidade de instalar ou configurar MySQL.

## Estrutura principal

```text
projeto_flask_sbadmin/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   └── static/
├── instance/          # banco SQLite criado automaticamente
├── config.py
├── requirements.txt
└── run.py
```

## Observação importante
Este projeto é uma base escolar/de desenvolvimento. Antes de publicar na internet, configure uma `SECRET_KEY` forte, revise a criação da primeira conta administrativa e utilize HTTPS.
