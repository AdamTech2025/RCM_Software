# RAG System with AI Agents using ChromaDB

This directory contains a Retrieval-Augmented Generation (RAG) system using AI agents with ChromaDB as the vector database. The system processes medical coding documents and provides accurate responses to queries about medical coding, billing, and related topics.

## Features

- **Document Processing**: Processes PDF, text, and JSON files from the data directory
- **Vector Database**: Uses ChromaDB to store and retrieve document embeddings
- **AI Agents**: Uses CrewAI to create a team of AI agents for retrieval, analysis, and validation
- **Command-Line Interface**: Provides a command-line interface to interact with the RAG system
- **Validation**: Includes a validation script to evaluate the RAG system's performance

## Requirements

Make sure you have the following dependencies installed:

```bash
pip install -r ../../requirements.txt
```

## Usage

### Setting Up the RAG System

To set up the RAG system, run:

```bash
python rag_cli.py setup
```

This will process the documents in the data directory and create a vector database in the `chroma_db` directory.

To force a reload of the vector database, use the `--force` flag:

```bash
python rag_cli.py setup --force
```

### Querying the RAG System

To query the RAG system, run:

```bash
python rag_cli.py query "What are the CPT codes for a routine physical examination?"
```

### Interactive Mode

To run the RAG system in interactive mode, run:

```bash
python rag_cli.py interactive
```

This will start an interactive session where you can enter queries and get responses.

### Validating the RAG System

To validate the RAG system, run:

```bash
python rag_cli.py validate
```

This will run a series of test queries and evaluate the responses.

## File Structure

- `rag_agent_system.py`: Main implementation of the RAG system
- `validate_rag_system.py`: Validation script for the RAG system
- `rag_cli.py`: Command-line interface for the RAG system
- `test_queries.json`: Default test queries for validation (created automatically)
- `validation_results.json`: Validation results (created automatically)
- `chroma_db/`: Directory to persist the vector database (created automatically)

## Customization

You can customize the RAG system by modifying the following parameters:

- `data_dir`: Directory containing the data files
- `persist_dir`: Directory to persist the vector database
- `embedding_model_name`: Name of the embedding model to use
- `llm_model_name`: Name of the LLM to use
- `chunk_size`: Size of chunks to split documents into
- `chunk_overlap`: Overlap between chunks

For example:

```bash
python rag_cli.py setup --data-dir "../custom_data" --persist-dir "./custom_db"
```

## API Key Setup

This system requires an OpenAI API key for the LLM. Make sure to set the `OPENAI_API_KEY` environment variable or add it to the `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

## Example Queries

Here are some example queries you can try:

- "What are the CPT codes for a routine physical examination?"
- "How do I code for a dermatology consultation?"
- "What is the ICD-10 code for type 2 diabetes?"
- "Explain the difference between CPT and HCPCS codes."
- "What documentation is required for billing a level 4 E/M visit?" 