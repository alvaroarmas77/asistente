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
        # 1. Get Azure Credentials from environment
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        tenant_id = os.getenv('AZURE_TENANT_ID')
        user_email = os.getenv('MY_OUTLOOK_EMAIL') # Add this to your Streamlit Secrets!

        if not all([client_id, client_secret, tenant_id]):
            return "Error: Missing Azure credentials (ID, Secret, or Tenant) in environment."
        
        if not user_email:
            return "Error: MY_OUTLOOK_EMAIL not set. Background apps need a target email to find the calendar."

        # 2. Exchange Credentials for a real JWT Access Token
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default"
        }
        
        try:
            token_res = requests.post(token_url, data=token_data, timeout=10)
            token_res.raise_for_status()
            token = token_res.json().get("access_token")
        except Exception as e:
            return f"Error obtaining Access Token: {str(e)}"

        # 3. Build the Microsoft Graph API event object
        # Note: We use /users/{email}/ instead of /me/ for application-level access
        url = f"https://graph.microsoft.com/v1.0/users/{user_email}/events"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        event = {
            "subject": subject,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
            "attendees": [
                {
                    "emailAddress": {
                        "address": attendee_email
                    },
                    "type": "required"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=event, timeout=10)
            if response.status_code == 201:
                return f"Success: Appointment created in Outlook calendar of {user_email}."
            return f"Error from Microsoft Graph: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception occurred while calling Outlook API: {str(e)}"