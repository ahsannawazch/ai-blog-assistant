# 🤖 AI Blog Assistant  
> An end-to-end LLM-powered research & writing companion that turns any topic into a polished, SEO-ready blog post. It fetches real world data using tavily to use upto date information for the blog. The assistant mimics how  a human content writer would plan, research and execulte a blog post. Each node is assigned a defined role in the workflow to get a coherent blog. 

---

## ✨ Features

- 🧠 **Smart Topic Analysis** – automatically decomposes complex topics.  
- 🔍 **Real-time Web Research** – fetches up-to-date sources via Tavily  
- ✍️ **Structured Drafting** – consistent tone and real world info with minimum hallucinations  .
- 🎯 **Interactive Chat UI** – Thanks to the Chainlit 
- 💬 **Memory-Backed ChitChat** – context-aware conversations with `mem0`. It is basically a RAG over past conversations and provides the ChitChat node with context aware past interactions

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

### Workflow Diagram

![Workflow Diagram](https://github.com/ahsannawazch/ai-blog-assistant/blob/master/workflow/workflow%20ai%20blog%20assistant.png?raw=true)

---

## 🚀 Quick Start

### Prerequisites
- Python ≥ 3.10  
- API keys: Groq (Free for limited usage) 
- Tavily (Free for limited usage)
- Mem0 (Free for limited usage)
- LangSmith *(optional)*

### Run
```bash
# 1. Clone
git clone https://github.com/ahsannawazch/ai-blog-assistant
cd ai-blog-assistant

# 2. Install
pip install -r requirements.txt

# 3. Configure
cp .env.sample .env
# edit .env with your keys

# 4. Run
chainlit run app.py --port 8000
# open http://localhost:8000
```

## 🤝 Contributing
Found a bug or have an idea?  
- 🐛 [Open an issue](https://github.com/ahsannawazch/ai-blog-assistant/issues)


