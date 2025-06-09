from typing_extensions import TypedDict
from typing import Annotated, List, Dict
from langgraph.graph.message import add_messages
from langgraph.types import Send
from pydantic_ai import Agent
from pydantic import BaseModel
from models import llama_model, llama_4_model, gemma_model
from prompts import topic_analyst_prompt_v2, get_list_prompt, writer_prompt_v2, intent_classifier_prompt, editor_prompt
from tavily import TavilyClient


from mem0 import MemoryClient
mem0 = MemoryClient()



class State(TypedDict):
    query: str
    intention: str
    topic_analyzer: str
    questions_list: list
    web_search_result: Annotated[list, add_messages]  
    initial_draft: str
    editor_draft: Dict[str, str]
    status: str
    ChitChat_history: Annotated[list, add_messages]
    user_id: str
    # agent_id: str
    # run_id: str

class QueriesState(TypedDict):
    question: str


# Intent Classifier Node
def intent_classifier(state: State):
    print(f'________________Getting to know the user intention____')
    user_prompt = state['query']
    agent = Agent(
        model= llama_model,
        retries=3,
        system_prompt=intent_classifier_prompt,
        instrument=False
    )
    response = agent.run_sync(user_prompt=user_prompt)
    print(f'User Intention: {response.output}')
    return {'intention': response.output}


# Topic Analyzer Node
def topic_analyzer(state: State):
    print(f'________________Entering into Topic Analyser Node____')
    agent = Agent(
        model=llama_model,
        system_prompt=topic_analyst_prompt_v2,
        retries=3,
    )
    user_prompt = state['query']
    response = agent.run_sync(user_prompt=user_prompt)
    print(f'_____________Exiting into Topic Analyser Node______')
    return {"topic_analyzer": response.output}

# Question List Generator
def list_questions(state: State):
    class QuestionList(BaseModel):
        questions: List[str]  
    print("___________Getting structured Questions________")
    list_agent = Agent(
        model=gemma_model,
        output_type=QuestionList,
        system_prompt=get_list_prompt,
    )
    unstructured_questions = state['topic_analyzer']
    response = list_agent.run_sync(user_prompt=unstructured_questions)
    total_questions = len(response.output.questions)
    print(f"___I think, I got {total_questions}___")
    return {"questions_list": response.output.questions}

# web search node
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
    print(" Exiting web_search node")
    return {'web_search_result': [search_result]}

# question mapper
def map_questions_to_search(state: State):
    questions = state['questions_list']
    return [Send(node='web_search', arg=QueriesState(question=question)) for question in questions]

# writer node 
def writer_node(state: State):
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
    prompt = f"""{query} \n\n Relevant Questions and Answers: {QA_pairs} """
    response = writer_agent.run_sync(user_prompt=prompt)
    
    # Save initial draft to mem0
    # mem0.add(response.output, metadata={"type": "blog_draft_initial"}, user_id=user_id)
    
    return {"initial_draft": response.output}

# Editor Node with mem0 memory
def editor_node(state: State):
    print("\n__________We are in editor node____________________\n")
    draft = None
    
    if state.get('editor_draft'):
        status = "Using the latest editor's draft for further enhancements.... "
        print(status)   
        draft = state['editor_draft']        

    elif state.get('initial_draft'):
        status = "Editing the Already Generated Blog:"
        print(status)
        draft = state['initial_draft']
    else:
        status = "Please generate a blog first. Can't edit an empty blog."
        print(status)

    if draft is not None:
        user_instruction = f"Instruction about editing: {state['query']} \n\n The Blog: {draft}"
        editor_agent = Agent(           
            model=llama_4_model,                
            system_prompt=editor_prompt,
            retries=3
        )   

        # prompt = f'Instruction: Change the tone of the Blog to Gen-z. Here is the blog: {initial_draft}'
        response = editor_agent.run_sync(user_prompt=user_instruction)
        
        print("_______________Exiting the EDITOR Node____________________")

        return {'editor_draft': response.output, 'status': status}    
    else:
        return {'editor_draft': 'No data to edit', 'status': status}
       
# ChitChat Node with memory
def ChitChat(state: State):
    query = state['query']
    user_id = state['user_id']
    print("Entering the chat node__________")
    
    # Retrieve relevant memories
    memories = mem0.search(query, limit=5, user_id=user_id, )   # test with app id/ run id/ agent id (for a session)
    context = "\n".join([messages["memory"] for messages in memories]) if memories else "No prior context."
    # print(f'Past Interactions so far: {context}')
    
    chat_agent = Agent(
        model=gemma_model,
        retries=3,
        system_prompt=f'You are a helpful assistant. Previous conversation:\n{context}\nRespond kindly.',
    )
    response = chat_agent.run_sync(user_prompt=query)
    # print(f'chat_response: {response.output}')
    
    # Store interaction in mem0
    mem0.add(f"User: {query}\nAssistant: {response.output}", metadata={"type": "chitchat"}, user_id=user_id)
    return {'ChitChat_history': response.output}

# Intent Router
def intent_router(state: State):                 
    intent = state['intention']
    if 'NewTopic' in intent:
        return 'topic_analyst'
    elif 'EditLastOutput' in intent:
        return 'Editor'
    else:
        return 'ChitChat'
