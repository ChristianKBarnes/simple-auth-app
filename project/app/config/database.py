import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ.get('DB_HOST')
db_database = os.environ.get('DB_DATABASE')
db_user = os.environ.get('DB_USER')
db_port = os.environ.get('DB_PORT')
db_password = os.environ.get('DB_PASSWORD')

db_url = "postgresql://{user}:{password}@{host}:{port}/{database}".format(user=db_user, password=db_password, host=db_host, port=db_port, database=db_database)

db_test_url = "postgresql://{user}:{password}@{host}:{port}/{database}".format(user=db_user, password=db_password, host=db_host, port=db_port, database=db_database)
