import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve connection information from environment variables
database_name = os.environ['DB_NAME']
username = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']


# Construct the database URL
database_url = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"