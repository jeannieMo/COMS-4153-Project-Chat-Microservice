from framework.services.service_factory import BaseServiceFactory
from app.resources.conversation_resource import ConversationResource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
import os

class ServiceFactory(BaseServiceFactory):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        if service_name == 'ConversationResourceService':
            context = {
                "host": os.getenv("DB_HOST"),
                "port": int(os.getenv("DB_PORT")),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
                "database": os.getenv("DB_NAME")
            }
            return MySQLRDBDataService(context)
        elif service_name == 'ConversationResource':
            return ConversationResource()
        else:
            raise ValueError(f"Service {service_name} is not supported.")