#!/usr/bin/env python
import sys
import os
import warnings

# 1. SQLite Fix for environments like GitHub Actions
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def setup_environment():
    # Supports both naming conventions
    raw_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not raw_key:
        print("⚠️ WARNING: No API Key found!")
    
    # Force API Studio keys into environment
    os.environ["GOOGLE_API_KEY"] = str(raw_key) if raw_key else ""
    os.environ["GEMINI_API_KEY"] = str(raw_key) if raw_key else ""
    os.environ["LITELLM_LOCAL_RESOURCES"] = "True"
    
    # 🚨 THE VERTEX KILLERS: Prevent LiteLLM from drifting into Google Cloud
    vars_to_remove = [
        "GOOGLE_CLOUD_PROJECT", 
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "VERTEXAI_PROJECT", 
        "VERTEXAI_LOCATION",
        "CLOUD_RUNTIME"
    ]
    for var in vars_to_remove:
        os.environ.pop(var, None)
            
    return raw_key

def run():
    setup_environment()
    
    # Path logic to ensure imports work in GitHub Actions
    current_file_path = os.path.abspath(__file__)
    package_dir = os.path.dirname(current_file_path)
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)

    try:
        from crew import AsistenteAgendaCrew
    except ImportError:
        from asistente_agenda.crew import AsistenteAgendaCrew

    # ✅ Inputs strictly matched to tasks.yaml variables
    inputs = {
        'appointment_request': 'Quiero una cita para mañana a las 3pm para una revisión técnica con Juan Perez (+51999888777).',
        'Nombre': 'Juan', 
        'apellido': 'Perez'
    }
    
    try:
        crew_instance = AsistenteAgendaCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)
        print("\n✅ Crew Execution Complete!")
        print(result)
    except Exception as e:
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()