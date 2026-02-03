#!/usr/bin/env python
import sys
import os
import warnings

# 1. SQLite Fix
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def setup_environment():
    # Get the key
    raw_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not raw_key:
        print("⚠️ WARNING: No Google API Key found!")
    
    # --- THE MAGIC FIX: FORCE AI STUDIO ENDPOINT ---
    # This tells LiteLLM exactly where to go, bypassing the Vertex AI logic
    os.environ["GOOGLE_API_KEY"] = str(raw_key) if raw_key else ""
    os.environ["GEMINI_API_KEY"] = str(raw_key) if raw_key else ""
    os.environ["GOOGLE_AI_STUDIO_API_KEY"] = str(raw_key) if raw_key else ""
    
    # Force the API Base to Google AI Studio
    os.environ.pop("GEMINI_API_BASE", None)
    
    # Disable LiteLLM's automatic attempt to use local Google Cloud credentials
    os.environ["LITELLM_LOCAL_RESOURCES"] = "True"
    
    # 🚨 THE VERTEX KILLERS: Strip every variable that triggers Vertex AI
    vars_to_remove = [
        "GOOGLE_CLOUD_PROJECT", 
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "VERTEXAI_PROJECT", 
        "VERTEXAI_LOCATION",
        "CLOUD_RUNTIME" # Some runners use this to auto-detect GCP
    ]
    for var in vars_to_remove:
        os.environ.pop(var, None)
            
    os.environ["VIRTUAL_ENV"] = "True" 
    return raw_key

def run():
    setup_environment()
    
    # --- PATH LOGIC ---
    current_file_path = os.path.abspath(__file__)
    package_dir = os.path.dirname(current_file_path)
    
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)

    try:
        from crew import AsistenteAgendaCrew
        import crew as crew_mod
    except ImportError:
        from asistente_agenda.crew import AsistenteAgendaCrew
        import asistente_agenda.crew as crew_mod

    print(f"DEBUG: Loading crew from: {crew_mod.__file__}")

    inputs = {
        'appointment_request': 'Quiero una cita para mañana a las 3pm para una revisión técnica con Juan Perez (+51999888777).',
        'Nombre': 'Juan', 
        'apellido': 'Perez'
    }
    
    try:
        # Initialize and kickoff
        crew_instance = AsistenteAgendaCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)
        print("\n✅ Crew Execution Complete!")
        print(result)
    except Exception as e:
        # Final catch for the Vertex error to give us info
        if "VertexAIException" in str(e) or "404" in str(e):
            print("\n❌ LLM ROUTING ERROR: LiteLLM is still being pulled toward Vertex AI.")
            print("Action: Check if 'langchain-google-genai' is in requirements.txt")
        
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
