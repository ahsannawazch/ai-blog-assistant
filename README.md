# 🤖 AI Content Writer Bot

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Chainlit](https://img.shields.io/badge/chainlit-0.7.700-orange)](https://github.com/Chainlit/chainlit)
[![LangGraph](https://img.shields.io/badge/langgraph-latest-green)](https://github.com/langchain-ai/langgraph)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> 📝 An intelligent content generation system powered by LLMs that researches, writes, and refines content automatically!

## ✨ Features

🧠 **Smart Topic Analysis**
- Automatically understands and breaks down complex topics
- Identifies key areas to research

🔍 **Intelligent Research**
- Uses Tavily API for real-time web search
- Generates comprehensive Q&A pairs

✍️ **Advanced Content Generation**
- Creates well-structured drafts
- Maintains consistent tone and style
- Includes citations and references

🎯 **Interactive Experience**
- User-friendly chat interface
- Real-time progress tracking
- Draft previews and editing

🔄 **Advanced Workflow**
- Modular graph-based architecture
- Traceable and debuggable processes
- Easy to extend and customize

## 🧩 Additional Features

💬 **Intent Classification**
- Determines user intent (e.g., content creation, editing, or chat).

🔍 **Topic Analysis**
- Analyzes user queries to identify the main topic..

❓ **Question Generation**
- Generates structured questions based on the analyzed topic.

🌐 **Web Search Integration**
- Performs web searches to gather relevant information for content creation.

📝 **Content Writing**
- Generates drafts of content (e.g., blogs) using AI models.

✏️ **Content Editing**
- Refines drafts based on user instructions.

💡 **ChitChat Mode**
- Engages in conversational interactions with memory for context-aware responses.

🔄 **Graph Workflow**
- Manages operations using a state graph for seamless transitions between tasks.

🧠 **Memory Integration**
- Uses `mem0` to store and retrieve memory for enhanced user interactions.

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- 🐍 Python 3.10.10 or higher
- 🔑 API keys for:
  - OpenAI
  - Tavily
  - LangSmith (optional)

### 🛠️ Installation

#### Using Python

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-content-writer.git
   cd ai-content-writer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.sample .env
   # Edit .env with your API keys
   ```

#### Using Docker 🐳

1. **Build the Docker image**
   ```bash
   docker build -t ai-content-writer .
   ```

2. **Run with Docker**
   ```bash
   docker run -p 8000:8000 --env-file .env ai-content-writer
   ```

### 🏃‍♂️ Running the App

#### Local Development
```bash
chainlit run src/app.py --port 8000
```

Then open your browser and navigate to `http://localhost:8000`. That's it! 🎉

## 🎨 Customization

Want to make it your own? Here's how:

📋 **Content Templates**
- Modify prompts in `utils/prompts.py`
- Add new writing styles
- Customize output formats

🔧 **Workflow Adjustments**
- Edit `langgraph_workflow.py`
- Add new research sources
- Implement custom agents

## 📄 License

MIT License - feel free to use it in your own projects! 🎁

## 🤝 Contributing

We welcome contributions! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit PRs

---

<p align="center">
Made with ❤️ and powered by LLMs
</p>
