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
    description: str = "Crea eventos reales en el calendario de Outlook personal para Perú."
    args_schema: Type[BaseModel] = OutlookCalendarRequest

    def _run(self, subject: str, start_time: str, end_time: str, attendee_email: str) -> str:
        # Recuperar credenciales de los Secrets
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        # Para cuentas personales, tenant_id DEBE ser 'consumers' en tus Secrets de Streamlit
        tenant_id = os.getenv('AZURE_TENANT_ID', 'consumers') 
        user_email = "alvaro.armas@outlook.com" # Hardcoded para asegurar el endpoint

        if not all([client_id, client_secret, tenant_id]):
            return "Error: Faltan credenciales AZURE_CLIENT_ID o AZURE_CLIENT_SECRET en Secrets."

        # 1. Obtener Token JWT (Flujo OAuth2 Client Credentials)
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default" 
        }

        try:
            token_res = requests.post(token_url, data=token_data, timeout=10)
            if token_res.status_code != 200:
                return f"Error de Autenticación Azure: {token_res.text}"
            
            final_jwt = token_res.json().get("access_token")
        except Exception as e:
            return f"Error obteniendo Token: {str(e)}"

        # 2. Endpoint específico para cuenta personal (users/email)
        url = f"https://graph.microsoft.com/v1.0/users/{user_email}/events"
        
        headers = {
            "Authorization": f"Bearer {final_jwt}",
            "Content-Type": "application/json",
            "Prefer": 'outlook.timezone="SA Pacific Standard Time"' # Zona horaria de Perú
        }
        
        # Estructura del Evento
        event = {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": f"Cita agendada por Asistente IA para {attendee_email}. Confirmada automáticamente."
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
            "location": {"displayName": "Microsoft Teams / Virtual"},
            # Esto intenta que Outlook envíe la invitación por correo automáticamente
            "responseRequested": True 
        }
        
        try:
            # 3. Llamada a la API de Microsoft Graph
            response = requests.post(url, headers=headers, json=event, timeout=10)
            
            if response.status_code == 201:
                data = response.json()
                web_url = data.get('webLink', 'No disponible')
                return f"✅ ¡Cita creada con éxito en tu calendario! Link: {web_url}"
            
            # Manejo específico del error 403
            if response.status_code == 403:
                return "Error 403 (Acceso Denegado): Verifica que el permiso Calendars.ReadWrite sea de tipo 'Application' y tenga el Círculo Verde en Azure."
            
            return f"Error de Microsoft Graph: {response.status_code} - {response.text}"
            
        except Exception as e:
            return f"Excepción en la API: {str(e)}"