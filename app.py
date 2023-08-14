
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
import os
import streamlit as st
from apikey import apikey

os.environ["OPENAI_API_KEY"] = apikey

embeddings = OpenAIEmbeddings()

# Load saved embeddings from hardisk
db = FAISS.load_local("index_1000t", embeddings)

# Define llm 
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.1)

# Define memory instance
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')

# Define AQ retrieval chain
chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=db.as_retriever(), memory=memory)

def main():
    st.title("ARU Chatbot Mr. Yildirim ")
    st.write("Ask me anything about university!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "source_history" not in st.session_state:
        st.session_state.source_history = []
    if "input_counter" not in st.session_state:
        st.session_state.input_counter = 0

    # Display the previous chat history and sources
    for i in range(0, len(st.session_state.chat_history), 2):
        st.write("**User**: ", st.session_state.chat_history[i])
        st.write("**Mr. Yildirim**: ", st.session_state.chat_history[i+1])
        st.write("**Sources**: ", st.session_state.source_history[i//2])
        
    # Feedback button
    if len(st.session_state.chat_history) >= 2:
        if st.button('Reply better next time!', key=f'dislike_{st.session_state.input_counter-1}'):
            with open('disliked_responses.txt', 'a') as file:
                file.write(f"Question: {st.session_state.chat_history[-2]}\n")
                file.write(f"Answer: {st.session_state.chat_history[-1]}")
                file.write(f"Sources: {st.session_state.source_history[-1]}\n\n")

    # Create a form for the user input
    with st.form(key='user_input_form'):
        user_input = st.text_input(f"User {st.session_state.input_counter}:", key="user_input")
        submit_button = st.form_submit_button(label='Ask')

    # If the submit button is pressed
    if submit_button and user_input:
        # Add user input to conversation history
        st.session_state.chat_history.append(user_input)

        # Get the bot's response
        bot_response = chain({"question": user_input}, return_only_outputs=True)

        # Add bot response and its sources to their respective histories
        st.session_state.chat_history.append(bot_response['answer'])
        st.session_state.source_history.append(bot_response['sources'])

        # Display the bot's response and its sources
        st.write("**Mr. Yildirim**: ", bot_response['answer'])
        st.write("**Sources**: ", bot_response['sources'])

        # Increment the counter for the next input
        st.session_state.input_counter += 1
        
        # Rerun the script to generate a new input line
        st.experimental_rerun()

# Run the Streamlit app
if __name__ == "__main__":
    main()

