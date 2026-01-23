#!/usr/bin/env python
import sys
import os
from microsoft_outlook_appointment_scheduling_assistant.crew import MicrosoftOutlookAppointmentSchedulingAssistantCrew

def run():
    """
    Run the crew.
    """
    # The Cloud environment provides these variables automatically if 
    # you uploaded them during 'crewai deploy create'
    inputs = {
        'Nombre': 'sample_value',
        'apellido': 'sample_value',
        'apellidos': 'sample_value'
    }
    
    try:
        # Initialize and kickoff the crew
        # Note: Ensure crew.py is using LLM(model="gemini/gemini-1.5-flash")
        result = MicrosoftOutlookAppointmentSchedulingAssistantCrew().crew().kickoff(inputs=inputs)
        
        # In 2026, the platform captures the return value for the API response
        return result
        
    except Exception as e:
        # Standard error formatting for cloud logs
        print(f"Error: {str(e)}")
        sys.exit(1)

def train():
    """Train the crew."""
    inputs = {'Nombre': 'sample', 'apellido': 'sample', 'apellidos': 'sample'}
    try:
        MicrosoftOutlookAppointmentSchedulingAssistantCrew().crew().train(
            n_iterations=int(sys.argv[2]), 
            filename=sys.argv[3], 
            inputs=inputs
        )
    except Exception as e:
        print(f"Training Error: {e}")
        sys.exit(1)

# ... (replay and test functions remain as backups)

if __name__ == "__main__":
    # If no arguments are passed, default to 'run' for the cloud environment
    command = sys.argv[1] if len(sys.argv) > 1 else "run"
    
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "test":
        # Supports: main.py test 10 gemini/gemini-1.5-flash
        test()
    else:
        run() # Default fallback to run