from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests
import os

class OutlookCalendarRequest(BaseModel):
    """Input schema for Outlook Calendar Tool."""
    subject: str = Field(..., description="The title of the meeting")
    start_time: str = Field(..., description="ISO format start time (e.g. '2024-05-01T15:00:00')")
    end_time: str = Field(..., description="ISO format end time")
    attendee_email: str = Field(..., description="The email of the person requested the appointment")

class OutlookCalendarTool(BaseTool):
    name: str = "outlook_calendar_manager"
    description: str = "Creates events in the Outlook/Microsoft 365 Calendar."
    args_schema: Type[BaseModel] = OutlookCalendarRequest

    def _run(self, subject: str, start_time: str, end_time: str, attendee_email: str) -> str:
        token = os.getenv('OUTLOOK_ACCESS_TOKEN')
        if not token:
            return "Error: OUTLOOK_ACCESS_TOKEN not set."

        url = "https://graph.microsoft.com/v1.0/me/events"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        event = {
            "subject": subject,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
            "attendees": [{"emailAddress": {"address": attendee_email}}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=event, timeout=10)
            if response.status_code == 201:
                return "Success: Appointment created in Outlook."
            return f"Error: {response.text}"
        except Exception as e:
            return f"Exception: {str(e)}"