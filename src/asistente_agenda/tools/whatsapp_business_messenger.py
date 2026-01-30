from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests
import json
import os

class WhatsAppMessageRequest(BaseModel):
    """Input schema for WhatsApp Business Messenger Tool."""
    phone_number: str = Field(..., description="Recipient's phone number with country code (e.g. '51999888777')")
    message: str = Field(..., description="The message content to send")

class WhatsAppBusinessMessenger(BaseTool):
    name: str = "whatsapp_business_messenger"
    description: str = "Sends WhatsApp messages for appointment confirmations and reminders via Business API."
    args_schema: Type[BaseModel] = WhatsAppMessageRequest

    def _run(self, phone_number: str, message: str) -> str:
        access_token = os.getenv('WHATSAPP_ACCESS_TKN')
        phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        
        if not access_token or not phone_number_id:
            return "Error: Missing WhatsApp environment variables."

        # WhatsApp API usually wants numbers without the '+' prefix
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_phone,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                return f"Success: Message sent to {clean_phone}"
            return f"Error: {response.text}"
        except Exception as e:
            return f"Exception: {str(e)}"