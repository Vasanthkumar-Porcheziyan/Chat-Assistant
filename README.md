# Personal Chat Assistant

A modern, customizable, and open-source chat UI frontend built with Streamlit. This project provides a clean and intuitive chat interface perfect for integrating with chatbot systems, language models, or any conversational AI applications.

## 🌟 Features

- **Modern Chat Interface**: Clean, responsive design with custom message styling
- **User & Bot Message Differentiation**: Distinct visual styling for user and assistant messages
- **Auto-Scroll**: Automatically scrolls to the latest messages during conversation
- **Session State Management**: Maintains chat history throughout the user session
- **Responsive Design**: Messages properly align left (bot) and right (user) with text wrapping for long content
- **Custom Icons**: Beautiful SVG icons for both user and bot avatars
- **Easy Integration**: Simple to integrate with any LLM or chatbot backend

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- NVIDIA API credentials (for LLM integration)
  - `nvidia_base_url`: API endpoint for NVIDIA or compatible service
  - `nvidia_api_key`: Authentication token for the API

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vasanthkumar-Porcheziyan/Chat-Assistant.git
   cd Chat-Assistant
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Choose one of the following methods:

   **Method A: Using `.env.local` file (Recommended for local development)**
   
   Create a `.env.local` file in the project root:
   ```
   NVIDIA_BASE_URL=https://api.nvidia.com/v1/chat
   NVIDIA_API_KEY=your-api-key-here
   ```

   **Method B: Using Streamlit Secrets (Recommended for Streamlit Cloud)**
   
   Create `.streamlit/secrets.toml` in the project root:
   ```toml
   nvidia_base_url = "https://api.nvidia.com/v1/chat"
   nvidia_api_key = "your-api-key-here"
   ```

   **Method C: System Environment Variables**
   
   On Windows (PowerShell):
   ```powershell
   $env:NVIDIA_BASE_URL = "https://api.nvidia.com/v1/chat"
   $env:NVIDIA_API_KEY = "your-api-key-here"
   ```
   
   On macOS/Linux:
   ```bash
   export NVIDIA_BASE_URL="https://api.nvidia.com/v1/chat"
   export NVIDIA_API_KEY="your-api-key-here"
   ```

5. **Add to `.gitignore`** (to prevent committing secrets)
   ```
   .env.local
   .env
   .streamlit/secrets.toml
   ```

## 💻 Usage

1. **Run the application**
   ```bash
   streamlit run main.py
   ```

2. **Access the app**
   - The app will automatically open in your default browser at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in the terminal

3. **Start chatting**
   - Type your message in the input field at the bottom
   - Press Enter or click send to submit your message
   - Your messages appear on the right (purple), bot responses appear on the left (blue)

## 📁 Project Structure

```
Chat-Assistant/
├── main.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
├── .env.local              # Environment variables (local development)
├── .streamlit/
│   └── secrets.toml        # Streamlit cloud secrets (not committed)
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
└── LICENSE                 # License information
```

### Key Files Explained

#### main.py
- `user_message(message)`: Displays user messages aligned to the right with custom styling
- `bot_message(message)`: Displays bot responses aligned to the left
- `generate_bot_response(messages)`: Calls the NVIDIA API to generate AI responses
- `main()`: Main Streamlit app logic handling UI and conversation flow

#### Configuration Files
- `.env.local`: Store sensitive credentials for local development
- `.streamlit/secrets.toml`: Store secrets for Streamlit Cloud deployment
- `requirements.txt`: List of Python package dependencies

## ⚙️ Configuration Details

### Chat History Management

Messages are stored in `st.session_state.chat_history` as a list of tuples:
```python
(message_text: str, is_bot_response: bool)
```

Example structure:
```python
st.session_state.chat_history = [
    ("Let's start chatting! 👇", True),
    ("Hello, how are you?", False),
    ("I'm doing great! How can I help?", True),
]
```

### Message Formatting

Messages use HTML/CSS styling with these properties:
- **Container**: Flexbox layout with gap spacing
- **Message Bubble**: 70% max-width for responsiveness
- **Text Wrapping**: `word-wrap: break-word` prevents overflow
- **Icons**: SVG avatars for visual distinction

## 🎨 UI Customization

### Message Colors
- **User Messages**: Purple (`#63196b`) - right-aligned
- **Bot Messages**: Blue (`#074c85`) - left-aligned
- **Avatar Background**: Orange (`rgb(255, 189, 69)`)

To customize colors, edit the `style` attributes in the `user_message()` and `bot_message()` functions in `main.py`:

```python
# User message background color
style="background-color: #63196b; ..."

# Bot message background color
style="background-color: #074c85; ..."
```

### Adjusting Message Width
The messages are constrained to 70% of the screen width. To change this, modify the `max-width` property:

```python
# In user_message() or bot_message() function
style="...max-width: 70%; ..."  # Change 70% to desired value
```

### Avatar Icons
Both user and bot messages include SVG icons. Replace the SVG `<path>` elements in the functions to customize the icons.

## 🔧 LLM Integration

This application is pre-configured to work with NVIDIA API endpoints using the `google/gemma-2-2b-it` model. The integration uses the OpenAI Python client library to communicate with NVIDIA's API.

### Current Configuration

The bot uses the following settings:
```python
{
    "model": "google/gemma-2-2b-it",
    "temperature": 0.2,      # Lower = more deterministic
    "top_p": 0.7,           # Nucleus sampling
    "max_tokens": 1024      # Maximum response length
}
```

