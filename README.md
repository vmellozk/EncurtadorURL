# 🔗 Encurtador de URL

Este é um projeto simples de **Encurtador de URL** desenvolvido utilizando **Flask**, **PyMySQL** e **SQLAlchemy**. O objetivo do projeto é criar uma aplicação web onde o usuário pode encurtar URLs longas e acessá-las de forma mais prática e curta.

## ✨ Funcionalidades

- **Encurtar URL**: O usuário insere uma URL longa e recebe uma versão encurtada.
- **Redirecionamento**: O usuário pode acessar a URL encurtada e será redirecionado para a URL original.
- **Histórico de URLs**: O usuário pode visualizar um histórico de URLs encurtadas.

## 🛠️ Tecnologias Utilizadas

- **Flask**: Framework web para desenvolvimento da aplicação.
- **PyMySQL**: Conector MySQL para Python.
- **SQLAlchemy**: ORM para manipulação de banco de dados.

## 🎬 Demonstração do Projeto (Vídeo)

[![Assista à apresentação no YouTube](https://img.youtube.com/vi/M-yneh7qwiU/maxresdefault.jpg)](https://www.youtube.com/watch?v=M-yneh7qwiU)

## ✅ Requisitos

Antes de começar, certifique-se de ter o seguinte instalado:

- Python 3.x
- MySQL ou MariaDB
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/encurtador-url.git
cd encurtador-url
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use venv\Scripts\activate
```

3. Ative o ambiente virtual:

```bash
./venv/scripts/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Configure o banco de dados MySQL:

- Crie um banco de dados no MySQL (por exemplo, encurtador_db).
- No arquivo config.py, configure as credenciais do banco de dados:

```bash
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:senha@localhost/encurtador_db'
```

6. Crie as tabelas no banco de dados:

```bash
python
>>> from app import db
>>> db.create_all()
```

7. Execute a aplicação Flask:

```bash
python app.py
```

## 📁 Estrutura do Projeto

```php
encurtador-url/
│
├── app.py                  # Arquivo principal da aplicação Flask
├── config.py               # Configurações do banco de dados
├── models.py               # Definição dos modelos (tabelas do banco)
├── requirements.txt        # Dependências do projeto
├── templates/              # Templates HTML
│   └── index.html          # Página principal
└── static/                 # Arquivos estáticos (CSS, JS, imagens)
    └── style.css           # Estilo para a aplicação
```

## 🤝 Contribuição

Se você deseja contribuir com este projeto, siga as etapas abaixo:

- Faça um fork deste repositório.
- Crie uma branch com a sua feature: git checkout -b minha-feature.
- Faça commit das suas mudanças: git commit -am 'Adiciona nova feature'.
- Envie para o seu repositório: git push origin minha-feature.
- Abra um pull request.

## 📄 Licença

Este projeto está licenciado sob a MIT License. O arquivo 'LICENSE' será disponibilizado para mais informações.
