from typing import Any, List, Optional

class ConversationResource:
    def __init__(self):
        from app.services.service_factory import ServiceFactory
        self.data_service = ServiceFactory.get_service('ConversationResourceService')

    def create_conversation(self, conversation: dict) -> dict:
        """Create a new conversation."""
        try:
            inserted_id = self.data_service.insert(
                database_name="p1_database",
                table="conversations",
                data=conversation, 
            )
            return {"convo_id": inserted_id}  # Return as a dictionary for consistency
        except Exception as e:
            raise Exception(f"{str(e)}")
    
    def update_conversation(self, conversation_id: int, conversation: dict) -> dict:
        """Create a new conversation."""
        try:
            self.data_service.update(
                database_name="p1_database",
                table="conversations",
                data=conversation, 
                key_field="convo_id",
                key_value=conversation_id
            )
        except Exception as e:
            raise Exception(f"{str(e)}")

    def get_conversation(self, conversation_id: int) -> Optional[dict]:
        """Retrieve a conversation from the database."""
        return self.data_service.fetch_one(
            database_name="p1_database",
            table="conversations",
            key_field="convo_id",
            key_value=conversation_id
        )

    def get_all_conversations(self) -> List[dict]:
        """Retrieve all conversations from the database."""
        return self.data_service.fetch_all(
            database_name="p1_database",
            table="conversations"
        )

    def delete_conversation(self, conversation_id: int) -> None:
        """Delete a conversation from the database."""
        try:
            self.data_service.delete(
                database_name="p1_database",
                table="conversations",
                key_field="convo_id",
                key_value=conversation_id
            )
        except Exception as e:
            raise Exception(f"Error deleting conversation: {str(e)}")