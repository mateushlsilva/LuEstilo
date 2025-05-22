from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from app.config import settings
from app.database import Database
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

db = Database()

@app.get('/')
def home(db: Session = Depends(db.get_db)):
    return {"message": 'Home', 'status': 200}

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0