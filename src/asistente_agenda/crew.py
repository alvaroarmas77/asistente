import os
import sys
import warnings
from datetime import datetime  # <-- Línea sugerida
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# SQLite Fix for GitHub Environments
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

# Import Tools
try:
    from asistente_agenda.tools.outlook_calendar_tool import OutlookCalendarTool
except ImportError:
    try:
        from tools.outlook_calendar_tool import OutlookCalendarTool
    except ImportError:
        from crewai.tools import BaseTool
        class OutlookCalendarTool(BaseTool):
            name: str = "outlook_calendar_manager"
            description: str = "Tool unavailable"
            def _run(self, **kwargs): return "Outlook tool not available."

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

@CrewBase
class AsistenteAgendaCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # --- LÍNEA SUGERIDA: Obtener fecha real ---
        # Esto asegura que el agente sepa que hoy es marzo de 2026
        self.fecha_actual = datetime.now().strftime('%A, %d de %B de %Y')
        
        self.shared_llm = LLM(
            model=os.getenv("MODEL", "gemini/gemini-3.1-pro-preview"), # Sugerencia: Flash es más rápido para agendar
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1, # Bajamos temperatura para mayor precisión en fechas
            max_rpm=10,
            config={
                "thinking_level": "medium" 
            }
        )

    @agent
    def appointment_request_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["appointment_request_parser"],
            llm=self.shared_llm,
            # Inyectamos la fecha en el contexto del agente
            description=f"Hoy es {self.fecha_actual}. Asegúrate de procesar las fechas para el año 2026.",
            verbose=True
        )

    @agent
    def calendar_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["calendar_manager"],
            llm=self.shared_llm,
            tools=[OutlookCalendarTool()],
            # Inyectamos la fecha aquí también para que el manager no alucine
            description=f"Hoy es {self.fecha_actual}. Usa siempre el año 2026 al agendar.",
            verbose=True
        )

    @agent
    def email_confirmation_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["email_confirmation_specialist"],
            llm=self.shared_llm,
            verbose=True
        )

    @agent
    def summary_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["summary_specialist"],
            llm=self.shared_llm,
            verbose=True
        )

    @task
    def parse_appointment_request(self) -> Task:
        # Añadimos la fecha a la tarea para reforzar el contexto
        task_config = self.tasks_config["parse_appointment_request"]
        task_config['description'] = f"(Hoy es {self.fecha_actual}) " + task_config['description']
        return Task(config=task_config)

    @task
    def check_availability_and_create_calendar_event(self) -> Task:
        return Task(config=self.tasks_config["check_availability_and_create_calendar_event"])

    @task
    def send_email_confirmation(self) -> Task:
        return Task(config=self.tasks_config["send_email_confirmation"])

    @task
    def complete_appointment_setup(self) -> Task:
        return Task(config=self.tasks_config["complete_appointment_setup"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )