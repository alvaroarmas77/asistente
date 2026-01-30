import os
import sys
import warnings

# 1. SQLite Fix for GitHub Actions environment
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# --- FINAL IMPORT STRATEGY ---
# We use direct imports because main.py will now inject the correct folder into sys.path
try:
    from tools.whatspp_business_messenger import WhatsAppBusinessMessenger
    from tools.outlook_calendar_tool import OutlookCalendarTool
    from tools.custom_tool import MyCustomTool
except ImportError:
    # This acts as a backup for local development environments
    try:
        from asistente_agenda.tools.whatspp_business_messenger import WhatsAppBusinessMessenger
        from asistente_agenda.tools.outlook_calendar_tool import OutlookCalendarTool
        from asistente_agenda.tools.custom_tool import MyCustomTool
    except ImportError as e:
        print(f"❌ Tool Import Error: {e}")
        # Placeholder classes to prevent 'NoneType' errors during Agent initialization
        class WhatsAppBusinessMessenger: pass
        class OutlookCalendarTool: pass
        class MyCustomTool: pass

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

@CrewBase
class AsistenteAgendaCrew:
    """AsistenteAgendaCrew crew for managing appointment scheduling and notifications"""

    def __init__(self):
        # 2. LLM Configuration: Forcing Google AI Studio to avoid Vertex 404s
        self.shared_llm = LLM(
            model="gemini/gemini-1.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            provider="google",
            temperature=0.5
        )

    # --- Agents Section ---

    @agent
    def appointment_request_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["appointment_request_parser"],
            llm=self.shared_llm,
            allow_delegation=False,
            verbose=True
        )

    @agent
    def calendar_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["calendar_manager"],
            llm=self.shared_llm,
            tools=[OutlookCalendarTool()],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def email_confirmation_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["email_confirmation_specialist"],
            llm=self.shared_llm,
            allow_delegation=False,
            verbose=True
        )

    @agent
    def whatsapp_reminder_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["whatsapp_reminder_specialist"],
            llm=self.shared_llm,
            # Initializing tools safely
            tools=[WhatsAppBusinessMessenger(), MyCustomTool()],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def summary_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["summary_specialist"],
            llm=self.shared_llm,
            allow_delegation=False,
            verbose=True
        )

    # --- Tasks Section ---

    @task
    def parse_appointment_request(self) -> Task:
        return Task(config=self.tasks_config["parse_appointment_request"])

    @task
    def check_availability_and_create_calendar_event(self) -> Task:
        return Task(config=self.tasks_config["check_availability_and_create_calendar_event"])

    @task
    def send_email_confirmation(self) -> Task:
        return Task(config=self.tasks_config["send_email_confirmation"])

    @task
    def schedule_whatsapp_reminders(self) -> Task:
        return Task(config=self.tasks_config["schedule_whatsapp_reminders"])

    @task
    def complete_appointment_setup(self) -> Task:
        return Task(config=self.tasks_config["complete_appointment_setup"])

    # --- Crew Orchestration ---

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )