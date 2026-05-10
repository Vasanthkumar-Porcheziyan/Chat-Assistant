# Chat Assistant Enhancement Plan

## Overview
This plan outlines the steps to enhance the existing chat assistant with:
1. Conversation history persistence (already partially implemented)
2. Model selection dropdown in sidebar
3. Settings modal for advanced parameters (temperature, top_p, max_tokens, etc.)
4. Proper component-based architecture
5. Responsive Design & Layout Adjustments
6. Production Ready Code & Structure

## Current State Analysis
The existing `main.py` contains:
- Basic chat UI with user/bot message styling
- Session state management for chat history
- Integration with NVIDIA API using OpenAI client
- Hardcoded model parameters (google/gemma-2-2b-it, temperature=0.2, top_p=0.7, max_tokens=1024)

## Component Structure to Implement

### 1. Header Component (`components/header.py`)
- Application title
- Settings button to trigger modal
- State management for settings modal visibility

### 2. Sidebar Component (`components/sidebar.py`)
- Model selection dropdown
- Display of current model info
- Collapsible/expandable section for quick settings

### 3. Settings Modal Component (`components/settings_modal.py`)
- Modal dialog for advanced LLM parameters
- Temperature slider (0.0-2.0)
- Top-p slider (0.0-1.0)
- Max tokens selector
- Model-specific parameters (if applicable)
- Save/Cancel buttons

### 4. Chat Area Component (`components/chat_area.py`)
- Message display logic (separated from main.py)
- Scroll-to-bottom functionality
- Message styling functions

## Implementation Steps

### Phase 1: Component Creation
1. Create `components/` directory
2. Implement `header.py` with title and settings button
3. Implement `sidebar.py` with model selection
4. Implement `settings_modal.py` with parameter controls
5. Implement `chat_area.py` with message rendering

### Phase 2: Main Application Updates
1. Refactor `main.py` to use component functions
2. Move session state initialization to appropriate location
3. Integrate model and settings selection into LLM service call
4. Add settings button event handler to show/hide modal
5. Ensure conversation history persists correctly

### Phase 3: Parameter Integration
1. Create default settings state in session_state
2. Update `generate_bot_response()` to use dynamic parameters
3. Pass selected model and settings from sidebar/modal to LLM call
4. Handle parameter validation and defaults

### Phase 4: Styling and UX Improvements
1. Ensure consistent styling across components
2. Add loading states and feedback
3. Implement proper modal behavior (overlay, close on outside click)
4. Add tooltips/help text for parameters

## Data Flow
1. User selects model in sidebar → updates session_state.selected_model
2. User adjusts settings in modal → updates session_state.llm_settings
3. On message submit:
   - Chat history retrieved from session_state
   - Selected model and settings passed to LLM service
   - Response generated and added to history
   - UI re-rendered with new messages

## Session State Structure
```python
st.session_state = {
    "chat_history": [(message, is_bot), ...],
    "selected_model": "google/gemma-2-2b-it",  # default
    "llm_settings": {
        "temperature": 0.2,
        "top_p": 0.7,
        "max_tokens": 1024,
        # ... other parameters
    },
    "show_settings": False  # modal visibility
}
```

## Files to Create/Modify
- `components/header.py` (new)
- `components/sidebar.py` (new)
- `components/settings_modal.py` (new)
- `components/chat_area.py` (new)
- `main.py` (modified)

## Dependencies
- streamlit (already used)
- openai (already used)
- python-dotenv (already used)

## Testing Considerations
1. Verify model selection changes the API call
2. Verify settings parameters affect response generation
3. Verify chat history persists across messages
4. Verify modal opens/closes correctly
5. Verify UI remains responsive during API calls
6. Test edge cases (empty settings, invalid parameters)

## Future Enhancements (Post-Implementation)
- Persistent chat history (localStorage/database)
- Multiple conversation threads
- Message editing/deletion
- Export/share functionality
- Dark/light theme toggle
- Voice input/output