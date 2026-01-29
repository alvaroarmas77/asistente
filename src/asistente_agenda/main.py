#!/usr/bin/env python
import sys
import os

# SQLite Fix
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

def run():
    # Fetch the key
    raw_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not raw_key:
        print("ERROR: No API Key found.")
        sys.exit(1)
    
    # THE FIX: LiteLLM uses GEMINI_API_KEY. 
    # We DELETE GOOGLE_API_KEY to stop the buggy native SDK from triggering.
    os.environ["GEMINI_API_KEY"] = raw_key
    if "GOOGLE_API_KEY" in os.environ:
        del os.environ["GOOGLE_API_KEY"]
    
    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
    except ImportError:
        from crew import AsistenteAgendaCrew

    inputs = {
        'Nombre': 'Juan',
        'apellido': 'Perez',
        'solicitud de cita': 'Quiero una cita para mañana a las 3pm para una revisión técnica.'
    }
    
    print("## Starting Asistente Agenda Crew with forced LiteLLM routing...")
    AsistenteAgendaCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()