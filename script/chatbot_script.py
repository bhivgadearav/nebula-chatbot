# This is the file I wrote when trying to create a chatbot with langchain without ui
# It lists the steps involved and code for that step
# So you can better understand how to make a chatbot using langchain
# Refer to langchain if the current langchain version is higher then 0.3 as it was created in langchain v0.3

# Steps
# 1. Load OPEN_API_KEY
# 2. Initialize a openai model
# 3. Add memory
# 4. Add a prompt template
# 5. Initialize a chain
# 6. Invoke the chain

# This code is upto date with langchain v0.3

# Step 1 
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
open_api_key = os.environ["OPENAI_API_KEY"]

# Step 2
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

# Step 3
import uuid
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {} #In-memory storage

## Generates unique session ids
def generate_session_id():
    return uuid.uuid4()
config = {"configurable": {"session_id": thread_id}}

## Used by runnable message history to get a session's message history or create if it doesn't exist and then return it
def get_by_session_id(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Step 4 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

template = ChatPromptTemplate([
    # ("system", "You are a helpful AI bot. Your name is {name}."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{user_input}"),
])

# Step 5
chain = template | model #Base chain

## Chain with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_by_session_id,
    input_messages_key="user_input",
    history_messages_key="history",
)

sessions = {}
current_session_id = generate_session_id()
sessions[current_session_id] = f"Session {len(sessions + 1)}"

# Make openai and langchain api keys and try running the file
response_1 = chain_with_history.invoke(
    {"user_input": "My full name is Arav Bhivgade."},
    config = {'configurable': {'session_id': current_session_id}}
)

response_1 = chain_with_history.invoke(
    {"user_input": "What is my last name?"},
    config = {'configurable': {'session_id': current_session_id}}
)

# RunnableWithMessageHistory can be used to store and retrieve memory from other places
# Reference - https://www.perplexity.ai/search/how-do-i-use-runnablewithmessa-tXTnzkguQwuK_Int29X0Ng

# on init generare_session_id() generates a id for first ever convo
# which is stored in current_sesssion_id and sessions so it is always accesible and is used in the config when chain_with_history is invokes
# if user wants to start a new convo, generate_session_id is called and current_session_id is set to returned value and also stored in sessions as per first one is stored
# if user wants to go back to a session, that session from sessions is retrieved and set to curren_session_id