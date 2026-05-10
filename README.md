# 🤖 Personal Chat Assistant

A premium, **dark-mode AI chat assistant** built with [Streamlit](https://streamlit.io/), powered by the [NVIDIA AI Endpoints](https://www.nvidia.com/en-us/ai/) via the OpenAI-compatible API. Features persistent chat history backed by a local PostgreSQL database.

---

## ✨ Features

- 🎨 **Premium Dark UI** — Dark-mode interface with gradient headers, styled message bubbles, and a polished glassmorphism aesthetic
- 💬 **Multi-turn Conversations** — Full chat history maintained per session, ordered by timestamp
- 📋 **Persistent History** — All sessions and messages stored in PostgreSQL (`chat_sessions` & `chat_messages` tables)
- 🗂️ **Session Management** — Each new chat creates a dedicated session; clicking any history item in the sidebar restores the full conversation
- 🤖 **Multi-Model Support** — Switch between multiple NVIDIA-hosted LLMs from the sidebar
- ⚙️ **Configurable LLM Parameters** — Tune Temperature, Top-P, Max Tokens, Frequency Penalty, and Presence Penalty via the sidebar or settings modal
- 💡 **Welcome Screen with Suggestions** — Quick-start prompt chips on app load for new chats

---

## 🗂️ Project Structure

```
Chat-Assistant/
├── main.py                         # App entry point — Streamlit page config, DB init, main chat loop
│
├── components/
│   ├── header.py                   # Renders the top header bar
│   ├── sidebar.py                  # Sidebar: New Chat, session history list, model & settings controls
│   ├── chat_area.py                # Welcome screen, user/bot message renderers, chat history display
│   └── settings_modal.py          # Advanced LLM settings dialog (st.dialog)
│
├── services/
│   ├── connect_postgresdb.py       # PostgreSQL connection (st.connection) & table initialization
│   ├── chat_manager.py             # Session & message CRUD: create_new_chat, add_message, get_current_history
│   └── llm_service.py             # NVIDIA/OpenAI API client & generate_bot_response()
│
├── styles/
│   └── dark_theme.css             # Custom CSS — dark theme, message bubbles, animations
│
├── .streamlit/
│   ├── config.toml                 # Streamlit theme configuration
│   └── secrets.toml               # PostgreSQL connection credentials (gitignored)
│
├── .env.local                      # NVIDIA API key & base URL (gitignored)
└── requirements.txt               # Python dependencies
```

---

## 🗄️ Database Schema

The app uses two PostgreSQL tables:

```sql
CREATE TABLE chat_sessions (
    session_id   UUID PRIMARY KEY,
    user_id      UUID,
    building_id  UUID,
    title        TEXT,
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    updated_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE chat_messages (
    message_id  BIGSERIAL PRIMARY KEY,
    session_id  UUID REFERENCES chat_sessions(session_id),
    role        TEXT NOT NULL,          -- 'user' | 'assistant'
    message     TEXT NOT NULL,
    metadata    JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

Tables are created automatically on app startup if they don't already exist.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (local instance running)
- NVIDIA API key — [Get one here](https://build.nvidia.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/Vasanthkumar-Porcheziyan/Chat-Assistant.git
cd Chat-Assistant
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv myenv

# Windows
myenv\Scripts\activate

# macOS / Linux
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env.local` file in the project root:

```env
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### 5. Configure PostgreSQL Connection

Create `.streamlit/secrets.toml`:

```toml
[connections.postgresql]
dialect = "postgresql"
host = "localhost"
port = "5432"
database = "chatbot"
username = "postgres"
password = "your_postgres_password"
```

> **Note**: Make sure the `chatbot` database already exists in your local PostgreSQL server. The app will create the required tables automatically on first run.

### 6. Run the App

```bash
python -m streamlit run main.py
```

Open your browser at `http://localhost:8501`.

---

## 🧠 Architecture Overview

```
User Input (st.chat_input)
        │
        ▼
main.py — orchestrates the flow
        │
        ├──► chat_manager.create_new_chat()   ──► INSERT INTO chat_sessions
        │
        ├──► chat_manager.add_message()       ──► INSERT INTO chat_messages (role='user')
        │
        ├──► llm_service.generate_bot_response()  ──► NVIDIA API (streaming)
        │
        └──► chat_manager.add_message()       ──► INSERT INTO chat_messages (role='assistant')
                                                        + UPDATE chat_sessions.updated_at
```

**Sidebar history** queries `chat_sessions` ordered by `created_at DESC`. Clicking a session sets `st.session_state.current_chat_id` and triggers a rerun, loading the full conversation from `chat_messages` ordered by `created_at ASC`.

---

## ⚙️ LLM Settings

| Parameter | Default | Description |
|---|---|---|
| Temperature | `0.2` | Controls randomness — lower is more deterministic |
| Top-P | `0.7` | Nucleus sampling — lower focuses on likely tokens |
| Max Tokens | `1024` | Maximum response length |
| Frequency Penalty | `0.0` | Penalizes repeated tokens |
| Presence Penalty | `0.0` | Encourages exploring new topics |

---

## 🤖 Supported Models

| Model | Provider |
|---|---|
| `google/gemma-2-2b-it` | Google (default) |
| `nvidia/nemotron-3-super-120b-a12b:free` | NVIDIA |
| `meta/llama-3.1-8b-instruct` | Meta |
| `microsoft/phi-3-mini-128k-instruct` | Microsoft |
| `anthropic/claude-3-haiku` | Anthropic |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | [Streamlit](https://streamlit.io/) |
| LLM API | [NVIDIA AI Endpoints](https://build.nvidia.com/) (OpenAI-compatible) |
| Database | PostgreSQL via `st.connection` + SQLAlchemy |
| DB Driver | `psycopg2-binary` |
| Styling | Custom CSS (dark theme) |
| Environment | `python-dotenv` |

---

## 📁 Key Files Reference

| File | Purpose |
|---|---|
| `main.py` | App entrypoint, DB init, chat loop |
| `services/connect_postgresdb.py` | DB connection & schema initialization |
| `services/chat_manager.py` | All session & message DB operations |
| `services/llm_service.py` | LLM API call logic |
| `components/sidebar.py` | Sidebar with history & settings |
| `components/chat_area.py` | Chat message rendering |
| `.streamlit/secrets.toml` | PostgreSQL credentials |
| `.env.local` | NVIDIA API credentials |

---

## 🔒 Security Notes

- Never commit `.env.local` or `.streamlit/secrets.toml` — both are listed in `.gitignore`
- Use environment variables or secrets management in production deployments

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
