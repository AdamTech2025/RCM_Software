"""
Validation Script for RAG System with AI Agents

This script validates the RAG system by running a series of test queries
and evaluating the responses.
"""

import logging
import json
from pathlib import Path
from typing import List, Dict, Any

from rag_agent_system import RAGAgentSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGSystemValidator:
    """
    Validator for the RAG system
    """
    
    def __init__(
        self,
        rag_system: RAGAgentSystem,
        test_queries_file: str = "test_queries.json",
        results_file: str = "validation_results.json"
    ):
        """
        Initialize the validator
        
        Args:
            rag_system: RAG system to validate
            test_queries_file: File containing test queries
            results_file: File to write validation results to
        """
        self.rag_system = rag_system
        self.test_queries_file = Path(test_queries_file)
        self.results_file = Path(results_file)
        
        # Create default test queries if file doesn't exist
        if not self.test_queries_file.exists():
            self.create_default_test_queries()
    
    def create_default_test_queries(self) -> None:
        """
        Create default test queries
        """
        logger.info(f"Creating default test queries file: {self.test_queries_file}")
        
        # Default test queries
        test_queries = [
            {
                "query": "What are the CPT codes for a routine physical examination?",
                "expected_keywords": ["physical examination", "CPT", "code", "routine"]
            },
            {
                "query": "How do I code for a dermatology consultation?",
                "expected_keywords": ["dermatology", "consultation", "code"]
            },
            {
                "query": "What is the ICD-10 code for type 2 diabetes?",
                "expected_keywords": ["ICD-10", "diabetes", "type 2"]
            },
            {
                "query": "Explain the difference between CPT and HCPCS codes.",
                "expected_keywords": ["CPT", "HCPCS", "difference"]
            },
            {
                "query": "What documentation is required for billing a level 4 E/M visit?",
                "expected_keywords": ["documentation", "level 4", "E/M", "billing"]
            }
        ]
        
        # Write test queries to file
        with open(self.test_queries_file, "w") as f:
            json.dump(test_queries, f, indent=2)
    
    def load_test_queries(self) -> List[Dict[str, Any]]:
        """
        Load test queries from file
        
        Returns:
            List of test queries
        """
        logger.info(f"Loading test queries from {self.test_queries_file}")
        
        # Load test queries from file
        with open(self.test_queries_file, "r") as f:
            test_queries = json.load(f)
        
        logger.info(f"Loaded {len(test_queries)} test queries")
        return test_queries
    
    def evaluate_response(self, response: str, expected_keywords: List[str]) -> Dict[str, Any]:
        """
        Evaluate a response against expected keywords
        
        Args:
            response: Response to evaluate
            expected_keywords: Expected keywords in the response
            
        Returns:
            Evaluation results
        """
        # Convert response to lowercase for case-insensitive matching
        response_lower = response.lower()
        
        # Check if each expected keyword is in the response
        keyword_results = {}
        for keyword in expected_keywords:
            keyword_lower = keyword.lower()
            keyword_results[keyword] = keyword_lower in response_lower
        
        # Calculate overall score
        keywords_found = sum(1 for result in keyword_results.values() if result)
        total_keywords = len(expected_keywords)
        score = keywords_found / total_keywords if total_keywords > 0 else 0
        
        return {
            "keyword_results": keyword_results,
            "keywords_found": keywords_found,
            "total_keywords": total_keywords,
            "score": score
        }
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate the RAG system
        
        Returns:
            Validation results
        """
        logger.info("Validating RAG system")
        
        # Load test queries
        test_queries = self.load_test_queries()
        
        # Run test queries
        results = []
        for test_query in test_queries:
            query = test_query["query"]
            expected_keywords = test_query["expected_keywords"]
            
            logger.info(f"Running test query: {query}")
            
            # Query RAG system
            response = self.rag_system.query(query)
            
            # Evaluate response
            evaluation = self.evaluate_response(response, expected_keywords)
            
            # Add to results
            results.append({
                "query": query,
                "response": response,
                "expected_keywords": expected_keywords,
                "evaluation": evaluation
            })
        
        # Calculate overall score
        overall_score = sum(result["evaluation"]["score"] for result in results) / len(results) if results else 0
        
        # Create validation results
        validation_results = {
            "results": results,
            "overall_score": overall_score
        }
        
        # Write validation results to file
        with open(self.results_file, "w") as f:
            json.dump(validation_results, f, indent=2)
        
        logger.info(f"Validation complete, overall score: {overall_score:.2f}")
        return validation_results

def main():
    """
    Main function to validate the RAG system
    """
    # Initialize RAG system
    rag_system = RAGAgentSystem(
        data_dir="../data",
        persist_dir="./chroma_db"
    )
    
    # Set up RAG system
    rag_system.setup()
    
    # Initialize validator
    validator = RAGSystemValidator(rag_system)
    
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

if __name__ == "__main__":
    main() 