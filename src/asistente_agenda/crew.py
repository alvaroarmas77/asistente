import os
import sys
import warnings
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Filter Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Import Tools
try:
    from asistente_agenda.tools.whatsapp_business_messenger import WhatsAppBusinessMessenger
    from asistente_agenda.tools.outlook_calendar_tool import OutlookCalendarTool
except ImportError:
    from tools.whatsapp_business_messenger import WhatsAppBusinessMessenger
    from tools.outlook_calendar_tool import OutlookCalendarTool

@CrewBase
class AsistenteAgendaCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Explicitly pull the key
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        # We use provider="google" to tell LiteLLM: "Ignore Vertex, use the AI Studio Key"
        self.shared_llm = LLM(
            model="gemini/gemini-1.5-flash",
            api_key=api_key,
            provider="google",
            temperature=0.5
        )

    @agent
    def appointment_request_parser(self) -> Agent:
        return Agent(config=self.agents_config["appointment_request_parser"], llm=self.shared_llm, verbose=True)

    @agent
    def calendar_manager(self) -> Agent:
        return Agent(config=self.agents_config["calendar_manager"], llm=self.shared_llm, tools=[OutlookCalendarTool()], verbose=True)

    @agent
    def email_confirmation_specialist(self) -> Agent:
        return Agent(config=self.agents_config["email_confirmation_specialist"], llm=self.shared_llm, verbose=True)

    @agent
    def whatsapp_reminder_specialist(self) -> Agent:
        return Agent(config=self.agents_config["whatsapp_reminder_specialist"], llm=self.shared_llm, tools=[WhatsAppBusinessMessenger()], verbose=True)

    @agent
    def summary_specialist(self) -> Agent:
        return Agent(config=self.agents_config["summary_specialist"], llm=self.shared_llm, verbose=True)

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

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )