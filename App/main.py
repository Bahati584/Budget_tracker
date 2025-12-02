from fastapi import FastAPI
from App.routers import users, categories, transactions
from App.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budget Tracker API", version="1.0.0")

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(transactions.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Budget Tracker API!", "version": "1.0.0"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}