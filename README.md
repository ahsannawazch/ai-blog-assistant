# Content Writer Workflow with LangGraph, Chainlit, and Pydantic AI

This repository implements an automated content generation workflow using [LangGraph](https://github.com/langchain-ai/langgraph), [Chainlit](https://github.com/Chainlit/chainlit), and [Pydantic AI](https://github.com/pydantic/ai). The system is designed to analyze a user-provided topic, generate relevant questions, perform web searches for answers, and synthesize a draft article—all orchestrated through a modular, traceable graph workflow.

## Features

- **Topic Analysis**: Uses LLMs to analyze a user query and extract the main topic.
- **Question Generation**: Automatically generates a list of relevant questions about the topic.
- **Web Search Integration**: Fetches up-to-date answers for each question using the Tavily API.
- **Draft Writing**: Synthesizes a coherent draft using the generated Q&A pairs.
- **Chainlit UI**: Provides an interactive chat interface for users to submit topics and receive drafts.
- **LangSmith Tracing**: Enables advanced tracing and debugging of the workflow.

## Project Structure

```
.
├── app.py                  # Chainlit app entry point
├── langgraph_workflow.py   # Core workflow logic using LangGraph
├── utils/
│   └── prompts.py          # Prompt templates for each agent
├── requirements.txt        # Python dependencies
└── ...                     # Other supporting files
```

## How It Works

1. **User Input**: The user submits a topic via the Chainlit chat interface.
2. **Topic Analysis**: The system analyzes the topic using an LLM agent.
3. **Question Generation**: Another agent generates a list of questions about the topic.
4. **Web Search**: For each question, the system performs a web search and retrieves answers.
5. **Draft Writing**: The answers are compiled and passed to a writer agent to generate a draft article.
6. **Output**: The draft is returned to the user in the chat interface.

## Getting Started

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) or `pip` for dependency management
- API keys for Tavily and any LLM providers (set in `.env`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file with the required API keys.

### Running the App

To start the Chainlit app:

```bash
chainlit run app.py
```

Then, open the provided URL in your browser to interact with the system.

## Customization

- **Prompts**: Modify `utils/prompts.py` to adjust the behavior of each agent.
- **Workflow**: Edit `langgraph_workflow.py` to change the graph structure or add new nodes.
- **UI**: Customize the Chainlit interface in `app.py`.

## License

MIT License
