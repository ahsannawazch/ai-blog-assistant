# 🤖 AI Blog Assistant  
> An end-to-end LLM-powered research & writing companion that turns any topic into a polished, SEO-ready blog post.

---

## ✨ Features

- 🧠 **Smart Topic Analysis** – automatically decomposes complex topics  
- 🔍 **Real-time Web Research** – fetches up-to-date sources via Tavily  
- ✍️ **Structured Drafting** – consistent tone and real world info with minimum hallucinations  .
- 🎯 **Interactive Chat UI** – Thanks to the Chainlit 
- 💬 **Memory-Backed ChitChat** – context-aware conversations with `mem0`. It is basically a RAG over past conversations.

---

## 🧩 Core Workflow Nodes
| Node | Purpose |
|------|---------|
| **Intent Classification** | Detects whether you want to create, edit, or just chat |
| **Topic Analysis** | Extracts the main subject and sub-topics |
| **Question Generation** | Produces research questions to cover |
| **Web Search** | Retrieves answers & sources |
| **Content Writing** | Builds the first draft |
| **Content Editing** | Refines or rewrites based on your feedback |

---

## 🚀 Quick Start

### Prerequisites
- Python ≥ 3.10  
- API keys: OpenAI, Tavily, LangSmith *(optional)*

### Option A – Local Python
```bash
# 1. Clone
git clone https://github.com/yourusername/ai-blog-assistant.git
cd ai-blog-assistant

# 2. Install
pip install -r requirements.txt

# 3. Configure
cp .env.sample .env
# edit .env with your keys

# 4. Run
chainlit run src/app.py --port 8000
# open http://localhost:8000
```


## 📁 Project Layout

```
ai-blog-assistant
├── src
│   ├── app.py                 # Chainlit entry point
│   ├── langgraph_workflow.py  # State-graph definition
│   └── utils/
│       └── prompts.py         # All prompts & templates
├── requirements.txt
├── .env.sample
└── README.md
```

---

## 🤝 Contributing
Found a bug or have an idea?  
- 🐛 [Open an issue](https://github.com/yourusername/ai-blog-assistant/issues)  

---
