import os
import sys

# Maintain SQLite fix for agent workers
try:
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class AsistenteAgendaCrew:
    """AsistenteAgenda crew"""
    
    def __init__(self):
        self.shared_llm = LLM(
            model="gemini/gemini-1.5-flash", 
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.5
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
            verbose=True
        )