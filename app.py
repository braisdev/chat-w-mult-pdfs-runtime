import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from htmlTemplates import css, bot_template, user_template


def get_pdf_text(pdf_docs):
    """
    Get the text from the pdf documents
    """
    raw_text = ""

    for pdf_doc in pdf_docs:
        pdf_reader = PdfReader(pdf_doc)
        for page in pdf_reader.pages:
            raw_text += page.extract_text()

    return raw_text

def get_vectorstore(text_chunks):
    """
    Create the vectorstore
    """

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(text_chunks, embeddings)

    return vectorstore

def get_text_chunks(raw_text):
    """
    Get the text chunks from the raw text
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    text_chunks = text_splitter.split_text(raw_text)

    return text_chunks

def get_conversation_chain(vectorstore):
    """
    Create the conversation chain
    """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chat = ChatOpenAI(temperature=0)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = chat,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )

    return conversation_chain

    return chain

def handle_user_input(user_question):
    """
    Handle the user input
    """
    if st.session_state.conversation:
        response = st.session_state.conversation({'question':user_question})
        st.session_state.chat_history = response['chat_history']

        for i,message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
def main():

    st.set_page_config(page_title="Chat with multiple PDFs in memory", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header("Chat with multiple PDFs in memory :books:")

    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdfs_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True
        )
        if st.button("Process"):
            with st.spinner("Processing your documents..."):
                # get pdf text
                raw_text = get_pdf_text(pdfs_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create the vectorstore
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':

    main()