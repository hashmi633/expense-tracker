from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import validator

class ExpenseCreate(SQLModel):
    amount: float = Field(gt=0)  # Must be positive
    description: str = Field(min_length=1)  # Non-empty
    category: str = Field(min_length=1)  # Non-empty
    transaction_date : datetime

    @validator("transaction_date", pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                # Try ISO format (e.g., "2025-07-24T00:00:00")
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                try:
                    # Try "DD Month YYYY" (e.g., "24 July 2025")
                    return datetime.strptime(v, "%d %B %Y")
                except ValueError:
                    try:
                        # Try "DD-MM-YYYY" (e.g., "24-07-2025")
                        return datetime.strptime(v, "%d-%m-%Y")
                    except ValueError as e:
                        raise ValueError(
                            "Date must be in ISO format (e.g., '2025-07-24'), "
                            "'DD Month YYYY' (e.g., '24 July 2025'), "
                            "or 'DD-MM-YYYY' (e.g., '24-07-2025')"
                        ) from e
        return v
    
def test_class():
    date = "2025-07-24T10:18:24.162Z"
    transaction_date = datetime.fromisoformat(date.replace("Z", "+00:00"))
    schema_data = ExpenseCreate(
        amount=10,
        description="description",
        category="education",
        transaction_date=transaction_date
    )

    schema_data_dict = schema_data.dict()

    print(f"type of schema instance:{type(schema_data)}, type of schema_data_dict: {type(schema_data_dict)}")