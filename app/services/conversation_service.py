from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
import json  # To handle messages as JSON
from typing import Optional  # Import Optional

class ConversationService:
    def __init__(self):
        self.resource = ServiceFactory.get_service('ConversationResource')

    def create_conversation(self, conversation_data: dict):
        """Create a new conversation or update an existing one."""
        try:
            formatted_conversation_data = {
                "name": conversation_data["name"],
                "participants": json.dumps(conversation_data["participants"]),  # Convert list to JSON string
                "messages": json.dumps(conversation_data["messages"]),  # Convert list of messages to JSON string
                "isGroup": bool(conversation_data["isGroup"])
            }
            self.resource.create_conversation(formatted_conversation_data)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating conversation: {str(e)}")

    def update_conversation(self, conversation_id: int, conversation_data: dict):
        """Create a new conversation or update an existing one."""
        try:
            formatted_conversation_data = {
                "name": conversation_data["name"],
                "participants": json.dumps(conversation_data["participants"]),  # Convert list to JSON string
                "messages": json.dumps(conversation_data["messages"]),  # Convert list of messages to JSON string
                "isGroup": bool(conversation_data["isGroup"])
            }
            self.resource.update_conversation(conversation_id, formatted_conversation_data)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating conversation: {str(e)}")

    def get_conversation(self, conversation_id: int):
        """Retrieve a conversation from the database."""
        conversation = self.resource.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail=f"Conversation with ID {conversation_id} not found")
        return conversation

