import os
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
#from langchain_google_genai import ChatGoogleGenerativeAI

@CrewBase
class AsistenteAgendaCrew:
    """AsistenteAgenda crew"""
    
    # Absolute path setup for GitHub Linux environment
    base_path = os.path.dirname(os.path.realpath(__file__))
    agents_config = os.path.join(base_path, 'config', 'agents.yaml')
    tasks_config = os.path.join(base_path, 'config', 'tasks.yaml')


    def __init__(self):
        self.shared_llm = LLM(
            model="google/gemini-1.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.5,
            # This forces the underlying google-genai SDK to use v1
            config={
                "api_version": "v1"
            }
        )

    @agent
    def appointment_request_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["appointment_request_parser"],
            tools=[],
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            llm=self.shared_llm,
        )

    @agent
    def calendar_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["calendar_manager"],
            tools=[],
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            llm=self.shared_llm,
        )

    @agent
    def email_confirmation_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["email_confirmation_specialist"],
            tools=[],
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            llm=self.shared_llm,
        )

    @agent
    def whatsapp_reminder_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["whatsapp_reminder_specialist"],
            tools=[], 
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            llm=self.shared_llm,
        )

    @agent
    def summary_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["summary_specialist"],
            tools=[],
            inject_date=True,
            allow_delegation=False,
            max_iter=15,
            llm=self.shared_llm,
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
    def schedule_whatsapp_reminders(self) -> Task:
        return Task(config=self.tasks_config["schedule_whatsapp_reminders"])

    @task
    def complete_appointment_setup(self) -> Task:
        return Task(config=self.tasks_config["complete_appointment_setup"])

    @crew
    def crew(self) -> Crew:
        """Creates the AsistenteAgenda crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            manager_llm=self.shared_llm 
        )