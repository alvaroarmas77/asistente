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
    
    # 1. Standard API Key Setup
    os.environ["GOOGLE_API_KEY"] = raw_key
    os.environ["GEMINI_API_KEY"] = raw_key
    
    # 2. THE FIX: Force LiteLLM to ignore Google Cloud/Vertex logic
    os.environ["LITELLM_LOCAL_RESOURCES"] = "True"
    
    # 3. Explicitly tell LiteLLM NOT to use Vertex AI
    # This prevents it from looking for 'Default Credentials'
    os.environ["VIRTUAL_ENV"] = "True" 
    
    return raw_key



def run():
    setup_environment()
    
    # Simplified import to match the PYTHONPATH: src/
    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
        import asistente_agenda.crew as crew_mod
        print(f"DEBUG: Loading crew from: {crew_mod.__file__}")
    except ImportError:
        from crew import AsistenteAgendaCrew
        import crew as crew_mod
        print(f"DEBUG: Loading crew from: {crew_mod.__file__}")

    inputs = {
        'Nombre': 'Juan',
        'apellido': 'Perez',
        'solicitud de cita': 'Quiero una cita para mañana a las 3pm para una revisión técnica.',
        'Correo electrónico': 'juan.perez@example.com',
        'número de WhatsApp': '+51999888777',
        'fecha y duración de la cita': 'Mañana a las 15:00 (1 hora)',
        'propósito de la cita': 'Revisión técnica'
    }
    
    print("\n## Starting Asistente Agenda Crew...")
    
    # Debug: Check the LLM config right before kickoff
    crew_instance = AsistenteAgendaCrew()
    print(f"DEBUG: Using model: {crew_instance.shared_llm.model}")
    
    try:
        crew_instance.crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()