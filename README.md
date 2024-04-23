# DOC-GPT

DOC-GPT is a web application developed using Django and an artificial intelligence API.
This system allows users to upload their documents and perform queries on these documents
using advanced natural language processing techniques.
The system also provides functionalities to selectively share parts of the documents
on the internet for invited users.

## Features

- **Document Upload**: Users can upload documents in common formats such as PDF, DOCX, and TXT.
- **Smart Query**: Use the artificial intelligence API to query specific information in the stored documents.
- **Selective Sharing**: Ability to share parts of the documents on the web, accessible via invites.
- **User-Friendly Interface**: Clear and responsive user interface for an enhanced user experience.
- **Robust Security**: User authentication and access control to ensure document security.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Frontend**: HTMX (allows dynamic interactions without full JavaScript)
- **AI**: Integration with `langchain`, OpenAI and other AI models
- **Database**: PostgreSQL, SQLite (for development)
- **Asynchronous Processing**: Celery for background tasks

## Highlights

1. The entire frontend was developed using only HTML without JavaScript, using Tailwind and the HTMX framework.
2. The processing of splitting and embedding the texts, which can be time-consuming, runs
   in background using asynchronous processing with Celery.
3. Using **taskipy** to aid development, with commands:
   - task worker - Starts the celery worker
   - task flower - Starts the celery flower
   - task pre - Runs pre_commit to analyze files
   - task coverage - Runs the test coverage
   - task test - Runs the unit tests
   - task tailwind_watch - Runs the tailwind watch process
   - task tailwind_minify - Runs the tailwind minify process
4. Can be adapted for deployment on any service that supports Django and Celery.
   The *Dockerfile* and *fly.toml* included implement deployment on fly.io (https://fly.io).

## Initial Setup

### Prerequisites

- Python 3.12
- Poetry (optional, but recommended)
- pip and Virtualenv (alternatives to poetry)

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/document-query-assistant.git
   cd document-query-assistant
   ```

2. Create a virtual environment and activate it:
   ```bash
   poetry shell
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Configure the environment by copying the .env.model file to .env and adjust the variables:
   - DATABASE_URL: database connection URL
   - OPENAI_API_KEY: OpenAI API key to use
   - SERVER_EMAIL: Email address of the sender
   - EMAIL_*: Email service
   - REDIS_URL: Redis address
   - VECTOR_DB: Vector database to use for embeddings (qdrant or supabase)
   - SUPABASE_URL: Supabase URL (if supabase option of VECTOR_DB)
   - SUPABASE_SERVICE_KEY: Service key of supabase (if supabase option of VECTOR_DB)
   - QDRANT_PATH: local_qdrant (To use local qdrant in development)
   - QDRANT_URL: QDrant service URL (if qdrant option of VECTOR_DB)
   - QDRANT_KEY: qdrant key (if qdrant option of VECTOR_DB)

5. Set up the database (adjust in `settings.py` if necessary) and run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Start the local celery worker:
   ```bash
   task worker
   ```

8. Start the local celery flower:
   ```bash
   task flower
   ```

9. Access `http://localhost:8000` in your browser.

## License

This project is distributed under the MIT license. See the `LICENSE` file for more details.

## Contact

- Gonçalo Franco - [gapfranco@gmail.com](mailto:gapfranco@gmail.com)
- Project Link: [https://github.com/gapfranco/docgpt](https://github.com/gapfranco/docgpt)
