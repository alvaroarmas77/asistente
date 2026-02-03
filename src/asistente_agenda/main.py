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
    raw_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    os.environ["GOOGLE_API_KEY"] = str(raw_key) if raw_key else ""
    os.environ["GEMINI_API_KEY"] = str(raw_key) if raw_key else ""
    os.environ["LITELLM_LOCAL_RESOURCES"] = "True"
    os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
    os.environ["VIRTUAL_ENV"] = "True" 
    return raw_key

def run():
    setup_environment()
    
    # --- THE PATH FIX ---
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

    # ✅ FIXED: Corrected the quote syntax and matched tasks.yaml variable
    inputs = {
        'appointment_request': 'Quiero una cita para mañana a las 3pm para una revisión técnica con Juan Perez (+51999888777).',
        'Nombre': 'Juan', 
        'apellido': 'Perez'
    }
    
    try:
        crew_instance = AsistenteAgendaCrew()
        # The kickoff starts the process
        result = crew_instance.crew().kickoff(inputs=inputs)
        print("\n✅ Crew Execution Complete!")
        print(result)
    except Exception as e:
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
