#!/usr/bin/env python
import sys
import os
import warnings

# 1. SQLite Fix for environments without modern sqlite3
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def setup_environment():
    """Configures environment to force Google AI Studio and bypass Vertex AI."""
    raw_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not raw_key:
        print("❌ ERROR: No API Key found in environment variables.")
        return None

    # Force the key into both standard variable names
    os.environ["GOOGLE_API_KEY"] = raw_key
    os.environ["GEMINI_API_KEY"] = raw_key
    
    # CRITICAL: Prevent LiteLLM from searching for Google Cloud / Vertex credentials
    os.environ["LITELLM_LOCAL_RESOURCES"] = "True"
    
    # Remove any project ID or credentials path that might trigger Vertex logic
    os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    
    # Force LiteLLM to use the standard Google AI Studio base URL if it's confused
    os.environ["VIRTUAL_ENV"] = "True" 
    
    return raw_key

def run():
    key = setup_environment()
    if not key:
        sys.exit(1)
    
    # --- ENHANCED IMPORT LOGIC ---
    # This ensures tools inside crew.py are found correctly by adding the current path to sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
        import asistente_agenda.crew as crew_mod
    except ImportError:
        try:
            from crew import AsistenteAgendaCrew
            import crew as crew_mod
        except ImportError as e:
            print(f"❌ Critical Import Error: {e}")
            sys.exit(1)

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
    
    try:
        # Initialize the crew
        crew_instance = AsistenteAgendaCrew()
        
        # Verify the model name (from our crew.py fix)
        print(f"DEBUG: Using model string: {crew_instance.shared_llm.model}")
        
        # Start the process
        crew_instance.crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()