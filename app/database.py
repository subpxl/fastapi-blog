from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL


engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
sessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()

def get_db() -> Generator[Any, Any, None] :
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()