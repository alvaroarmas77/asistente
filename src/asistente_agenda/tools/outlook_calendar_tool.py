from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests
import os

class OutlookCalendarRequest(BaseModel):
    """Esquema de entrada para la herramienta de calendario."""
    subject: str = Field(..., description="El título de la reunión")
    start_time: str = Field(..., description="Fecha y hora de inicio en formato ISO (e.g. '2026-03-05T15:00:00')")
    end_time: str = Field(..., description="Fecha y hora de fin en formato ISO")
    attendee_email: str = Field(..., description="Email de la persona que solicita la cita")

class OutlookCalendarTool(BaseTool):
    name: str = "outlook_calendar_manager"
    description: str = "Crea eventos reales en el calendario de Outlook/Microsoft 365 para Perú."
    args_schema: Type[BaseModel] = OutlookCalendarRequest

    def _run(self, subject: str, start_time: str, end_time: str, attendee_email: str) -> str:
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        tenant_id = os.getenv('AZURE_TENANT_ID')
        user_email = os.getenv('MY_OUTLOOK_EMAIL')

        if not all([client_id, client_secret, tenant_id, user_email]):
            return "Error: Faltan credenciales en los Secrets de Streamlit."

        # 1. Obtener Token JWT
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
            final_jwt = token_res.json().get("access_token")
        except Exception as e:
            return f"Error obteniendo Token: {str(e)}"

        # 2. Configurar el evento para PERÚ (SA Pacific Standard Time)
        url = f"https://graph.microsoft.com/v1.0/users/{user_email}/events"
        headers = {
            "Authorization": f"Bearer {final_jwt}",
            "Content-Type": "application/json",
            "Prefer": 'outlook.timezone="SA Pacific Standard Time"' # Forzamos zona horaria de Perú
        }
        
        event = {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": f"Cita agendada por Asistente IA para {attendee_email}"
            },
            "start": {
                "dateTime": start_time,
                "timeZone": "SA Pacific Standard Time" 
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "SA Pacific Standard Time"
            },
            "attendees": [
                {
                    "emailAddress": {"address": attendee_email},
                    "type": "required"
                }
            ],
            "location": {"displayName": "Reunión Virtual / Oficina"}
        }
        
        try:
            response = requests.post(url, headers=headers, json=event, timeout=10)
            if response.status_code == 201:
                data = response.json()
                web_url = data.get('webLink', 'No disponible')
                return f"✅ Éxito: Cita agendada en el calendario de {user_email} (Hora Perú). Link: {web_url}"
            
            return f"Error de Microsoft Graph: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Excepción en la API: {str(e)}"