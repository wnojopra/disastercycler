from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Disaster Cycler API")
app.include_router(router)
