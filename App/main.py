from fastapi import FastAPI
from App.routers import users, categories, transactions
from App.database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budget Tracker API")

# Include routers
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(transactions.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Budget Tracker API!"}
