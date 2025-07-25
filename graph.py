from langgraph.graph import StateGraph, START, END
from nodes import State, QueriesState
from nodes import intent_classifier, topic_analyzer, web_search, writer_node, editor_node, ChitChat, intent_router, map_questions_to_search, list_questions
from langgraph.checkpoint.memory import MemorySaver

graph_builder = StateGraph(State)

# Graph Construction
def create_graph():
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
    graph_builder.add_conditional_edges('list_questions', map_questions_to_search, ['web_search'])
    graph_builder.add_edge('web_search', 'writer_node')
    graph_builder.add_edge('writer_node', END)
    graph_builder.add_edge('Editor', END)
    graph_builder.add_edge('ChitChat', END)
    
    memory = MemorySaver()
    return graph_builder.compile(checkpointer=memory)


