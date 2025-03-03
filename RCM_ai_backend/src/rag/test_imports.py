"""
Test imports for the RAG system
"""

print("Testing imports...")

# Test basic imports
try:
    import os
    import logging
    from typing import List, Dict, Any, Optional
    from pathlib import Path
    print("✓ Basic imports")
except ImportError as e:
    print(f"✗ Basic imports: {e}")

# Test environment and configuration
try:
    from dotenv import load_dotenv
    print("✓ dotenv")
except ImportError as e:
    print(f"✗ dotenv: {e}")

# Test LangChain imports
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    print("✓ langchain.text_splitter")
except ImportError as e:
    print(f"✗ langchain.text_splitter: {e}")

try:
    from langchain_community.vectorstores.chroma import Chroma
    print("✓ langchain_community.vectorstores.chroma")
except ImportError as e:
    print(f"✗ langchain_community.vectorstores.chroma: {e}")

try:
    from langchain_openai import ChatOpenAI
    print("✓ langchain_openai")
except ImportError as e:
    print(f"✗ langchain_openai: {e}")

# Test CrewAI imports
try:
    from crewai import Agent
    print("✓ crewai")
except ImportError as e:
    print(f"✗ crewai: {e}")

print("Import tests completed.") 