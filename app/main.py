from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# Incluindo as rotas
app.include_router(router, prefix="/api/v1", tags=["Appointments"])

@app.get("/")
def root():
    return {"message": "Appointment Service is Running!"}
