#WIP 9_22_23
#faiss_CPU_for_+Llama2BOT
import gc 
import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.llms import HuggingFaceTextGenInference
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory

def clear_index():
    global vector_store  # Declare vector_store as global to ensure we are accessing the correct object
    if 'vector_store' in globals():  # Check if vector_store exists
        del vector_store  # Delete the object holding the FAISS index
        gc.collect()  # Force Python to perform garbage collection
        st.success('Index cleared from memory')

# Call clear_index at the beginning of your script or initialization function
clear_index()

# Load the files from the path
loader = DirectoryLoader('data/', glob="faqs_long_V2.txt", loader_cls=TextLoader)
#loader = DirectoryLoader('data/', glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
text_chunks = text_splitter.split_documents(documents)

#
embeddings="BAAI/bge-base-en"
encode_kwargs = {'normalize_embeddings': True} # I.e. Cosine Similarity

model_norm = HuggingFaceBgeEmbeddings(
    model_name=embeddings,
    model_kwargs={'device' : 'cpu' },
    encode_kwargs=encode_kwargs                                       
    )

# Vector store
vector_store = FAISS.from_documents(text_chunks, model_norm)

# Create HuggingFaceTextGenInference as the language model - Check Port Match to TGI
llm = HuggingFaceTextGenInference(
    inference_server_url="http://localhost:8080/",
    max_new_tokens=512,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
)

system_prompt = "Only provide answers using information from the context provided and if you do not the answer state that the data is not contained in your knowledge base and stop your response" 

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                              retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                              memory=memory)

st.title("🦙Local Llama2 with Langchain🦜")
         #running locally with Chat 🤖 with an S3.pdf Document")

def conversation_chat(query):
    # Construct the prompt using the LLaMa 2 chat models structure
    full_query = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{query} [/INST]</s>"
    
    result = chain({"question": full_query, "chat_history": st.session_state['history']})
    return result["answer"]

def initialize_session_state():
    with st.spinner("Initializing session..."):
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello! Ask me anything about AWS our supported AWS products"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Lets get started! 👋"]

def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="My Knowledgebase contains info about AWS services...", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button:
            with st.spinner("Sending..."):
                if user_input:
                    output = conversation_chat(user_input)
                    st.session_state['past'].append(user_input)
                    st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user',)
                message(st.session_state["generated"][i], key=str(i) + '_assistant',)

# Initialize session state
initialize_session_state()
# Display chat history
display_chat_history()
