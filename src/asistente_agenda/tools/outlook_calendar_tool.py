from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests
import os

class OutlookCalendarRequest(BaseModel):
    subject: str = Field(..., description="El título de la reunión")
    start_time: str = Field(..., description="Fecha y hora de inicio ISO (e.g. '2026-03-05T15:00:00')")
    end_time: str = Field(..., description="Fecha y hora de fin ISO")
    attendee_email: str = Field(..., description="Email de la persona que solicita la cita")

class OutlookCalendarTool(BaseTool):
    name: str = "outlook_calendar_manager"
    description: str = "Crea eventos en el calendario de Outlook Business y envía invitaciones."
    args_schema: Type[BaseModel] = OutlookCalendarRequest

    def _run(self, subject: str, start_time: str, end_time: str, attendee_email: str) -> str:
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        # ¡CAMBIO CRÍTICO!: Para Business, NO uses 'consumers', usa el ID largo de tus Secrets
        tenant_id = os.getenv('AZURE_TENANT_ID') 
        user_email = "soportesap@frontera-virtual.com"

        # 1. Obtener Token
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default" 
        }

        try:
            token_res = requests.post(token_url, data=token_data, timeout=10)
            final_jwt = token_res.json().get("access_token")
        except Exception as e:
            return f"Error de Token: {str(e)}"

        # 2. URL FORZADA AL CALENDARIO VISUAL (Paso 3 crítico)
        # Cambiamos /events por /calendar/events para que aparezca en tu Outlook
        url = f"https://graph.microsoft.com/v1.0/users/{user_email}/calendar/events"
        
        headers = {
            "Authorization": f"Bearer {final_jwt}",
            "Content-Type": "application/json",
            "Prefer": 'outlook.timezone="SA Pacific Standard Time"'
        }
        
        event = {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": f"Cita agendada por Asistente IA. <br>Invitado: {attendee_email}"
            },
            "start": {"dateTime": start_time, "timeZone": "SA Pacific Standard Time"},
            "end": {"dateTime": end_time, "timeZone": "SA Pacific Standard Time"},
            "attendees": [
                {
                    "emailAddress": {"address": attendee_email},
                    "type": "required"
                }
            ],
            # ESTO FUERZA EL ENVÍO DEL CORREO DE INVITACIÓN
            "allowNewTimeProposals": True,
            "isOnlineMeeting": True,
            "onlineMeetingProvider": "teamsForBusiness"
        }
        
        try:
            # Crear evento e invitar automáticamente
            response = requests.post(url, headers=headers, json=event, timeout=10)
            
            if response.status_code == 201:
                web_url = response.json().get('webLink', 'No disponible')
                # Si el evento se creó, el correo de invitación se envía automáticamente 
                # porque incluimos a alguien en la lista de 'attendees'.
                return f"✅ ÉXITO: Cita en calendario y correo enviado a {attendee_email}. Link: {web_url}"
            
            return f"Error Graph: {response.status_code} - {response.text}"
            
        except Exception as e:
            return f"Excepción: {str(e)}"