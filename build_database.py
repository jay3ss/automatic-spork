"""Create the table(s) in the databse.

WARNING: the database WILL be DELETED and recreated if this is run.
"""
import os

from sqlalchemy import MetaData

from config import engine
from models import Base

# NOTE: Should OK because not connected to database at this point
if os.path.exists('definitions.db'):
    os.remove('definitions.db')

Base.metadata.create_all(bind=engine)
metadata = MetaData(engine, reflect=True)
