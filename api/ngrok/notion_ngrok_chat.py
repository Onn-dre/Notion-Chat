import streamlit as st
from langchain.document_loaders import NotionDBLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import textwrap

load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings()

st.set_page_config(page_title="Test")

@st.cache_data
def create_db_from_notion(NOTION_TOKEN, DATABASE_ID):
    loader = NotionDBLoader(
        integration_token=NOTION_TOKEN, 
        database_id=DATABASE_ID,
        request_timeout_sec=30 
    )
    
    ndb = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(ndb)

    db = FAISS.from_documents(docs, embeddings)
   
    return db 

@st.cache_data
def get_response_from_query(_db, query, k=4):
    """
    gpt-3.5-turbo can handle up to 4097 tokens. Setting the chunksize to 1000 and k to 4 maximizes
    the number of tokens to analyze.
    """
    docs = _db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

    # Template to use for the system message prompt
    template = """
        You are a helpful assistant that can answer questions about content contained in Notion 
        databases based on: {docs}
        
        Only use the factual information from the information provided to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
        """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Answer the following question: {question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)

    response = chain.run(question=query, docs=docs_page_content)
    response = response.replace("\n", "")
    return response, docs

st.title("Test")

NOTION_TOKEN = st.text_input("Enter your Notion integration token:")
DATABASE_ID = st.text_input("Enter your Notion database ID:")

if NOTION_TOKEN and DATABASE_ID:
    db = create_db_from_notion(NOTION_TOKEN, DATABASE_ID)

    query = st.text_input("What's your question?")
    if query:
        response, docs = get_response_from_query(db, query)

        st.subheader("Answer:")
        st.write(textwrap.fill(response, width=50))

