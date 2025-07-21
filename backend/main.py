from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from db.database import create_db_and_tables
from model import Expenses
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI)->AsyncGenerator[None, None]:
    print("Starting Application")
    create_db_and_tables()
    print("Expense Categorizer Application Started")
    yield

app : FastAPI = FastAPI(lifespan=lifespan, title="Expense Categorizer",
                        version="0.0.0",
                        servers=[
                            {
                                "url":"http://127.0.0.1:8001",
                                "description": "development server"
                            }
                        ]
                        )

app.include_router(router=router)

def main():
    print("Hello from expense-categorizer!")


if __name__ == "__main__":
    main()
