import os
import sys
import warnings

# 1. SQLite Fix for GitHub Actions / Linux environments
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool

# --- FIXED IMPORT STRATEGY ---
# This structure handles the different pathing between local development and GitHub/AMP
try:
    # Standard import for the structure CrewAI expects
    from asistente_agenda.tools.whatsapp_business_messenger import WhatsAppBusinessMessenger
    from asistente_agenda.tools.outlook_calendar_tool import OutlookCalendarTool
    from asistente_agenda.tools.custom_tool import MyCustomTool
except ImportError:
    try:
        # Fallback for different sys.path setups
        from tools.whatsapp_business_messenger import WhatsAppBusinessMessenger
        from tools.outlook_calendar_tool import OutlookCalendarTool
        from tools.custom_tool import MyCustomTool
    except ImportError as e:
        print(f"⚠️ Tool Import Warning: {e}. Using placeholders.")
        # Placeholders must inherit from BaseTool to pass Agent validation
        class WhatsAppBusinessMessenger(BaseTool):
            name: str = "WhatsApp Placeholder"
            description: str = "Tool unavailable due to import error"
            def _run(self, **kwargs): return "WhatsApp tool not available."

        class OutlookCalendarTool(BaseTool):
            name: str = "Outlook Placeholder"
            description: str = "Tool unavailable due to import error"
            def _run(self, **kwargs): return "Outlook tool not available."

        class MyCustomTool(BaseTool):
            name: str = "Custom Placeholder"
            description: str = "Tool unavailable due to import error"
            def _run(self, **kwargs): return "Custom tool not available."

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

@CrewBase
class AsistenteAgendaCrew:
    """AsistenteAgendaCrew crew for managing appointment scheduling and notifications"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    def __init__(self):
        # 2. LLM Configuration: Using Google AI Studio (Gemini)
        # Note: Ensure GOOGLE_API_KEY is set in GitHub Secrets and CrewAI Settings
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
            # ✅ Fixed: Initializing the tool class properly
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
            # ✅ Fixed: Initializing tools safely with parentheses
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
