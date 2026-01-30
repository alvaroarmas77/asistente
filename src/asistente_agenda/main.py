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
    os.environ["GOOGLE_API_KEY"] = raw_key
    os.environ["GEMINI_API_KEY"] = raw_key
    os.environ["LITELLM_LOCAL_RESOURCES"] = "True"
    os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
    os.environ["VIRTUAL_ENV"] = "True" 
    return raw_key

def run():
    setup_environment()
    
    # --- THE PATH FIX ---
    # This finds the 'src/asistente_agenda' folder and adds it to the search path
    current_file_path = os.path.abspath(__file__) # Path to main.py
    package_dir = os.path.dirname(current_file_path) # Path to asistente_agenda folder
    
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)
    # --------------------

    try:
        from crew import AsistenteAgendaCrew
        import crew as crew_mod
    except ImportError:
        from asistente_agenda.crew import AsistenteAgendaCrew
        import asistente_agenda.crew as crew_mod

    print(f"DEBUG: Loading crew from: {crew_mod.__file__}")

    inputs = {
        'Nombre': 'Juan', 'apellido': 'Perez',
        'solicitud de cita': 'Quiero una cita para mañana a las 3pm para una revisión técnica.',
        'Correo electrónico': 'juan.perez@example.com',
        'número de WhatsApp': '+51999888777',
        'fecha y duración de la cita': 'Mañana a las 15:00 (1 hora)',
        'propósito de la cita': 'Revisión técnica'
    }
    
    try:
        crew_instance = AsistenteAgendaCrew()
        crew_instance.crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()