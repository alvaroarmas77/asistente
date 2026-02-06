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
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    vertex_triggers = [
        "GOOGLE_CLOUD_PROJECT", 
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "VERTEXAI_PROJECT", 
        "VERTEXAI_LOCATION",
        "CLOUD_RUNTIME",
        "GOOGLE_SERVICE_ACCOUNT"
    ]
    for var in vertex_triggers:
        os.environ.pop(var, None)

    # 3. Explicitly set the key for the Generative AI path
    os.environ["GOOGLE_API_KEY"] = str(api_key)
    return api_key

def run():
    import os
    import sys

    # 1. TRIPLE-LOCK: Physically delete Vertex triggers from the Python procesimport os
    import sys

    # 1. TRIPLE-LOCK: Physically delete Vertex triggers from the Python process memory
    # This forces LiteLLM to use the API Key path instead of Google Cloud path.
    vars_to_kill = [
        "GOOGLE_CLOUD_PROJECT", 
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "VERTEXAI_PROJECT", 
        "VERTEXAI_LOCATION",
        "CLOUD_RUNTIME",
        "GOOGLE_SERVICE_ACCOUNT"
    ]
    for var in vars_to_kill:
        if var in os.environ:
            del os.environ[var]

    # 2. Setup path
    current_path = os.path.dirname(os.path.abspath(__file__))
    if current_path not in sys.path:
        sys.path.append(current_path)

    # 3. Kickoff logic (Ensure you import your crew here)
    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
    except ImportError:
        from crew import AsistenteAgendaCrew

    inputs = {
        'appointment_request': 'Quiero una cita para mañana a las 3pm para una revisión técnica con Juan Perez (+51999888777).',
        'Nombre': 'Juan',
        'apellido': 'Perez'
    }
    
    AsistenteAgendaCrew().crew().kickoff(inputs=inputs)s memory
    # This forces LiteLLM to use the API Key path instead of Google Cloud path.
    vars_to_kill = [
        "GOOGLE_CLOUD_PROJECT", 
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "VERTEXAI_PROJECT", 
        "VERTEXAI_LOCATION",
        "CLOUD_RUNTIME",
        "GOOGLE_SERVICE_ACCOUNT"
    ]
    for var in vars_to_kill:
        if var in os.environ:
            del os.environ[var]

    # 2. Setup path
    current_path = os.path.dirname(os.path.abspath(__file__))
    if current_path not in sys.path:
        sys.path.append(current_path)

    # Now you can safely import your crew and kickoff
    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
    except ImportError:
        from crew import AsistenteAgendaCrew

    setup_environment()
    
    current_file_path = os.path.abspath(__file__)
    package_dir = os.path.dirname(current_file_path)
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)

    try:
        from crew import AsistenteAgendaCrew
    except ImportError:
        from asistente_agenda.crew import AsistenteAgendaCrew

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