import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from microsoft_outlook_appointment_scheduling_assistant.tools.whatsapp_business_messenger import WhatsAppBusinessMessenger




@CrewBase
class MicrosoftOutlookAppointmentSchedulingAssistantCrew:
    """MicrosoftOutlookAppointmentSchedulingAssistant crew"""

    
    @agent
    def appointment_request_parser(self) -> Agent:
        
        return Agent(
            config=self.agents_config["appointment_request_parser"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                temperature=0.7,
                max_rpm=2,      # <--- LIMITA A 2 SOLICITUDES POR MINUTO
                max_iter=3      # <--- EVITA QUE EL AGENTE SE BUCLEE Y GASTE TU CUOTA
            ),
            
        )
    
    @agent
    def calendar_manager(self) -> Agent:
        
        return Agent(
            config=self.agents_config["calendar_manager"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            apps=[
                    "microsoft_outlook/get_calendar_events",
                    
                    "microsoft_outlook/create_calendar_event",
                    ],
            
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                temperature=0.7,
                max_rpm=2,      # <--- LIMITA A 2 SOLICITUDES POR MINUTO
                max_iter=3      # <--- EVITA QUE EL AGENTE SE BUCLEE Y GASTE TU CUOTA
            ),
            
        )
    
    @agent
    def email_confirmation_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["email_confirmation_specialist"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            apps=[
                    "microsoft_outlook/send_email",
                    ],
            
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                temperature=0.7,
                max_rpm=2,      # <--- LIMITA A 2 SOLICITUDES POR MINUTO
                max_iter=3      # <--- EVITA QUE EL AGENTE SE BUCLEE Y GASTE TU CUOTA
            ),
            
        )
    
    @agent
    def whatsapp_reminder_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["whatsapp_reminder_specialist"],
            
            
            tools=[				WhatsAppBusinessMessenger()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                temperature=0.7,
                max_rpm=2,      # <--- LIMITA A 2 SOLICITUDES POR MINUTO
                max_iter=3      # <--- EVITA QUE EL AGENTE SE BUCLEE Y GASTE TU CUOTA
            ),
            
        )
    
    @agent
    def summary_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["summary_specialist"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                temperature=0.7,
                max_rpm=2,      # <--- LIMITA A 2 SOLICITUDES POR MINUTO
                max_iter=3      # <--- EVITA QUE EL AGENTE SE BUCLEE Y GASTE TU CUOTA
            ),
            
        )
    

    
    @task
    def parse_appointment_request(self) -> Task:
        return Task(
            config=self.tasks_config["parse_appointment_request"],
            markdown=False,
            
            
        )
    
    @task
    def check_availability_and_create_calendar_event(self) -> Task:
        return Task(
            config=self.tasks_config["check_availability_and_create_calendar_event"],
            markdown=False,
            
            
        )
    
    @task
    def send_email_confirmation(self) -> Task:
        return Task(
            config=self.tasks_config["send_email_confirmation"],
            markdown=False,
            
            
        )
    
    @task
    def schedule_whatsapp_reminders(self) -> Task:
        return Task(
            config=self.tasks_config["schedule_whatsapp_reminders"],
            markdown=False,
            
            
        )
    
    @task
    def complete_appointment_setup(self) -> Task:
        return Task(
            config=self.tasks_config["complete_appointment_setup"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the MicrosoftOutlookAppointmentSchedulingAssistant crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # 1. Change the model to Gemini
            # 2. Add memory=False to prevent the OpenAI Embedder error
            llm=LLM(model="gemini/gemini-1.5-flash"), 
             memory=False 
        )
