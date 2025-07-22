import httpx
from agents import function_tool
import chainlit as cl

@function_tool
async def record_expense(amount: float, description: str, category: str, transaction_date: str):
    """
    Records a new expense.
    Args:
        amount (float): The amount of the expense.
        description (str): A brief description of the expense.
        category (str): The category of the expense (e.g., "food", "transport", "utilities").
        date (str): The date of the expense in YYYY-MM-DD format.
    """
    BACKEND_URL = "http://127.0.0.1:8001"
    ADD_EXPENSE_ENDPOINT = f"{BACKEND_URL}/add_expense"

    try:
        json_payload = {
            "amount": amount,
            "description": description,
            "category": category,
            "transaction_date": transaction_date
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                ADD_EXPENSE_ENDPOINT,
                json=json_payload,
                timeout=10.0
            )
            if response.status_code ==200:
                await cl.Message(content="Expense recorded successfully! ✅").send()
                return "expense recorded successfully"
            else:
                return f"failed to record expense. status {response.status_code}, error: {response.text}"
    except httpx.TimeoutException:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error recording expense: {str(e)}"

