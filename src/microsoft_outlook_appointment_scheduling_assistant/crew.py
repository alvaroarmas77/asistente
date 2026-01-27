import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from microsoft_outlook_appointment_scheduling_assistant.tools.whatsapp_business_messenger import WhatsAppBusinessMessenger

@CrewBase
class MicrosoftOutlookAppointmentSchedulingAssistantCrew:
    """MicrosoftOutlookAppointmentSchedulingAssistant crew"""

    # We define the LLM once to keep the code DRY and avoid multiple initializations
    def __init__(self):
        self.shared_llm = LLM(
            model="google/gemini-1.5-flash",
            temperature=0.7,
            max_rpm=2,
            # Note: max_iter is usually an Agent parameter, not an LLM parameter.
            # I have moved it to the Agent definitions below.
        )

    @agent
    def appointment_request_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["appointment_request_parser"],
            tools=[],
            allow_delegation=False,
            max_iter=3,
            llm=self.shared_llm,
            verbose=True
        )

    @agent
    def calendar_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["calendar_manager"],
            # Apps are used in CrewAI Enterprise/Cloud; 
            # for local/open-source, ensure these are supported tools.
            tools=[], 
            allow_delegation=False,
            max_iter=3,
            llm=self.shared_llm,
            verbose=True
        )

    @agent
    def email_confirmation_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["email_confirmation_specialist"],
            tools=[],
            allow_delegation=False,
            max_iter=3,
            llm=self.shared_llm,
            verbose=True
        )

    @agent
    def whatsapp_reminder_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["whatsapp_reminder_specialist"],
            tools=[WhatsAppBusinessMessenger()],
            allow_delegation=False,
            max_iter=3,
            llm=self.shared_llm,
            verbose=True
        )

    @agent
    def summary_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["summary_specialist"],
            tools=[],
            allow_delegation=False,
            max_iter=3,
            llm=self.shared_llm,
            verbose=True
        )

    @task
    def parse_appointment_request(self) -> Task:
        return Task(
            config=self.tasks_config["parse_appointment_request"],
        )

    @task
    def check_availability_and_create_calendar_event(self) -> Task:
        return Task(
            config=self.tasks_config["check_availability_and_create_calendar_event"],
        )

    @task
    def send_email_confirmation(self) -> Task:
        return Task(
            config=self.tasks_config["send_email_confirmation"],
        )

    @task
    def schedule_whatsapp_reminders(self) -> Task:
        return Task(
            config=self.tasks_config["schedule_whatsapp_reminders"],
        )

    @task
    def complete_appointment_setup(self) -> Task:
        return Task(
            config=self.tasks_config["complete_appointment_setup"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MicrosoftOutlookAppointmentSchedulingAssistant crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False # Prevents the OpenAI embedding error if you don't have an API key set
        )