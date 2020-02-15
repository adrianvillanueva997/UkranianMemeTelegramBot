import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(verbose=True)
updater = os.getenv('UPDATER')
engine = create_engine(f"mysql+mysqldb://{os.getenv('USERNAME_DB')}:{os.getenv('PASSWORD_DB')}@{os.getenv('IP')}",
                       encoding='utf-8')
OPapi_key = os.getenv('OPapi_key')
