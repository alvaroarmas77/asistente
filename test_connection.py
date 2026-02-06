import os
import google.generativeai as genai

def test_gemini_connection():
    # 1. Get the key
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"--- Diagnostic Start ---")
    print(f"Key found: {'Yes (Starts with ' + api_key[:8] + ')' if api_key else 'No'}")
    
    if not api_key:
        print("ERROR: GOOGLE_API_KEY is missing from environment!")
        return

    try:
        # 2. Configure the NATIVE Google SDK (Bypassing LiteLLM/Vertex)
        genai.configure(api_key=api_key)
        
        # 3. List available models (Checks if key has permissions)
        print("Checking available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" - Found: {m.name}")

        # 4. Attempt a simple generation
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Responde 'Conexión Exitosa' si puedes leer esto.")
        
        print(f"\n--- Result ---")
        print(f"Gemini Response: {response.text}")
        print(f"Status: SUCCESS ✅")

    except Exception as e:
        print(f"\n--- Result ---")
        print(f"Status: FAILED ❌")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")

if __name__ == "__main__":
    test_gemini_connection()