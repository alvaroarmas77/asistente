from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, Optional
import requests
import json
import os

class WhatsAppMessageRequest(BaseModel):
    """Input schema for WhatsApp Business Messenger Tool."""
    phone_number: str = Field(
        ..., 
        description="The recipient's phone number in international format (e.g., '+1234567890')"
    )
    message: str = Field(
        ..., 
        description="The message content to send"
    )
    message_type: str = Field(
        default="text", 
        description="Type of message to send (default: 'text')"
    )

class WhatsAppBusinessMessenger(BaseTool):
    """Tool for sending WhatsApp messages using WhatsApp Business API for appointment confirmations and reminders."""

    name: str = "WhatsApp Business Messenger"
    description: str = (
        "Send WhatsApp messages using WhatsApp Business API for appointment confirmations and reminders. "
        "Requires WHATSAPP_ACCESS_TKN and WHATSAPP_PHONE_NUMBER_ID environment variables to be set."
    )
    args_schema: Type[BaseModel] = WhatsAppMessageRequest

    def _format_phone_number(self, phone_number: str) -> str:
        """
        Format phone number to ensure it's in the correct format for WhatsApp API.
        Remove any non-numeric characters except the leading '+' and ensure it starts with country code.
        """
        # Remove all non-numeric characters except '+'
        formatted = ''.join(char for char in phone_number if char.isdigit() or char == '+')
        
        # If it doesn't start with '+', assume it needs one
        if not formatted.startswith('+'):
            formatted = '+' + formatted
            
        return formatted

    def _run(self, phone_number: str, message: str, message_type: str = "text") -> str:
        """
        Send a WhatsApp message using the WhatsApp Business API.
        
        Args:
            phone_number: The recipient's phone number in international format
            message: The message content to send
            message_type: Type of message to send (default: "text")
            
        Returns:
            JSON string with success status and message details
        """
        try:
            # Get required environment variables
            access_token = os.getenv('WHATSAPP_ACCESS_TKN')
            phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
            
            # Validate environment variables
            if not access_token:
                return json.dumps({
                    "success": False,
                    "error": "WHATSAPP_ACCESS_TKN environment variable is not set",
                    "details": "Please set the WHATSAPP_ACCESS_TKN environment variable with your WhatsApp Business API access token"
                })
                
            if not phone_number_id:
                return json.dumps({
                    "success": False,
                    "error": "WHATSAPP_PHONE_NUMBER_ID environment variable is not set",
                    "details": "Please set the WHATSAPP_PHONE_NUMBER_ID environment variable with your WhatsApp Business phone number ID"
                })
            
            # Format phone number
            formatted_phone = self._format_phone_number(phone_number)
            
            # Prepare API endpoint
            url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare request payload
            payload = {
                "messaging_product": "whatsapp",
                "to": formatted_phone,
                "type": message_type,
                "text": {
                    "body": message
                }
            }
            
            # Make API request
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            # Handle response
            if response.status_code == 200:
                response_data = response.json()
                return json.dumps({
                    "success": True,
                    "message": "WhatsApp message sent successfully",
                    "phone_number": formatted_phone,
                    "message_content": message,
                    "message_type": message_type,
                    "whatsapp_message_id": response_data.get("messages", [{}])[0].get("id", "N/A"),
                    "response": response_data
                })
            else:
                # Handle API errors
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", {}).get("message", "Unknown error")
                    error_code = error_data.get("error", {}).get("code", "Unknown")
                except:
                    error_message = response.text
                    error_code = response.status_code
                
                return json.dumps({
                    "success": False,
                    "error": f"WhatsApp API error (Code: {error_code})",
                    "details": error_message,
                    "status_code": response.status_code,
                    "phone_number": formatted_phone
                })
                
        except requests.exceptions.Timeout:
            return json.dumps({
                "success": False,
                "error": "Request timeout",
                "details": "The request to WhatsApp API timed out. Please try again."
            })
            
        except requests.exceptions.ConnectionError:
            return json.dumps({
                "success": False,
                "error": "Connection error",
                "details": "Unable to connect to WhatsApp API. Please check your internet connection."
            })
            
        except requests.exceptions.RequestException as e:
            return json.dumps({
                "success": False,
                "error": "Request failed",
                "details": f"HTTP request failed: {str(e)}"
            })
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": "Unexpected error",
                "details": f"An unexpected error occurred: {str(e)}"
            })