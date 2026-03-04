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
    description: str = "Crea eventos reales en el calendario de Outlook/Microsoft 365."
    args_schema: Type[BaseModel] = OutlookCalendarRequest

    def _run(self, subject: str, start_time: str, end_time: str, attendee_email: str) -> str:
        # 1. Obtener credenciales
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        tenant_id = os.getenv('AZURE_TENANT_ID')
        user_email = os.getenv('MY_OUTLOOK_EMAIL')

        if not all([client_id, client_secret, tenant_id, user_email]):
            return "Error: Faltan credenciales (ID, Secret, Tenant o Email) en los Secrets de Streamlit."

        # 2. Generar el Token JWT real (con puntos xxxx.yyyy.zzzz)
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
            
            # Usamos un nombre de variable único para evitar conflictos de sistema
            final_jwt = token_res.json().get("access_token")
            
            if not final_jwt or "." not in final_jwt:
                return "Error: El token recibido de Microsoft no tiene el formato JWT esperado."
                
        except Exception as e:
            return f"Error obteniendo Token JWT: {str(e)}"

        # 3. Llamada a Microsoft Graph usando el token recién generado
        url = f"https://graph.microsoft.com/v1.0/users/{user_email}/events"
        headers = {
            "Authorization": f"Bearer {final_jwt}", # <--- Usamos la variable específica
            "Content-Type": "application/json"
        }
        
        event = {
            "subject": subject,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
            "attendees": [
                {
                    "emailAddress": {"address": attendee_email},
                    "type": "required"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=event, timeout=10)
            if response.status_code == 201:
                return f"✅ Éxito: Cita agendada para {user_email}."
            
            # Si falla aquí con 401, sabremos que el token fue rechazado por contenido, no por formato
            return f"Error de Microsoft Graph: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Excepción en la API: {str(e)}"