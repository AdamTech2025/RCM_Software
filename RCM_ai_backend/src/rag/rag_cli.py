"""
Command-Line Interface for RAG System with AI Agents

This script provides a command-line interface to interact with the RAG system.
"""

import argparse
import logging
import sys
from pathlib import Path

from rag_agent_system import RAGAgentSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command-line arguments
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="RAG System with AI Agents")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up the RAG system")
    setup_parser.add_argument("--force", action="store_true", help="Force reload of the vector store")
    setup_parser.add_argument("--data-dir", type=str, default="../data", help="Directory containing the data files")
    setup_parser.add_argument("--persist-dir", type=str, default="./chroma_db", help="Directory to persist the vector store")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the RAG system")
    query_parser.add_argument("query", type=str, help="Query to run")
    query_parser.add_argument("--data-dir", type=str, default="../data", help="Directory containing the data files")
    query_parser.add_argument("--persist-dir", type=str, default="./chroma_db", help="Directory to persist the vector store")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Run the RAG system in interactive mode")
    interactive_parser.add_argument("--data-dir", type=str, default="../data", help="Directory containing the data files")
    interactive_parser.add_argument("--persist-dir", type=str, default="./chroma_db", help="Directory to persist the vector store")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate the RAG system")
    validate_parser.add_argument("--data-dir", type=str, default="../data", help="Directory containing the data files")
    validate_parser.add_argument("--persist-dir", type=str, default="./chroma_db", help="Directory to persist the vector store")
    validate_parser.add_argument("--test-queries", type=str, default="test_queries.json", help="File containing test queries")
    validate_parser.add_argument("--results-file", type=str, default="validation_results.json", help="File to write validation results to")
    
    return parser.parse_args()

def setup_rag_system(args):
    """
    Set up the RAG system
    
    Args:
        args: Command-line arguments
    """
    logger.info("Setting up RAG system")
    
    # Initialize RAG system
    rag_system = RAGAgentSystem(
        data_dir=args.data_dir,
        persist_dir=args.persist_dir
    )
    
    # Set up RAG system
    rag_system.setup(force_reload=args.force)
    
    logger.info("RAG system setup complete")

def query_rag_system(args):
    """
    Query the RAG system
    
    Args:
        args: Command-line arguments
    """
    logger.info(f"Querying RAG system: {args.query}")
    
    # Initialize RAG system
    rag_system = RAGAgentSystem(
        data_dir=args.data_dir,
        persist_dir=args.persist_dir
    )
    
    # Set up RAG system
    rag_system.setup()
    
    # Query RAG system
    response = rag_system.query(args.query)
    
    print(f"\nQuery: {args.query}")
    print(f"\nResponse: {response}")

def run_interactive_mode(args):
    """
    Run the RAG system in interactive mode
    
    Args:
        args: Command-line arguments
    """
    logger.info("Running RAG system in interactive mode")
    
    # Initialize RAG system
    rag_system = RAGAgentSystem(
        data_dir=args.data_dir,
        persist_dir=args.persist_dir
    )
    
    # Set up RAG system
    rag_system.setup()
    
    print("\nRAG System with AI Agents")
    print("Type 'exit' or 'quit' to exit")
    
    while True:
        # Get query from user
        query = input("\nEnter your query: ")
        
        # Check if user wants to exit
        if query.lower() in ["exit", "quit"]:
            break
        
        # Query RAG system
        response = rag_system.query(query)
        
        print(f"\nResponse: {response}")

def validate_rag_system(args):
    """
    Validate the RAG system
    
    Args:
        args: Command-line arguments
    """
    logger.info("Validating RAG system")
    
    # Import validator
    from validate_rag_system import RAGSystemValidator
    
    # Initialize RAG system
    rag_system = RAGAgentSystem(
        data_dir=args.data_dir,
        persist_dir=args.persist_dir
    )
    
    # Set up RAG system
    rag_system.setup()
    
    # Initialize validator
    validator = RAGSystemValidator(
        rag_system=rag_system,
        test_queries_file=args.test_queries,
        results_file=args.results_file
    )
    
    # Validate RAG system
    validation_results = validator.validate()
    
    # Print validation results
    print(f"Overall score: {validation_results['overall_score']:.2f}")
    
    for i, result in enumerate(validation_results["results"]):
        print(f"\nQuery {i+1}: {result['query']}")
        print(f"Score: {result['evaluation']['score']:.2f}")
        print(f"Keywords found: {result['evaluation']['keywords_found']}/{result['evaluation']['total_keywords']}")
        
        # Print keyword results
        print("Keyword results:")
        for keyword, found in result["evaluation"]["keyword_results"].items():
            print(f"  - {keyword}: {'Found' if found else 'Not found'}")

def main():
    """
    Main function
    """
    # Parse command-line arguments
    args = parse_args()
    
    # Run command
    if args.command == "setup":
        setup_rag_system(args)
    elif args.command == "query":
        query_rag_system(args)
    elif args.command == "interactive":
        run_interactive_mode(args)
    elif args.command == "validate":
        validate_rag_system(args)
    else:
        print("No command specified, use --help for usage information")
        sys.exit(1)

if __name__ == "__main__":
    main() 