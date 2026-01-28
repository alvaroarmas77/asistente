__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

#!/usr/bin/env python
import os
from asistente_agenda.crew import AsistenteAgendaCrew

# Ensure the Gemini Key is recognized if you use it in this file
# os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

def run():
    """
    Run the crew.
    """
    inputs = {
        'Nombre': 'sample_value',
        'apellido': 'sample_value'
    }
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
        # Changed sys.argv indices because 'test' is sys.argv[1]
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