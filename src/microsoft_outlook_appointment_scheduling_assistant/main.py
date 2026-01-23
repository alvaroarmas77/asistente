#!/usr/bin/env python
import sys
import os
from microsoft_outlook_appointment_scheduling_assistant.crew import MicrosoftOutlookAppointmentSchedulingAssistantCrew

# --- FIX: Ensure the environment knows to use Gemini if not already set ---
# This looks for the key you uploaded during 'crewai deploy create'
if not os.getenv("GEMINI_API_KEY"):
    print("Warning: GEMINI_API_KEY not found in environment variables.")

def run():
    """
    Run the crew.
    """
    inputs = {
        'Nombre': 'sample_value',
        'apellido': 'sample_value',
        'apellidos': 'sample_value'
    }
    try:
        # We initialize the crew and kickoff
        # Make sure your crew.py is using the LLM(model="gemini/gemini-1.5-flash")
        MicrosoftOutlookAppointmentSchedulingAssistantCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"CRITICAL ERROR during kickoff: {e}")
        sys.exit(1)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'Nombre': 'sample_value',
        'apellido': 'sample_value',
        'apellidos': 'sample_value'
    }
    try:
        MicrosoftOutlookAppointmentSchedulingAssistantCrew().crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2], 
            inputs=inputs
        )
    except Exception as e:
        print(f"An error occurred while training the crew: {e}")
        sys.exit(1)

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MicrosoftOutlookAppointmentSchedulingAssistantCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        print(f"An error occurred while replaying the crew: {e}")
        sys.exit(1)

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'Nombre': 'sample_value',
        'apellido': 'sample_value',
        'apellidos': 'sample_value'
    }
    try:
        # FIX: Changed 'openai_model_name' to a generic model variable to avoid OpenAI errors
        model_name = sys.argv[2] if len(sys.argv) > 2 else "gemini/gemini-1.5-flash"
        MicrosoftOutlookAppointmentSchedulingAssistantCrew().crew().test(
            n_iterations=int(sys.argv[1]), 
            openai_model_name=model_name, 
            inputs=inputs
        )
    except Exception as e:
        print(f"An error occurred while testing the crew: {e}")
        sys.exit(1)

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
