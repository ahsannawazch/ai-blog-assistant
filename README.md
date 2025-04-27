# 🤖 AI Content Writer Bot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Chainlit](https://img.shields.io/badge/chainlit-latest-orange)](https://github.com/Chainlit/chainlit)
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

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- 🐍 Python 3.10 or higher
- 🔑 API keys for:
  - OpenAI
  - Tavily
  - LangSmith (optional)

### 🛠️ Installation

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

### 🏃‍♂️ Running the App

Launch the application:
```bash
chainlit run app.py
```

Then open your browser and navigate to the provided URL. That's it! 🎉

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
