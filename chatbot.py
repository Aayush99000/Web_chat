import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from transformers import pipeline

FLASK_URL = "https://flask-cwz9.vercel.app/"  # Base URL for the Flask app


# Split text into chunks
def get_text_chunks(text):

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)

# Generate vector store from text chunks
def get_vectorstore(text_chunks):
    model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
    embeddings = [model.encode(chunk) for chunk in text_chunks]
    embeddings = np.array(embeddings).astype("float32")
    # Create a FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, text_chunks

# Retrieve documents from vector store using a query
def retrieve_documents(query, index, documents, embedding_model, top_k=5):
    query_embedding = embedding_model.encode([query])
    # Perform similarity search in the FAISS index
    distances, indices = index.search(np.array(query_embedding).astype("float32"), top_k)
    # Retrieve the top matching document chunks
    return [documents[i] for i in indices[0]]

# Generate augmented answer based on query and retrieved documents
def generate_augmented_answer(query,context):

    # Using a summarization pipeline for now, you can replace this with other pipelines based on your needs
    # Initialize the BERT question-answering model (fine-tuned on SQuAD)
    qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
    result = qa_pipeline(question=query, context=context)
    return result['answer']
    # model_name = "t5-small"  # You can switch to larger models as needed
    # model = pipeline("summarization", model=model_name)

    # # Combine the context with the query to provide a more detailed response
    # input_text = f"Context: {context}\nQuestion: {query}"

    # # Use the model to generate a response
    # summary = model(input_text, max_length=200, min_length=50, do_sample=False)

    # return summary[0]['summary_text']
