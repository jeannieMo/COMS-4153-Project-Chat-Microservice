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

    def get_paginated_conversations(self, page: int, limit: int) -> List[dict]:
        """Retrieve a paginated list of conversations from the database."""
        try:
            offset = (page - 1) * limit
            conversations = self.data_service.fetch_paginated(
                database_name="p1_database",
                table="conversations",
                offset=offset,
                limit=limit
            )
            return conversations
        except Exception as e:
            raise Exception(f"{str(e)}")

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
        
    def get_total_conversation_count(self) -> int:
        """Retrieve the total count of conversations from the database."""
        try:
            count = self.data_service.count_all(
                database_name="p1_database",
                table="conversations"
            )
            return count
        except Exception as e:
            raise Exception(f"Error retrieving total conversation count: {str(e)}")