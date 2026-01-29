#!/usr/bin/env python
import sys
import os
import warnings

# 1. SQLite Fix (Mandatory for GitHub Actions/ChromaDB)
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

# Suppress minor warnings for cleaner logs
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def setup_environment():
    """Configures environment to force LiteLLM and avoid the buggy Native SDK."""
    raw_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not raw_key:
        print("ERROR: No API Key found in GitHub Secrets.")
        sys.exit(1)
    
    # Force LiteLLM by prioritizing GEMINI_API_KEY
    os.environ["GEMINI_API_KEY"] = raw_key
    os.environ["LITELLM_LOCAL_RESOURCES"] = "True"
    
    # Remove GOOGLE_API_KEY if present to prevent the Native SDK from auto-triggering
    if "GOOGLE_API_KEY" in os.environ:
        del os.environ["GOOGLE_API_KEY"]
    
    return raw_key

def run():
    setup_environment()
    
    # Import inside run to ensure SQLite fix is applied first
    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
    except ImportError:
        from crew import AsistenteAgendaCrew

    # THE FIX: Providing all variables required by your tasks.yaml placeholders
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
    print("## Environment: LiteLLM Bridge Forced (Safe Mode)\n")
    
    try:
        AsistenteAgendaCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"\n❌ Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()