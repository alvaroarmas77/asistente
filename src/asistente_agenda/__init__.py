def __init__(self):
        # We use the explicit LangChain class to avoid naming/routing issues
        self.shared_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            verbose=True,
            temperature=0.5,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )