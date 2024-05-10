'''
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredFileLoader
import tkinter as tk
from tkinter import filedialog
import shutil
import os
import sys

def from_web(url):
    # Load, chunk and index the contents of the blog.
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.load()
    return docs

def from_pdf(file_address):
    pass


CHROMA_PATH = "../../chroma_db"
DATA_PATH = "../../../Data"

def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        loader = UnstructuredFileLoader(file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} documents from {file_path}")
    else:
        print("No file selected.")

    root.destroy()
    
    loader = UnstructuredFileLoader(DATA_PATH)
    #loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


def retriever_from_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    #print(f"Number of split documents: {len(splits)}")
    Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(),persist_directory="../../chroma_db")
    print("Embeddings are added to vector store.")
    #return vector_store


if __name__ == "__main__":
    load_dotenv()
    retriever_from_docs(from_web(sys.argv[1]))
'''


import bs4
import pandas as pd
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain.document_loaders import PyPDFLoader, CSVLoader, ExcelLoader
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
#from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import sys
import shutil
import os
import uuid

'''
def from_web(url, selectors="div.job-description"):

    # Create a parser object with the specified selectors
    parser_kwargs = {}
    if selectors:
        parser_kwargs["bs_kwargs"] = dict(parse_only=bs4.SoupStrainer(selectors))
    
    # Load, chunk and index the contents of the blog.
    loader = WebBaseLoader(
        web_paths=(url,), **parser_kwargs,
    )
    docs = loader.load()
    return docs
'''

def from_web(url):
    loader = WebBaseLoader(web_paths=(url,),
                           bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                               class_=("post-content", "post-title", "post-header")
                           )),)
    docs = loader.load()
    return docs

def from_excel(file_address):
    docs = []
    for file_name in os.listdir(file_address):
        file_path = os.path.join(file_address, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".xlsx"):
            # Load the Excel file
            loader = UnstructuredExcelLoader(file_path=file_address)
            docs.extend(loader.load())
    return docs

def from_csv(file_address):
    # Load the CSV filecd 
    loader = CSVLoader(file_path=file_address)
    docs = loader.load()
    return docs

def from_pdf(file_address):
    loader = PyPDFLoader(file_path=file_address)
    docs = loader.load()
    return docs

def from_text_files(file_address):
    docs = []
    for file_name in os.listdir(file_address):
        file_path = os.path.join(file_address, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".txt"):
            loader = TextLoader(file_path)
            docs.extend(loader.load())
    return docs

def retriever_from_docs(docs):
    if not docs:
        print("No documents to process.")
        return
    #print("Documents:", docs)

    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"Number of document chunks: {len(splits)}")

    # Create embeddings for the document chunks
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    embeddings_list = embeddings.embed_documents([t.page_content for t in splits])
    
    # Generate unique IDs for each document chunk
    doc_ids = [str(uuid.uuid4()) for _ in range(len(splits))]
    print(f"Number of IDs generated: {len(doc_ids)}")

    # Create or load the Chroma vector store
    persist_directory="../../chroma_db"

    # Check if the directory exists
    if os.path.exists(persist_directory):
        # Remove the directory and its contents
        shutil.rmtree(persist_directory)
        print(f"Deleted {persist_directory}")

        # Load the existing vector store
        chroma_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    
    else:
        print(f"{persist_directory} does not exist")
        # Create a new vector store
        chroma_store = Chroma.from_documents(documents=splits, embedding=embeddings, 
                                             persist_directory=persist_directory)
    
    #Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(),persist_directory="../../chroma_db")
    #chroma_store = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="../../chroma_db")
    
    # Add the document chunks and embeddings to the vector store
    chroma_store.add_texts([t.page_content for t in splits], embeddings=embeddings_list
                           , ids=doc_ids)
    print("Embeddings are added to vector store.")
    

def main():
    print(sys.argv)
    load_dotenv()

    #file_address = "../../../db_28_2_text/db_28_2_text/"
    file_address = "../../../db_28_2_excel/db_28_2_excel/"

    # Check if the file_address exists
    if not os.path.exists(file_address):
        print("File address does not exist.")
        return

    # Determine the input type and load the documents accordingly
    if 'http' in sys.argv[1].lower():
        retriever_from_docs(from_web(sys.argv[1]))
    elif '.xls' in sys.argv[1].lower():
        retriever_from_docs(from_excel(sys.argv[1]))
    elif '.csv' in sys.argv[1].lower():
        retriever_from_docs(from_csv(sys.argv[1]))
    elif '.pdf' in sys.argv[1].lower():
        retriever_from_docs(from_pdf(sys.argv[1]))
    elif '.txt' in sys.argv[1].lower():
        retriever_from_docs(from_text_files(sys.argv[1]))
    elif 'excel' in sys.argv[1].lower():
        retriever_from_docs(from_excel(sys.argv[1]))
    elif 'text' in sys.argv[1].lower():
        retriever_from_docs(from_text_files(sys.argv[1]))
    else:
        print(f"Unsupported file format for file.")
    
if __name__ == "__main__":
    main()