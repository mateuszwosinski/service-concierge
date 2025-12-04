# Examples

This directory contains demo scripts and examples for the Luxury Concierge system.

## Streamlit Chat Demo

A simple web-based chat interface for interacting with the concierge agent.

### Setup

1. Install dependencies:
```bash
uv sync --dev
```

or if using pip:
```bash
pip install streamlit
```

2. Make sure your `.env` file is configured with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

### Running the Demo

```bash
streamlit run examples/demo_streamlit.py
```

The chat interface will open in your browser at `http://localhost:8501`

### Features

- 💬 **Chat interface** - Natural conversation with the AI concierge
- 🔄 **Multi-intent handling** - Handle complex requests with multiple needs
- 📝 **Conversation history** - Context-aware responses based on chat history
- 🛠️ **Tool integration** - Automatically calls tools for products, orders, appointments, and policies

### Example Queries

Try these sample queries:
- "Show me merino wool jackets"
- "What's the status of order ORD-001?"
- "Schedule a fitting appointment for next week"
- "What's your return policy?"
- "I need a new suit for an event and want to book a fitting" (multi-intent)

## Other Demos

- `demo_apis.py` - Direct API usage examples
- `demo_tool_definitions.py` - Tool definition generation
- `demo_understanding_tools.py` - Command-line demo of the Understanding module
