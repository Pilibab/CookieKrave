# backend/app/main.py

from fastapi import FastAPI
from api.endpoints.customer import router as customer_router

app = FastAPI(
    title="CookieKrave API",
    version="1.0.0"
)

# Register your router here
app.include_router(customer_router)

@app.get("/")
def root():
    return {"message": "Welcome to CookieKrave Backend API!"}