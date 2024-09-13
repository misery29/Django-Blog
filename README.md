
# AluGol

AluGol é um sistema de aluguel de campos, desenvolvido como parte de um projeto full-stack da DMS em colaboração com a Universidade de Vassouras. Utiliza Django e Docker com PostgreSQL.
## Funcionalidades

- Criação e Autenticação de Usuários: Cadastro e login via Django Allauth, com suporte para autenticação social e dois fatores (MFA).
- Pesquisa e Reserva de Campos: Usuários podem pesquisar e filtrar campos, fazer reservas e comentar após a reserva. É possível cancelar reservas não confirmadas e um comentário por campo é permitido por usuário.
- Histórico de Reservas: Visualização das reservas passadas dos usuários.
- Administração: Administradores podem gerenciar campos, reservas e avaliações, além de gerar relatórios de receitas em PDF ou CSV no painel do Django Admin.
- Mapas: Exibição das localizações dos campos em mapas, com uma visão geral da localização atual do usuário e campos próximos.
- Notificações: Emails enviados a administradores para novas reservas e comentários.
- Segurança: Todas as conexões são feitas via HTTPS, com um contêiner Nginx como proxy reverso.


Geocodificação

- API do Google Maps: Determina automaticamente as coordenadas dos endereços dos campos.


## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env:

DB_ENGINE="django.db.backends.postgresql"

POSTGRES_DB="blog_base_de_dados"

POSTGRES_USER="blog_user"

POSTGRES_PASSWORD="bloguserpassword"

POSTGRES_HOST="psql"

POSTGRES_PORT="5432"

EMAIL_HOST_PASSWORD = "xdja ifdf nypc nhwg"

EMAIL_HOST_USER = "joao.alugol@gmail.com"

## Rodando localmente

Clone o projeto

```bash
https://github.com/misery29/Django-Blog
```

Crie uma pasta "dotenv_files" na raíz do projeto

```bash
  mkdir dotenv_files
```

Crie um arquivo ".env" com as variáveis de ambiente 


Inicialize o docker compose pra rodar o projeto

```bash
  docker compose up --build
```
