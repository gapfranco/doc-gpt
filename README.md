# PROJETO DOC-GPT

O DocGPT é uma aplicação web desenvolvida com Django e uma API de inteligência artificial.
Este sistema permite que usuários façam upload de seus documentos e realizem consultas sobre estes documentos
utilizando técnicas avançadas de processamento de linguagem natural.
O sistema também oferece funcionalidades para compartilhar seletivamente partes dos documentos
na internet para usuários convidados.

## Características

- **Upload de Documentos**: Os usuários podem fazer upload de documentos em formatos comuns como PDF, DOCX, e TXT.
- **Consulta Inteligente**: Utilize a API de inteligência artificial para consultar informações específicas nos documentos armazenados.
- **Compartilhamento Seletivo**: Possibilidade de compartilhar partes dos documentos na web, acessíveis por meio de links gerados.
- **Interface Amigável**: Interface de usuário clara e responsiva para uma experiência de usuário aprimorada.
- **Segurança Robusta**: Autenticação de usuários e controle de acesso para garantir a segurança dos documentos.

## Tecnologias Utilizadas

- **Backend**: Django, Django REST Framework
- **Frontend**: HTMX (permite interações dinâmicas sem JavaScript completo)
- **IA**: Integração com `langchain`, OpenAI, Google Cloud NLP
- **Banco de Dados**: PostgreSQL, SQLite (para desenvolvimento)
- **Processamento assíncrono** - Celery para tarefas em background
- **Deploy**: fly.io

## Configuração Inicial

### Pré-requisitos

- Python 3.12
- Poetry (opcional, mas recomendado)
- pip e Virtualenv (opções para o poetry)

### Configuração do Ambiente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/document-query-assistant.git
   cd document-query-assistant
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   poetry shell
   ```

3. Instale as dependências:
   ```bash
   poetry install
   ```

4. Configure o ambiente copiando o arquivo .env.model para .env e ajuste as
   variáveis:
   - DATABASE_URL: url de conexão com o banco de dados
   - OPENAI_API_KEY: chave de API da OpenAI a utilizar
   - SERVER_EMAIL: Endereço de e-mail do remetendo de e-mails
   - EMAIL_*: Serviço de e-mail
   - REDIS_URL: Endereço do Redis
   - VECTOR_DB: Vector database a usar para embeddings (qdrant ou supabase)
   - SUPABASE_URL: Url do supabase (se opção supabase de VECTOR_DB)
   - SUPABASE_SERVICE_KEY= Service key do supabase  (se opção supabase de VECTOR_DB)
   - QDRANT_PATH=local_qdrant (Para usar qdrant local em desenvolvimento)
   - QDRANT_URL= url do serviço QDrant (se opção qdrant de VECTOR_DB)
   - QDRANT_KEY= qdrant key (se opção qdrant de VECTOR_DB)

5. Configure o banco de dados (ajustes no `settings.py` se necessário) e execute as migrações:
   ```bash
   python manage.py migrate
   ```

6. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

7. Inicie o celery worker local:
   ```bash
   task worker
   ```

8. Inicie o celery flower local:
   ```bash
   task flower
   ```

9. Acesse `http://localhost:8000` no seu navegador.


## Como Contribuir

Contribuições são bem-vindas, e qualquer ajuda é muito apreciada. Veja como você pode contribuir:

1. Fork o projeto no GitHub.
2. Clone seu fork para sua máquina local.
3. Crie uma branch para sua nova feature ou correção de bug.
4. Faça suas alterações.
5. Envie um pull request após rebase com a branch principal.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

- Nome do Mantenedor - [email@exemplo.com](mailto:email@exemplo.com)
- Projeto Link: [https://github.com/seu-usuario/document-query-assistant](https://github.com/seu-usuario/document-query-assistant)
