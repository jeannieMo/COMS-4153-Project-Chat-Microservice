import pymysql
from .BaseDataService import DataDataService

class MySQLRDBDataService(DataDataService):
    """
    A generic data service for MySQL databases. The class implement common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        connection = pymysql.connect(
            host=self.context["host"],
            port=self.context["port"],
            user=self.context["user"],
            passwd=self.context["password"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection

    def get_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        key_value: str):
        """
        See base class for comments.
        """

        connection = None
        result = None

        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} " + \
                        f"where {key_field}=%s"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            result = cursor.fetchone()
        except Exception as e:
            if connection:
                connection.close()

        return result

    def fetch_one(self, database_name: str, table: str, key_field: str, key_value: str):
        """Fetch a single record from the specified table."""
        connection = self._get_connection()
        try:
            sql = f"SELECT * FROM {database_name}.{table} WHERE {key_field} = %s"
            with connection.cursor() as cursor:
                cursor.execute(sql, (key_value,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            raise Exception (f"{str(e)}")
        finally:
            connection.close()

    def insert(self, database_name: str, table: str, data: dict):
        """Insert a new record into the database."""
        connection = self._get_connection()
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))

            sql = f"""
                INSERT INTO {database_name}.{table} ({columns}) VALUES ({placeholders});
            """
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(data.values()))
                inserted_id = cursor.lastrowid
                return inserted_id
        except Exception as e:
            raise Exception (f"{str(e)}")
        finally:
            connection.close()

    def fetch_all(self, database_name: str, table: str):
        connection = self._get_connection()
        try:
            sql = f"SELECT * FROM {database_name}.{table}"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            raise Exception(f"{str(e)}")
        finally:
            connection.close()

    def fetch_paginated(self, database_name: str, table: str, offset: int, limit: int):
        """Fetch a paginated list of records from the specified table."""
        connection = self._get_connection()
        try:
            sql = f"SELECT * FROM {database_name}.{table} LIMIT %s OFFSET %s"
            with connection.cursor() as cursor:
                cursor.execute(sql, (limit, offset))
                result = cursor.fetchall()
                return result
        except Exception as e:
            raise Exception(f"Error fetching paginated data: {str(e)}")
        finally:
            connection.close()

    def update(self, database_name: str, table: str, data: dict, key_field: str, key_value: str):
        """Update an existing record in the database based on a key field."""
        connection = self._get_connection()
        try:
            existing_record = self.fetch_one(database_name, table, key_field, key_value)
            if not existing_record:
                print("No")
                raise Exception(f"No record found with {key_field} = {key_value}")
        
            updates = ", ".join([f"{key} = %s" for key in data.keys()])

            sql = f"""
                UPDATE {database_name}.{table}
                SET {updates}
                WHERE {key_field} = %s;
            """
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(data.values()) + (key_value,))

        except Exception as e:
            raise Exception(f"{str(e)}")
        finally:
            connection.close()

    def delete(self, database_name: str, table: str, key_field: str, key_value: str):
        """Delete a record from the specified table based on a key field."""
        connection = self._get_connection()
        try:
            # Check if the record exists before attempting to delete
            existing_record = self.fetch_one(database_name, table, key_field, key_value)
            if not existing_record:
                raise Exception(f"No record found with {key_field} = {key_value}")

            sql = f"DELETE FROM {database_name}.{table} WHERE {key_field} = {key_value};"
            with connection.cursor() as cursor:
                cursor.execute(sql)

        except Exception as e:
            raise Exception(f"{str(e)}")
        finally:
            connection.close()

    def count_all(self, database_name: str, table: str) -> int:
        """Count all records in the specified table."""
        connection = self._get_connection()
        try:
            sql = f"SELECT COUNT(*) AS total FROM {database_name}.{table}"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['total']  # Returning the total count
        except Exception as e:
            raise Exception(f"Error counting records in {table}: {str(e)}")
        finally:
            connection.close()