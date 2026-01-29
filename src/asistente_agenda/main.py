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
    """Configures environment to force LiteLLM and avoid VertexAI."""
    raw_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not raw_key:
        print("ERROR: No API Key found in GitHub Secrets.")
        sys.exit(1)
    
    # Standardize keys for LiteLLM 'google_ai' provider
    os.environ["GOOGLE_API_KEY"] = raw_key
    os.environ["GEMINI_API_KEY"] = raw_key
    # os.environ["LITELLM_LOCAL_RESOURCES"] = "True" 
    
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