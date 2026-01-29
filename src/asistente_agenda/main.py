#!/usr/bin/env python
import sys
import os

# SQLite Fix for Cloud/Headless Environments
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

def run():
    # 1. Grab and standardize the API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: No API Key found.")
        sys.exit(1)
    
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key
    
    # 2. Local import to ensure environment is set
    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
    except ImportError:
        from crew import AsistenteAgendaCrew

    inputs = {
        'Nombre': 'Juan',
        'apellido': 'Perez',
        'solicitud de cita': 'Quiero una cita para mañana a las 3pm para una revisión técnica.'
    }
    
    print("## Starting Asistente Agenda Crew...")
    AsistenteAgendaCrew().crew().kickoff(inputs=inputs)

def train():
    from asistente_agenda.crew import AsistenteAgendaCrew
    inputs = {'Nombre': 'sample', 'apellido': 'value', 'solicitud de cita': 'sample'}
    try:
        AsistenteAgendaCrew().crew().train(n_iterations=int(sys.argv[2]), filename=sys.argv[3], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training: {e}")

def test():
    from asistente_agenda.crew import AsistenteAgendaCrew
    inputs = {'Nombre': 'sample', 'apellido': 'value', 'solicitud de cita': 'sample'}
    try:
        AsistenteAgendaCrew().crew().test(n_iterations=int(sys.argv[2]), openai_model_name=sys.argv[3], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command in ["train", "test"]:
        if len(sys.argv) < 4:
            print(f"Usage: main.py {command} <iterations> <filename/model>")
            sys.exit(1)
        globals()[command]()