import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get("DATABASE_URL")

db_test_url =  os.environ.get("DATABASE_TEST_URL")
