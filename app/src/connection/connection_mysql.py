import logging
import mysql.connector

from app.src.config.variables import MYSQL_USER, MYSQL_PASSWORD, MYSQL_SERVER, MYSQL_DB

logger = logging.getLogger(__name__)

insert_sql = """INSERT INTO db.examples (name, animal, language, format, mode, frame, height, width, animated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""


class MySQLClient:

    def __init__(self, connection, cursor):

        self.__connection = connection
        self.__cursor = cursor

    @staticmethod
    def init_client():
        """
        Static method for establishing MySQL DB connection

        """

        with mysql.connector.connect(user=MYSQL_USER,
                                    password=MYSQL_PASSWORD,
                                    host=MYSQL_SERVER,
                                    database=MYSQL_DB) as conn:
            cursor = conn.cursor()

            yield MySQLClient(connection=conn, cursor=cursor)

    def insert_db(self, val: tuple):

        self.__cursor.execute(insert_sql, val)

    def group_and_count_db(self, field: str):

        self.__cursor.execute(f"SELECT {field}, COUNT({field}) FROM examples GROUP BY {field}")
        result = self.__cursor.fetchall()

        return result

    def commit_db(self):

        self.__connection.commit()



