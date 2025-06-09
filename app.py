import chainlit as cl
import os
from langchain_core.tracers.context import tracing_v2_enabled
from graph import create_graph
import uuid

from dotenv import load_dotenv
load_dotenv()

# LangSmith Configuration
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "content-writer"

graph = create_graph()


@cl.on_chat_start
def chat_session():
    session_id = str(uuid.uuid4())
    # print(f'session id: {session_id}')
    cl.user_session.set("session_id", session_id)



# Testing new chainlit initiater
@cl.on_message
async def on_message(msg: cl.Message):
    user_query = msg.content
    # config = {"configurable": {"thread_id": cl.context.session.id}}
    config = {"configurable": {"thread_id": cl.user_session.get("session_id")}}   # I don't think this is working/needed
    # config = {"configurable": {"thread_id": "1234"}}
    print(config)

    with tracing_v2_enabled(project_name="content-writer") as cb:
        initial_state = {"query": user_query, "user_id": cl.user_session.get("session_id")}          # user_id related to mem0

        final_nodes = ['writer_node', 'Editor', 'ChitChat']
        process_nodes = ['intent_classifier', 'topic_analyst', 'list_questions','web_search']
        all_nodes = ['intent_classifier', 'topic_analyst', 'list_questions', 'writer_node', 'Editor', 'ChitChat', 'web_search']

        for event in graph.stream(initial_state, config):
            for node in all_nodes:
                if node in event and node in process_nodes:
                    if node == "intent_classifier":
                        data = cl.Message(content="🤔 Thinking ... ") 
                        await data.send()
                    elif node == "topic_analyst":
                        data.content = "🔍 Understanding the User Request ..."
                        await data.update()
                    elif node == "list_questions":
                        data.content = "💡 Brainstorming the topic ..."
                        await data.update()
                    elif node == "web_search":
                        data.content = "🌐 Searching web ... It'll take a minute  "
                        await data.update()
                    
                # If node is in final nodes, send the output
                elif node in event and node in final_nodes:
                    if node == "writer_node":
                        data.content= "✅ Blog Generated!" 
                        await data.update()
 
                        writer_output = event[node]
                        if isinstance(writer_output, dict):
                            first_value = next(iter(writer_output.values()), None)
                            await cl.Message(content=str(first_value)).send()

                    elif node == "Editor":
                        editor_output = event[node]
                        data.content = f"✏️ {editor_output['status']}"
                        await data.update()
                        
                        if isinstance(editor_output, dict):
                            first_value = next(iter(editor_output.values()), None)
                            await cl.Message(content=str(first_value)).send()

                    elif node == "ChitChat":
                        data.content = "💬 Chat mode ... "
                        await data.update()
                        chat_output = event[node]

                        if isinstance(chat_output, dict):
                            first_value = next(iter(chat_output.values()), None)
                            await cl.Message(content=str(first_value)).send()
