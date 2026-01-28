import sys

try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

#!/usr/bin/env python
import os
try:
    from asistente_agenda.crew import AsistenteAgendaCrew
except ImportError:
    from crew import AsistenteAgendaCrew

def run():
    """
    Run the crew.
    """
    # CRITICAL: Force the environment variable into the OS context 
    # so the LLM class sees it immediately.
    if not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

    inputs = {
        'Nombre': 'sample_value',
        'apellido': 'sample_value'
    }
    
    print("## Starting Asistente Agenda Crew...")
    AsistenteAgendaCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'Nombre': 'sample_value',
        'apellido': 'sample_value'
    }
    try:
        AsistenteAgendaCrew().crew().train(n_iterations=int(sys.argv[2]), filename=sys.argv[3], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AsistenteAgendaCrew().crew().replay(task_id=sys.argv[2])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'Nombre': 'sample_value',
        'apellido': 'sample_value'
    }
    try:
        AsistenteAgendaCrew().crew().test(n_iterations=int(sys.argv[2]), openai_model_name=sys.argv[3], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)