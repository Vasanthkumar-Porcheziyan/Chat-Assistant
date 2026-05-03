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
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── LICENSE             # License information
```

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

## 🔧 Integration with LLMs

Currently, the app displays static bot responses. To integrate with a real chatbot or LLM:

1. Replace this line in `main.py`:
   ```python
   bot_response = "This is a static bot response."
   ```

2. With your LLM integration:
   ```python
   bot_response = your_llm_function(user_input)
   ```

Example with OpenAI:
```python
import openai

def get_bot_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message.content

bot_response = get_bot_response(user_input)
```

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

## 📞 Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Built with ❤️ using Streamlit**
