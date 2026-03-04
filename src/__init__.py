from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Update to Gemini 3.1 Pro
self.shared_llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-pro-preview", # No "gemini/" prefix here for LangChain
    google_api_key=os.getenv("GOOGLE_API_KEY"), # Ensure variable name matches GitHub Secrets
    temperature=1.0,               # Better for 3.1 Reasoning
    max_output_tokens=2048,
    timeout=None,
    max_retries=2,
    stop=None
)