import streamlit as st
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chatbot import (
    get_text_chunks, 
    get_vectorstore, 
    generate_augmented_answer,
    retrieve_documents
)

FLASK_URL = "http://127.0.0.1:8080"  # Base URL for the Flask app


def fetch_posts_from_flask():
    response = requests.get(f"{FLASK_URL}/fetch-posts")
    if response.status_code == 200:
        posts = response.json()  # assuming the response is a list of posts in JSON format
        # Check if posts are in the expected format (list of dictionaries with 'content' key)
        if isinstance(posts, list) and all(isinstance(post, dict) and 'content' in post for post in posts):
            return posts
        else:
            st.error("Fetched posts do not have the expected format")
            return []
    else:
        st.error("Failed to fetch posts from the backend")
        return []
    
# Function to fetch available endpoints from the Flask backend
def list_endpoints():
    """Fetch the list of available endpoints."""
    response = requests.get(f"{FLASK_URL}/endpoints")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch endpoints from the backend")
        return []

# Function to add a new endpoint to the Flask backend
def add_endpoint(new_endpoint):
    """Add a new endpoint to the list."""
    response = requests.post(f"{FLASK_URL}/endpoints", json={"endpoint": new_endpoint})
    if response.status_code == 201:
        st.success("Endpoint added")
    else:
        st.error("Failed to add endpoint")

# Function to remove an endpoint from the Flask backend
def remove_endpoint(index):
    """Remove an endpoint from the list."""
    response = requests.delete(f"{FLASK_URL}/endpoints/{index}")
    if response.status_code == 200:
        st.success("Endpoint removed")
    else:
        st.error("Failed to remove endpoint")


def main():
    load_dotenv()
    st.set_page_config(page_title="ChatBot for WordPress ")
    st.title("WordPress Chatbot Interface")
    # Initialize session state variables if not present
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'user_query' not in st.session_state:
        st.session_state.user_query = ""
        
    # Initialize 'endpoints' in session_state if not already initialized
    if 'endpoints' not in st.session_state:
        st.session_state.endpoints = []
    # Create a sidebar with options
    with st.sidebar:
        st.header("Input WebSite name ")
        
        # Section for listing endpoints
        st.subheader("Wordpress Site name .com")
        # if 'endpoints' not in st.session_state:
        #     st.session_state.endpoints = list_endpoints()
        # List existing endpoints
        if st.session_state.endpoints:
            for i, endpoint in enumerate(st.session_state.endpoints):
                st.write(f"{i}: {endpoint}")

        # Add new endpoint
        new_endpoint = st.text_input("Enter a new Website URL")
        if st.button("Add"):
            if new_endpoint:
                add_endpoint(new_endpoint)
                st.session_state.endpoints.append(new_endpoint)

        # Remove an endpoint
        if st.session_state.endpoints:
            endpoint_to_remove = st.number_input(
                "Index of endpoint to remove",
                min_value=0,
                max_value=len(st.session_state.endpoints) - 1,
                step=1
            )

            if st.button("Remove Endpoint"):
                if 0 <= endpoint_to_remove < len(st.session_state.endpoints):
                    remove_endpoint(endpoint_to_remove)
                    st.session_state.endpoints.pop(endpoint_to_remove)

        # Button to fetch and process latest posts
        if st.button("Fetch Latest Posts"):
            if 'posts' not in st.session_state:
                st.session_state.posts = fetch_posts_from_flask()

            if st.session_state.posts:
                all_content = " ".join(post.get('content', '') for post in st.session_state.posts)
                if 'text_chunks' not in st.session_state:
                    st.session_state.text_chunks = get_text_chunks(all_content)
                    st.write(f"Total chunks created: {len(st.session_state.text_chunks)}")

                if 'index' not in st.session_state:
                    st.session_state.index, st.session_state.text_chunks = get_vectorstore(st.session_state.text_chunks)
                    st.success("Text processed and vector store created")


    # Display the chatbot-like interface on the home screen
    st.subheader("Chat with the Bot")
    # Show the conversation so far
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.write(f"**You**: {chat['content']}")
            else:
                st.write(f"**Bot**: {chat['content']}")

    # User input
    user_query = st.text_input("Ask your question:", value=st.session_state.user_query,key='prev')

    if st.button("Send"):
        if user_query:
            
            embedding_model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
            retrieved_docs = retrieve_documents(user_query, st.session_state.index, st.session_state.text_chunks,embedding_model)
            context = " ".join(retrieved_docs)
            # Generate answer from the chatbot
            answer = generate_augmented_answer(user_query,context)
            # Display the generated answer
            st.write(f"**Bot**: {answer}")
            # Add user message and bot response to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "bot", "content": answer})

        # Clear the user input field
        st.session_state.user_query = ""
        user_query = st.text_input("Ask your question:", value=st.session_state.user_query,key='next')
        st.rerun()  # Re-render the page to reset the text input

if __name__ == "__main__":
    main()
