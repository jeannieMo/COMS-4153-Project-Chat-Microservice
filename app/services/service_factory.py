from framework.services.service_factory import BaseServiceFactory
from app.resources.conversation_resource import ConversationResource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService


class ServiceFactory(BaseServiceFactory):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        if service_name == 'ConversationResourceService':
            context = {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "dbuserdbuser",
                "database": "p1_database"
            }
            return MySQLRDBDataService(context)
        elif service_name == 'ConversationResource':
            return ConversationResource()
        else:
            raise ValueError(f"Service {service_name} is not supported.")