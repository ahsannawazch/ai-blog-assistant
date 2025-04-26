import chainlit as cl
from pydantic_ai import Agent
from pydantic import BaseModel
from pydantic_ai.models.groq import GroqModel
from utils.prompts import topic_analyst_prompt_v2, get_list_prompt, writer_prompt_v2
import os
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Send
from tavily import TavilyClient
from langchain_core.tracers.context import tracing_v2_enabled

from dotenv import load_dotenv
load_dotenv()

# LangSmith Configuration
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "content-writer"

llama_model = GroqModel(model_name="llama-3.1-8b-instant")
gemma_model = GroqModel(model_name="gemma2-9b-it")
llama_4_model = GroqModel(model_name="meta-llama/llama-4-scout-17b-16e-instruct")

class State(TypedDict):
    query: str
    topic_analyzer: str
    questions_list: list
    web_search_result: Annotated[list, add_messages]
    Initial_Draft: str

class QueriesState(TypedDict):
    question: str

graph_builder = StateGraph(State)

def topic_analyzer(state: State):
    print("[Chainlit] Entering topic_analyzer node")
    agent = Agent(
        model=llama_model,
        system_prompt=topic_analyst_prompt_v2,
        retries=3,
    )
    user_prompt = state['query']
    response = agent.run_sync(user_prompt=user_prompt)
    print("[Chainlit] Exiting topic_analyzer node")
    return {"topic_analyzer": response.output}

def list_questions(state: State):
    print("[Chainlit] Entering list_questions node")
    class QuestionList(BaseModel):
        questions: List[str]
    list_agent = Agent(
        model=gemma_model,
        result_type=QuestionList,
        system_prompt=get_list_prompt,
    )
    unstructured_data = state['topic_analyzer']
    response = list_agent.run_sync(user_prompt=unstructured_data)
    print("[Chainlit] Exiting list_questions node")
    return {"questions_list": response.output.questions}

def web_search(state: QueriesState):
    # print("[Chainlit] Entering web_search node")
    query = state['question']
    tavily_client = TavilyClient()
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer="advanced",
        include_images=False
    )
    search_result = response['answer']
    print("[Chainlit] Exiting web_search node")
    return {'web_search_result': [search_result]}

def map_questions_to_search(state: State):
    questions = state['questions_list']
    return [Send(node='web_search', arg=QueriesState(question=question)) for question in questions]

def writer_node(state: State):
    print("[Chainlit] Entering writer_node")
    query = state['query']
    questions = state['questions_list']
    answers = state['web_search_result']
    QA_pairs = ""
    for question, answer in zip(questions, answers):
        QA_pairs += f"Question: {question}\nAnswer: {answer.content}\n\n"
    writer_agent = Agent(
        model=llama_4_model,
        retries=3,
        system_prompt=writer_prompt_v2,
    )
    writer_prompt = f"""{query} \n\n Relevant Questions and Answers: {QA_pairs} """
    response = writer_agent.run_sync(user_prompt=writer_prompt)
    print("[Chainlit] Exiting writer_node")
    return {"Initial_Draft": response.output}


def create_graph():
    graph_builder.add_node('topic_analyst', topic_analyzer)
    graph_builder.add_node('list_questions', list_questions)
    graph_builder.add_node('web_search', web_search)
    graph_builder.add_node('writer_node', writer_node)

    graph_builder.add_edge(START, 'topic_analyst')
    graph_builder.add_edge('topic_analyst', 'list_questions')
    graph_builder.add_conditional_edges('list_questions', map_questions_to_search, ['web_search'])
    graph_builder.add_edge('web_search', 'writer_node')
    graph_builder.add_edge('writer_node', END)
    
    return graph_builder.compile()

@cl.on_message
async def main(message: cl.Message):
    user_query = message.content
    with tracing_v2_enabled(project_name="content-writer") as cb:
        graph = create_graph()
        initial_state = {"query": user_query}
        final_state = graph.invoke(initial_state)
        draft = final_state["Initial_Draft"]
        if draft:
            await cl.Message(content=f"Draft:\n\n{draft}").send()
        else:
            await cl.Message(content="No draft was generated. Please try again.").send()