### Modifying the Model or Parameters

Edit the `generate_bot_response()` function in `main.py`:

```python
def generate_bot_response(messages):
    client = OpenAI(
        base_url=os.getenv("NVIDIA_BASE_URL"),
        api_key=os.getenv("NVIDIA_API_KEY")
    )

    completion = client.chat.completions.create(
        model="your-model-name",          # Change model here
        messages=messages,
        temperature=0.5,                  # Adjust (0.0-2.0)
        top_p=0.7,                        # Adjust (0.0-1.0)
        max_tokens=2048,                  # Change max response length
        stream=True
    )
    
    bot_response = ""
    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            bot_response += chunk.choices[0].delta.content
    return bot_response
```

### Using a Different LLM Provider

To use OpenAI, Anthropic, or other providers:

```python
# For OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
# Model calls would use "gpt-3.5-turbo", "gpt-4", etc.

# For Anthropic
from anthropic import Anthropic
client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
# Use their API format instead
```

### API Parameter Reference

- **temperature** (0.0 - 2.0): Controls randomness
  - Lower (0.1-0.3): More focused and deterministic
  - Higher (0.7-1.5): More creative and diverse
  
- **top_p** (0.0 - 1.0): Nucleus sampling
  - Lower values: More conservative responses
  - Higher values: More diverse responses
  
- **max_tokens**: Maximum length of generated response
  - Adjust based on your use case and API limits

## 📊 Chat History

The application maintains chat history during the session using Streamlit's `session_state`. Messages are stored as tuples:
```python
(message_text, is_bot_response: bool)
```

To persist chat history across sessions, you can:
- Save to a file (JSON, CSV)
- Use a database (SQLite, PostgreSQL)
- Integrate with cloud storage

## 🎯 Future Enhancements

- [ ] Persistent chat history (database integration)
- [ ] Multiple conversation threads
- [ ] Message editing and deletion
- [ ] Export chat history
- [ ] User authentication
- [ ] Voice input/output support
- [ ] File upload and sharing in chat
- [ ] Dark/Light theme toggle
- [ ] Typing indicators
- [ ] Message search functionality

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs by opening an issue
- Submit pull requests with improvements
- Suggest new features
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Tips & Tricks

- **Speed Up Loading**: Streamlit caches functions by default. Use `@st.cache_data` decorator for expensive operations
- **Debugging**: Run with `streamlit run main.py --logger.level=debug` for verbose output
- **Custom Styling**: Streamlit supports HTML and CSS. Extend the styling in the markdown functions as needed
- **Streaming Responses**: The bot response uses streaming for real-time output display
- **Message Persistence**: Chat history is stored in Streamlit's session state but clears on app restart

## 🐛 Troubleshooting

### API Connection Issues

**Error: "API key not found" or "Missing credentials"**
- Verify `.env.local` file exists in project root
- Check that environment variable names match exactly (case-sensitive)
- Restart the Streamlit app after updating environment variables
- Confirm your API key is valid and hasn't expired

### ImportError: "No module named 'openai'"

```bash
pip install --upgrade openai
```

### Streamlit Secrets Not Loading

If using `.streamlit/secrets.toml`:
- Ensure the file is in the `.streamlit/` directory (create if missing)
- Reload the page or restart Streamlit: `streamlit run main.py --logger.level=debug`
- Check TOML syntax (spaces, quotes, special characters)

### Environment Variables Not Recognized

**On Windows:**
```powershell
# Set permanently (will persist across sessions)
[Environment]::SetEnvironmentVariable("NVIDIA_API_KEY", "your-key", "User")

# Then restart PowerShell or Python
```

**On macOS/Linux:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export NVIDIA_BASE_URL="..."
export NVIDIA_API_KEY="..."

# Then run: source ~/.bashrc
```

### Chat Not Responding

1. Check if API credentials are set correctly
2. Verify API endpoint URL is correct
3. Check your API quota and usage limits
4. Review logs: `streamlit run main.py --logger.level=debug`
5. Test API connection separately:
   ```python
   from openai import OpenAI
   import os
   
   client = OpenAI(
       base_url=os.getenv("NVIDIA_BASE_URL"),
       api_key=os.getenv("NVIDIA_API_KEY")
   )
   
   response = client.chat.completions.create(
       model="google/gemma-2-2b-it",
       messages=[{"role": "user", "content": "Hello"}],
       max_tokens=100
   )
   print(response.choices[0].message.content)
   ```

## 📦 Dependencies

The project uses the following main dependencies:

- **streamlit** (>=1.0.0): Web framework for building the chat UI
- **openai** (>=1.0.0): Client library for OpenAI-compatible APIs
- **python-dotenv** (>=0.19.0): Load environment variables from `.env.local`

View all dependencies:
```bash
pip list
```

Update specific package:
```bash
pip install --upgrade openai
```

## 🚀 Deployment

### Streamlit Cloud

1. Push your repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set secrets in the app settings:
   - Go to Settings → Secrets
   - Add `nvidia_base_url` and `nvidia_api_key`
5. Deploy!

### Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t chat-assistant .
docker run -p 8501:8501 -e NVIDIA_API_KEY="your-key" -e NVIDIA_BASE_URL="your-url" chat-assistant
```

### Self-Hosted Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run on specific host/port
streamlit run main.py --server.port 8080 --server.address 0.0.0.0
```

## 📞 Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Built with ❤️ using Streamlit**
