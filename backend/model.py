# from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import validator

# Expense model
class Expenses(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: float = Field(gt=0)  # Must be positive
    description: str = Field(min_length=1)  # Non-empty
    category: str = Field(min_length=1)  # Non-empty
    created_at : datetime = datetime.utcnow()
    transaction_date : datetime

    @validator("transaction_date", pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d %B %Y")
            except ValueError as e:
                raise ValueError("Date must be in 'DD Month YYYY' format") from e
        return v



class Warehouse(SQLModel, table=True):
    warehouse_id: Optional[int] = Field(default=None, primary_key=True)
    warehouse_name: str = Field(index=True, unique=False,  description="Name of the warehouse")
    location: str = Field(description="Location of the warehouse")
