from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_USER = "root"
MYSQL_PASSWORD = "''"
MYSQL_HOST = "localhost"
MYSQL_DB = "Budget_tracker"

DATABASE_URL = f"mysql+pymysql://root@localhost/Budget_tracker"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
