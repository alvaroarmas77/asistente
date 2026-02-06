#!/usr/bin/env python
import sys
import os
import warnings

# SQLite Fix for environments like GitHub Actions
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def run():
    # Setup pathing
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Import the crew
    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
    except ImportError:
        from crew import AsistenteAgendaCrew

    # Validate API Key presence before starting
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        sys.exit(1)

    inputs = {
        'appointment_request': 'Quiero una cita para mañana a las 3pm para una revisión técnica con Juan Perez (+51999888777).',
        'Nombre': 'Juan',
        'apellido': 'Perez'
    }
    
    try:
        print(f"🚀 Initializing Crew with Key (last 4): ...{api_key[-4:]}")
        crew_instance = AsistenteAgendaCrew()
        
        # We ensure kickoff doesn't receive extra params that override crew.py
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        print("\n✅ Crew Execution Complete!")
        print(result)
    except Exception as e:
        # Improved error parsing for LiteLLM specific issues
        print(f"\n❌ Execution Error: {str(e)}")
        if "404" in str(e):
            print("💡 Suggestion: The model name or provider prefix is likely incorrect.")
        sys.exit(1)

if __name__ == "__main__":
    run()