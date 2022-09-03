import os

db_host = os.environ.get('DB_HOST')
db_database = os.environ.get('DB_DATABASE')
db_user = os.environ.get('DB_USER')
db_port = os.environ.get('DB_PORT')
db_password = os.environ.get('DB_PASSWORD')

db_url = "postgresql://{user}:{password}@{host}:{port}/{database}".format(db_user, db_password, db_host, db_port, db_database)
