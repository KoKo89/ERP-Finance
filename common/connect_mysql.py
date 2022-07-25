import mysql.connector
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuration import environment_exection

leadingDB  = mysql.connector.connect(
            host=environment_exection.database_host,
            port=environment_exection.database_port,
            user=environment_exection.database_username,
            passwd=environment_exection.database_password,
            database=environment_exection.database_leading
        )

financeDB  = mysql.connector.connect(
            host=environment_exection.database_host,
            port=environment_exection.database_port,
            user=environment_exection.database_username,
            passwd=environment_exection.database_password,
            database=environment_exection.database_finance
        )


userDb = mysql.connector.connect(
            host=environment_exection.database_host,
            port=environment_exection.database_port,
            user=environment_exection.database_username,
            passwd=environment_exection.database_password,
            database=environment_exection.database_user
        )