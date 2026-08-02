# AI Chatbot Application with Memory

## Tech Stack & Architecture
- **Frontend & UI:** Streamlit (`frontend.py`)
- **Authentication:** Streamlit Auth (Google OIDC) configured dynamically via `entrypoint.sh`
- **Orchestration & LLM:** LangChain, LangChain-OpenRouter (`modelmain.py`)
- **Short-Term Memory:** Redis (`langchain-redis`)
- **Long-Term Persistence:** MongoDB (`db.py`)
- **Containerization:** Docker (`dockerfile`) & Docker Compose (`docker-compose.yaml`)

## Project Files Summary
- `db.py`: Manages MongoDB database connections, inserts chat session history, fetches history filtered by `session_id` and `user_email`, and retrieves unique user session lists.
- `frontend.py`: Renders the Streamlit chat interface, handles Google OIDC login/logout state checks, manages session state, and synchronizes chat logs with MongoDB.
- `modelmain.py`: Encapsulates the LangChain pipeline (`RedisModel`), configuring Redis chat history and streaming responses from the OpenRouter LLM (`poolside/laguna-xs-2.1:free`).
- `entrypoint.sh`: Shell script that programmatically generates `/app/.streamlit/secrets.toml` from environment variables before launching Streamlit.
- `dockerfile`: Python 3.10 slim base image, copies project files, installs dependencies from `requirements.txt`, and sets `entrypoint.sh` as the container entrypoint.
- `docker-compose.yaml`: Orchestrates the Redis container (`redis:latest`) and Streamlit application container with all required environment variables (`MONGO_URI`, `OPENROUTER_API_KEY`, `REDIS_URL`, `OIDC_*`).
- `requirements.txt`: Project package dependencies (`langchain`, `langchain-core`, `langchain-openrouter`, `pymongo`, `langchain-redis`, `streamlit`, `streamlit[auth]`).

Access: `http://3.110.48.106.nip.io:8501`
