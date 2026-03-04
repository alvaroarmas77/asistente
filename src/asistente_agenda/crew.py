import os
import sys
import warnings
from crewai import Agent, Crew, Process, Task, LLM  # Added LLM import
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
        # FIX: Use the native CrewAI LLM class with the 'gemini/' prefix.
        # additional comment
        # This is the "magic word" that prevents the 'Provider NOT provided' error.
        self.shared_llm = LLM(
            model=os.getenv("MODEL", "gemini/gemini-3.1-pro-preview"),
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=1.0,           # Higher temperature is better for 3.1 reasoning
            max_rpm=10,                # You can increase this if you have a paid plan
            # New Gemini 3.1 parameter for thinking depth
            config={
                "thinking_level": "medium" 
            }
        )


    @agent
    def appointment_request_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["appointment_request_parser"],
            llm=self.shared_llm,
            verbose=True
        )

    @agent
    def calendar_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["calendar_manager"],
            llm=self.shared_llm,
            tools=[OutlookCalendarTool()],
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
        return Task(config=self.tasks_config["parse_appointment_request"])

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