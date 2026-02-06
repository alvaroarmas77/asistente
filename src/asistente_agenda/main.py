#!/usr/bin/env python
import sys
import os
import warnings

# SQLite Fix for environments like GitHub Actions
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def setup_environment():
    # Clear Vertex triggers to prevent DefaultCredentialsError
    vars_to_kill = [
        "GOOGLE_CLOUD_PROJECT", 
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "VERTEXAI_PROJECT", 
        "VERTEXAI_LOCATION",
        "CLOUD_RUNTIME",
        "GOOGLE_SERVICE_ACCOUNT"
    ]
    for var in vars_to_kill:
        os.environ.pop(var, None)
    
    # Force LiteLLM to use local API keys
    os.environ["LITELLM_LOCAL_RESOURCES"] = "True"

def run():
    setup_environment()

    # Setup pathing
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
    except ImportError:
        from crew import AsistenteAgendaCrew

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