"""Configuration settings for the iOS Test Generator API"""
import os
from dotenv import load_dotenv


class Config:
    """Configuration class for the iOS Test Generator API"""

    def __init__(self):
        load_dotenv()

        # Anthropic/LLM Configuration
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
        self.ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
        self.LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
        self.LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))

        # RAG Configuration
        self.RAG_PERSIST_DIR = os.getenv("RAG_PERSIST_DIR", "../python-rag/rag_store")
        self.RAG_COLLECTION = os.getenv("RAG_COLLECTION", "ios_app")
        self.RAG_EMBED_MODEL = os.getenv("RAG_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.RAG_TOP_K = int(os.getenv("RAG_TOP_K", "10"))

        # Server Configuration
        self.PORT = int(os.getenv("PORT", "8000"))
        self.HOST = os.getenv("HOST", "0.0.0.0")

        # API Configuration
        self.API_TITLE = "iOS Test Generator API"
        self.API_DESCRIPTION = "LLM-powered XCTest and XCUITest code generator (LangChain + Anthropic)"
        self.API_VERSION = "1.0.0"


# Global config instance
config = Config()
