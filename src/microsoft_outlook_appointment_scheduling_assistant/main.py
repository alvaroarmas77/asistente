#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv

# 1. Load environment variables at the very beginning
load_dotenv()

# 2. Add 'src' to path only once and clean up imports
sys.path.append(os.path.join(os.getcwd(), "src"))

from microsoft_outlook_appointment_scheduling_assistant.crew import MicrosoftOutlookAppointmentSchedulingAssistantCrew

def run():
    """
    Run the crew.
    """
    print("--- Starting Execution ---")
    
    # Updated inputs: Removed 'sample_value' with placeholders you can edit
    inputs = {
        'Nombre': 'Juan',
        'apellido': 'Perez',
        'apellidos': 'Perez Garcia'
    }
    
    try:
        # Initialize and kickoff the crew
        # Note: Ensure your crew.py uses LLM(model="gemini/gemini-1.5-flash")
        result = MicrosoftOutlookAppointmentSchedulingAssistantCrew().crew().kickoff(inputs=inputs)
        
        print("\n--- FINAL RESULT ---")
        print(result)
        return result
        
    except Exception as e:
        print(f"--- ERROR DURING EXECUTION: {e} ---")
        sys.exit(1)

def train():
    """Train the crew."""
    inputs = {'Nombre': 'Juan', 'apellido': 'Perez', 'apellidos': 'Perez Garcia'}
    try:
        if len(sys.argv) < 4:
            print("Usage: main.py train <iterations> <filename>")
            return
        
        MicrosoftOutlookAppointmentSchedulingAssistantCrew().crew().train(
            n_iterations=int(sys.argv[2]), 
            filename=sys.argv[3], 
            inputs=inputs
        )
    except Exception as e:
        print(f"Training Error: {e}")
        sys.exit(1)

# Entry point logic for both local 'uv run' and Cloud 'crewai run'
if __name__ == "__main__":
    # If no arguments are passed, default to 'run'
    command = sys.argv[1] if len(sys.argv) > 1 else "run"
    
    if command == "run":
        run()
    elif command == "train":
        train()
    else:
        # Fallback to run for standard cloud triggers
        run()