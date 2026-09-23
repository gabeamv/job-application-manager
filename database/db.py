from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
connectionString = f"{os.getenv("DB_PROTO") +
                      os.getenv("DB_USER") + ":" +
                      os.getenv("DB_PASSWORD") + "@" +
                      os.getenv("DB_HOST") + ":" +
                      os.getenv("DB_PORT") + "/" +
                      os.getenv("DB_NAME")
                      }"
engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


