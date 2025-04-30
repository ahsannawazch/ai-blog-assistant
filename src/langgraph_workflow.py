from pydantic_ai import Agent
from pydantic import BaseModel
from pydantic_ai.models.groq import GroqModel
from utils.prompts import topic_analyst_prompt_v2, get_list_prompt, writer_prompt_v2, intent_classifier_prompt, editor_prompt
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
os.environ["LANGCHAIN_PROJECT"] = "content-writer"  # Using the project name from your .env file


# Models initialization
llama_model = GroqModel(model_name="llama-3.1-8b-instant")
gemma_model = GroqModel(model_name="gemma2-9b-it")
llama_4_model = GroqModel(model_name="meta-llama/llama-4-scout-17b-16e-instruct")



class State(TypedDict):            # Rename this later to something like OverallState.
    query: str
    intention: str
    topic_analyzer: str        # ----> topic_analyzer_agent's reply =   str or list or markdown or pydantic (List) of questions
    questions_list: list
    web_search_result: Annotated[list, add_messages]  
    initial_draft: str
    editor_draft: Annotated[list, add_messages]  
    ChitChat_history = Annotated[list, add_messages]
    


class QueriesState(TypedDict):
    question: str 

graph_builder = StateGraph(State)

def intent_classifier(state: State):
    print(f'________________Getting to know the user intention____')

    user_prompt = state['query']

    agent = Agent(
        model= llama_model,
        retries=3,
        system_prompt=intent_classifier_prompt,
        instrument=False
    )

    response = agent.run_sync(
            user_prompt=user_prompt
        )

    print(f'User Intention: {response.output}')
    return {'intention': response.output}


def topic_analyzer(state: State):
    print(f'________________Entering into Topic Analyser Node____')

    agent = Agent(
        model=llama_model,
        system_prompt=topic_analyst_prompt_v2,
        retries=3,
    )

    user_prompt = state['query']

    response = agent.run_sync(
            user_prompt=user_prompt
        )

    print(f'_____________Exiting into Topic Analyser Node______')

    return {"topic_analyzer": response.output}


def list_questions(state: State):           # We can later merge this ability in the topic_analyzer 
                                            # to generate 'list' of Qs using pydantic or so
    class QuestionList(BaseModel):
        questions: List[str]  

    print("___________Getting structured Questions________")
    list_agent = Agent(
        model=gemma_model,
        output_type=QuestionList,
        system_prompt=get_list_prompt,
    )

    unstructured_questions = state['topic_analyzer']
    
    response = list_agent.run_sync(
        user_prompt=unstructured_questions
        )
    total_questions = len(response.output.questions)
    print(f"___I think, I got {total_questions}___")
    return {"questions_list": response.output.questions}  # Maybe we have to chnage this too
                                                        # if reviwer/editor asks for more questions
                                                        # we can use annoted list to have these question
                                                        # Appended later
                                                        # BUT  there is another approach
                                                        # We can have reviwer/editor with own tool/MCP support
                                                        # So it can  fill the gaps itself  (seems better way)


def web_search(state: QueriesState):    # Taking the state which has a question (`Send` by `map_questions_to_search`)
    
    query = state['question']
    print(query)

    tavily_client = TavilyClient()

    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer="advanced",
        include_images=False                      # We'll see this later
        )
    search_result = response['answer']

    return {'web_search_result': [search_result]}              # Saving results in the orignal/main state
    # I think we can get the questions and search_results from `questions_list` and `web_search_result` elements of `State`
    # we can zip elements from both of them to form a Q/A pair to give to the writer node.
    # I think we'd get the exact pair cause we're getting answer the way we are looping over each question in `map_questions_to_search' node.

def map_questions_to_search(state: State):
    questions = state['questions_list']
    return [Send(node='web_search', arg=QueriesState(question=question)) for question in questions]

def writer_node(state: State):
    query = state['query']                    # This also involves (GIVE ME QUESTIONS ONLY part, ETC).   Fix Later.
    questions = state['questions_list']
    answers = state['web_search_result']
    QA_pairs = ""

    for question, answer in zip(questions, answers):
        QA_pairs += f"Question: {question}\nAnswer: {answer.content}\n\n"

    writer_agent = Agent(
        model= llama_4_model,
        retries=3,
        system_prompt=writer_prompt_v2,
        )
    
    prompt = f"""{query} \n\n Relevant Questions and Answers: {QA_pairs} """

    response = writer_agent.run_sync(user_prompt=prompt)
    return {"initial_draft": response.output}

