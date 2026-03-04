#!/usr/bin/env python
import sys
import os
import warnings
import signal

# --- WINDOWS COMPATIBILITY PATCH ---
if sys.platform == "win32":
    missing_signals = ['SIGHUP', 'SIGTSTP', 'SIGQUIT', 'SIGCONT']
    for sig in missing_signals:
        if not hasattr(signal, sig):
            setattr(signal, sig, 1)
# -----------------------------------

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
    
    try:
        from asistente_agenda.crew import AsistenteAgendaCrew
    except ImportError:
        from crew import AsistenteAgendaCrew

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY no encontrado.")
        sys.exit(1)

    inputs = {
        'appointment_request': 'Quiero una cita para mañana a las 3pm para una revisión técnica con Juan Perez (+51999888777).',
        'Nombre': 'Juan',
        'apellido': 'Perez'
    }

    try:
        print(f"🚀 Iniciando Crew...")
        crew_instance = AsistenteAgendaCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)
        print("\n✅ Ejecución Completa!")
        print(result)
    except Exception as e:
        print(f"\n❌ Error de Ejecución: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()