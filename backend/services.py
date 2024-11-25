from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import load_dotenv

load_dotenv()

def process_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_answer_from_pdf(text: str, question: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "API key not found in environment variables. Please check your .env file."
    
    # Split text into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    try:
        # Create embeddings
        embeddings = OpenAIEmbeddings(api_key=api_key)
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # Get relevant chunks
        docs = knowledge_base.similarity_search(question)

        # Generate answer
        llm = ChatOpenAI(api_key=api_key, model_name="gpt-3.5-turbo", temperature=0)
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=question)
        
        return response
    except Exception as e:
        return f"API Error: {str(e)}. Please verify your OpenAI API key and billing setup at https://platform.openai.com/account/billing"