"""
RAG System with AI Agents using ChromaDB

This module implements a Retrieval-Augmented Generation (RAG) system using AI agents
with ChromaDB as the vector database. The system processes medical coding documents
and provides accurate responses to queries about medical coding, billing, and related topics.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Environment and configuration
from dotenv import load_dotenv

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    JSONLoader
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.tasks.task_output import TaskOutput

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class RAGAgentSystem:
    """
    RAG System with AI Agents using ChromaDB
    """
    
    def __init__(
        self, 
        data_dir: str = "../data",
        persist_dir: str = "./chroma_db",
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model_name: str = "gpt-3.5-turbo",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the RAG system
        
        Args:
            data_dir: Directory containing the data files
            persist_dir: Directory to persist the vector database
            embedding_model_name: Name of the embedding model to use
            llm_model_name: Name of the LLM to use
            chunk_size: Size of chunks to split documents into
            chunk_overlap: Overlap between chunks
        """
        self.data_dir = Path(data_dir)
        self.persist_dir = Path(persist_dir)
        self.embedding_model_name = embedding_model_name
        self.llm_model_name = llm_model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name=llm_model_name,
            temperature=0.2,
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
        # Initialize vector store
        self.vector_store = None
        
    def load_documents(self) -> List[Any]:
        """
        Load documents from the data directory
        
        Returns:
            List of documents
        """
        logger.info(f"Loading documents from {self.data_dir}")
        
        documents = []
        
        # Load PDF files
        pdf_files = list(self.data_dir.glob("*.pdf"))
        for pdf_file in pdf_files:
            logger.info(f"Loading PDF file: {pdf_file}")
            loader = PyPDFLoader(str(pdf_file))
            documents.extend(loader.load())
        
        # Load text files
        txt_files = list(self.data_dir.glob("*.txt"))
        for txt_file in txt_files:
            logger.info(f"Loading text file: {txt_file}")
            loader = TextLoader(str(txt_file))
            documents.extend(loader.load())
        
        # Load JSON files
        json_files = list(self.data_dir.glob("*.json"))
        for json_file in json_files:
            logger.info(f"Loading JSON file: {json_file}")
            # For JSON files, we need to specify the jq schema to extract text
            # This is a simple example, you might need to adjust based on your JSON structure
            loader = JSONLoader(
                file_path=str(json_file),
                jq_schema='.',
                text_content=False
            )
            documents.extend(loader.load())
        
        logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    def process_documents(self, documents: List[Any]) -> List[Any]:
        """
        Process documents by splitting them into chunks
        
        Args:
            documents: List of documents to process
            
        Returns:
            List of processed document chunks
        """
        logger.info("Processing documents")
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        logger.info(f"Split documents into {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, chunks: List[Any]) -> None:
        """
        Create a vector store from document chunks
        
        Args:
            chunks: List of document chunks
        """
        logger.info("Creating vector store")
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=str(self.persist_dir)
        )
        
        # Persist vector store
        self.vector_store.persist()
        
        logger.info(f"Created vector store with {len(chunks)} chunks")
    
    def load_vector_store(self) -> None:
        """
        Load an existing vector store
        """
        logger.info(f"Loading vector store from {self.persist_dir}")
        
        # Load vector store
        self.vector_store = Chroma(
            persist_directory=str(self.persist_dir),
            embedding_function=self.embeddings
        )
        
        logger.info("Loaded vector store")
    
    def setup(self, force_reload: bool = False) -> None:
        """
        Set up the RAG system
        
        Args:
            force_reload: Whether to force reload the vector store
        """
        # Check if vector store already exists
        if not force_reload and self.persist_dir.exists():
            logger.info("Vector store already exists, loading it")
            self.load_vector_store()
        else:
            logger.info("Creating new vector store")
            # Load and process documents
            documents = self.load_documents()
            chunks = self.process_documents(documents)
            
            # Create vector store
            self.create_vector_store(chunks)
    
    def create_agents(self) -> Dict[str, Agent]:
        """
        Create AI agents for the RAG system
        
        Returns:
            Dictionary of agents
        """
        logger.info("Creating AI agents")
        
        # Create retriever agent
        retriever_agent = Agent(
            role="Medical Coding Retriever",
            goal="Retrieve the most relevant information from the knowledge base",
            backstory="""You are an expert in medical coding and billing. 
            Your job is to retrieve the most relevant information from the knowledge base
            to answer questions about medical coding, billing, and related topics.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Create analyzer agent
        analyzer_agent = Agent(
            role="Medical Coding Analyzer",
            goal="Analyze the retrieved information and provide accurate answers",
            backstory="""You are an expert in medical coding and billing analysis.
            Your job is to analyze the information retrieved from the knowledge base
            and provide accurate answers to questions about medical coding, billing, and related topics.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        # Create validator agent
        validator_agent = Agent(
            role="Medical Coding Validator",
            goal="Validate the accuracy of the answers provided",
            backstory="""You are an expert in medical coding and billing validation.
            Your job is to validate the accuracy of the answers provided by the analyzer
            and ensure they are correct and complete.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        return {
            "retriever": retriever_agent,
            "analyzer": analyzer_agent,
            "validator": validator_agent
        }
    
    def create_tasks(self, agents: Dict[str, Agent], query: str) -> List[Task]:
        """
        Create tasks for the AI agents
        
        Args:
            agents: Dictionary of agents
            query: User query
            
        Returns:
            List of tasks
        """
        logger.info("Creating tasks")
        
        # Create retrieval task
        retrieval_task = Task(
            description=f"""
            Retrieve the most relevant information from the knowledge base to answer the following question:
            {query}
            
            Use the vector store to find the most relevant documents.
            """,
            expected_output="A comprehensive set of relevant information from the knowledge base",
            agent=agents["retriever"]
        )
        
        # Create analysis task
        analysis_task = Task(
            description=f"""
            Analyze the retrieved information and provide an accurate answer to the following question:
            {query}
            
            Use the information provided by the retriever to formulate a comprehensive answer.
            """,
            expected_output="A comprehensive and accurate answer to the question",
            agent=agents["analyzer"],
            context=[retrieval_task]
        )
        
        # Create validation task
        validation_task = Task(
            description=f"""
            Validate the accuracy of the answer provided by the analyzer for the following question:
            {query}
            
            Check if the answer is correct, complete, and addresses all aspects of the question.
            If there are any issues, provide corrections or additional information.
            """,
            expected_output="A validated and potentially enhanced answer to the question",
            agent=agents["validator"],
            context=[analysis_task]
        )
        
        return [retrieval_task, analysis_task, validation_task]
    
    def query(self, query: str) -> str:
        """
        Query the RAG system
        
        Args:
            query: User query
            
        Returns:
            Response from the RAG system
        """
        logger.info(f"Querying RAG system: {query}")
        
        # Check if vector store is initialized
        if self.vector_store is None:
            logger.error("Vector store not initialized, call setup() first")
            return "Error: Vector store not initialized"
        
        # Create a simple retrieval chain for the retriever agent to use
        retrieval_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 5}
            ),
            return_source_documents=True,
            verbose=True
        )
        
        # Create agents
        agents = self.create_agents()
        
        # Create tasks
        tasks = self.create_tasks(agents, query)
        
        # Create crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )
        
        # Execute crew
        result = crew.kickoff()
        
        logger.info(f"RAG system response: {result}")
        return result

def main():
    """
    Main function to demonstrate the RAG system
    """
    # Initialize RAG system
    rag_system = RAGAgentSystem(
        data_dir="../data",
        persist_dir="./chroma_db"
    )
    
    # Set up RAG system
    rag_system.setup(force_reload=True)
    
    # Query RAG system
    query = "What are the CPT codes for a routine physical examination?"
    response = rag_system.query(query)
    
    print(f"Query: {query}")
    print(f"Response: {response}")

if __name__ == "__main__":
    main() 