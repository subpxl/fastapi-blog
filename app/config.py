# SECRET_KEY="supersecretkey"
# ALGORITHM="HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES=30
# DATABASE_URL="sqlite:///./test.db"

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DATABASE_URL = os.getenv("DATABASE_URL")
