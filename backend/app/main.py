# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.admin import router as admin_router
from app.api.endpoints.bom import router as bom_router
from app.api.endpoints.cart import router as cart_router
from app.api.endpoints.customer import router as customer_router
from app.api.endpoints.fullfillment import router as fullfillment_router
from app.api.endpoints.inventory import router as inventory_router
from app.api.endpoints.orders import router as orders_router
from app.api.endpoints.products import router as product_router
from app.api.endpoints.riders import router as riders_router
from app.api.auth import router as auth_router

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
app.include_router(customer_router, prefix="/api")
app.include_router(product_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(bom_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(fullfillment_router[0], prefix="/api")
app.include_router(fullfillment_router[1], prefix="/api")
app.include_router(fullfillment_router[2], prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(riders_router, prefix="/api")
app.include_router(auth_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to CookieKrave Backend API!"}