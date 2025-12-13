from fastapi import FastAPI
from app.core.config import Config
from fastapi.middleware.cors import CORSMiddleware
from app.api import events
from app.api import signals
app = FastAPI(title=Config.app_name)
app.add_middleware(CORSMiddleware,
                    allow_origins=Config.cors_origins,
                    allow_credentials=True,
                    allow_methods="*",
                    allow_headers="*")

app.include_router(events.router,prefix="/api")
app.include_router(signals.router,prefix="/api")
@app.get('/')
def health():
    return "Server is up"




