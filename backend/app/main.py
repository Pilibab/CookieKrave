# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.customer import router as customer_router
from app.api.endpoints.products import router as product_router


app = FastAPI(
    title="CookieKrave API",
    version="1.0.0"
)

# Define the origins (URLs) that are allowed to talk to your backend
origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
    #TODO: add production domain (e.g., "https://cookiekrave.com"), should the app be online
]

# Add the middleware to the FastAPI app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allows requests from your frontend ports
    allow_credentials=True,       # Allows frontend to send cookies/auth headers
    allow_methods=["*"],          # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],          # Allows all HTTP headers
)

# Register your router here
app.include_router(customer_router)
app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Welcome to CookieKrave Backend API!"}