def editor_node(state: State):
    print("\n__________We are in editor node____________________\n")
    editor_draft = state['editor_draft']
    if editor_draft:  # Check if the list is non-empty
        draft = editor_draft[-1]
        print(f"Using latest editor draft")
    else:
        print("No earlier editing record, using initial_draft")
        draft = state['initial_draft']    

    
    editor_agent = Agent(           
        model=llama_4_model,                # Try Deepseek R1 for better Results (IMO) later
        system_prompt=editor_prompt,
        #tools= TavilyClienty,              # IMP: Later add tool/MCP support to fill in gaps to get new info (user can require new facts/info )
        retries=3
    )   

    prompt = f'Instruction: Change the tone of the Blog to Gen-z \n Here is the blog: {draft}'
    response = editor_agent.run_sync(user_prompt= prompt)
    return {'editor_draft': response.output}

def ChitChat(state: State):
    query = state['query']
    
    print("Entering the chat node__________")

    chat_agent = Agent(
        model= gemma_model,
        retries=3,
        system_prompt='You are a helpful assistant. Please repond to user queries with kind and compassion',
        )
    
    response = chat_agent.run_sync(user_prompt=query)
    print(f'chat_response: {response.output}')

    return {'chat_record': response.output}


def intent_router(state: State):                 
    intent = state['intention']              # NewTopic or EditLastOutput or ChitChat
    if 'NewTopic' in intent:
        return 'topic_analyst'
    elif 'EditLastOutput' in intent:
        return 'Editor'
    else:
        return 'ChitChat'



def create_graph():  # rename to something like graph schema or something (maybe not)
    # Nodes
    graph_builder.add_node('intent_classifier', intent_classifier)
    graph_builder.add_node('topic_analyst', topic_analyzer)
    graph_builder.add_node('list_questions', list_questions)
    graph_builder.add_node('web_search', web_search)
    graph_builder.add_node('writer_node', writer_node)
    graph_builder.add_node('Editor', editor_node)
    graph_builder.add_node('ChitChat', ChitChat)



    # Edges and conditionals
    graph_builder.add_edge(START,'intent_classifier')
    graph_builder.add_conditional_edges(
        'intent_classifier', intent_router, {
            'topic_analyst': 'topic_analyst',
            'Editor': 'Editor',
            'ChitChat': 'ChitChat'
            }
        )

    graph_builder.add_edge('topic_analyst','list_questions')
    graph_builder.add_conditional_edges('list_questions', map_questions_to_search, ['web_search'])  # The conditional edge is between two nodes here (questions and web search)
                                                                                                    # `map_questions_to_search` ain't a node, it is just a function.
                                                                                                    # Reasons why we have conditional edge instead of simple `add_edge`:
                                                                                                    # 1. N parallel executions (one per task) instead of Single execution of task_enricher
                                                                                                    # 2. Each task_enricher gets 1 task 
                                                                                                    # 3. Automatic parallelization
    graph_builder.add_edge('web_search', 'writer_node')
    graph_builder.add_edge('writer_node', END)

    # Editing flow
    graph_builder.add_edge('Editor', END)
    # Chat flow
    graph_builder.add_edge('ChitChat', END)


    return graph_builder.compile()



# Our main function
def main():
    with tracing_v2_enabled(project_name="content-writer") as cb:
        graph = create_graph()
        # print(graph.get_graph().draw_mermaid())
        
        initial_state = {"query": "I want to edit this blog" }

        final_state = graph.invoke(initial_state)
        
        for key, value in final_state.items():
            print(f"node: {key}\n\n  Data: {value}")
            print("__" * 40)
        
        print(f"🔗 LangSmith Trace URL: {cb.get_run_url()}")



    # graph = create_graph()

    # query = input("Your query: ")                           use this latter

    # initial_state = {
    # "query": "topic: Do Teslas Have Cigarette Lighters.",
    # }

    
    # for event in graph.stream(initial_state):
    #     for key in event:
    #         print("-----------------------------------")
    #         print("Done with " + key)
    #         print("\n*******************************************\n")

    # final_state = graph.invoke(initial_state)
    # # print("✅ Final State:")
    # for key, value in final_state.items():
    #     print(f"node: {key}\n\n  Data: {value}")
    #     print("__" * 40)


if __name__ == "__main__":
    main()