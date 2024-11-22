from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
import json  # To handle messages as JSON
from typing import Optional  # Import Optional

class ConversationService:
    def __init__(self):
        self.resource = ServiceFactory.get_service('ConversationResource')

    def create_conversation(self, conversation_data: dict) -> int:
        """Create a new conversation and return its ID."""
        try:
            formatted_conversation_data = {
                "name": conversation_data["name"],
                "participants": json.dumps(conversation_data["participants"]),  # Convert list to JSON string
                "messages": json.dumps(conversation_data["messages"]),  # Convert list of messages to JSON string
                "isGroup": bool(conversation_data["isGroup"])
            }

            # Assuming `self.resource.create_conversation` returns the ID of the created conversation
            conversation_id = self.resource.create_conversation(formatted_conversation_data)

            if not conversation_id:
                raise Exception("Failed to retrieve conversation ID after creation.")

            return conversation_id

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

    def get_all_conversations(self):
        """Retrieve a conversation from the database."""
        conversations = self.resource.get_all_conversations()
        if not conversations:
            raise HTTPException(status_code=404, detail=f"Conversations not found")
        return conversations

    def delete_conversation(self, conversation_id: int):
        """Delete a conversation from the database."""
        try:
            self.resource.delete_conversation(conversation_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error deleting conversation: {str(e)}")

    def get_total_conversation_count(self) -> int:
        """Get the total count of conversations."""
        try:
            total_count = self.resource.get_total_conversation_count()
            return total_count
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving total conversation count: {str(e)}")

    def get_paginated_conversations(self, page: int, limit: int):
        """Get a paginated list of conversations."""
        try:
            conversations = self.resource.get_paginated_conversations(page, limit)
            return conversations
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving paginated conversations: {str(e)}")