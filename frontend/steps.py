import chainlit as cl
import httpx


@cl.step(type= "tool")
async def process_expense(expense_data: dict):
    BACKEND_URL = "http://127.0.0.1:8001"
    ADD_EXPENSE_ENDPOINT = f"{BACKEND_URL}/add_expense"

    """Record an expense by sending to the backend API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                ADD_EXPENSE_ENDPOINT,
                json=expense_data,
                timeout=10.0
            )
            if response.status_code ==200:
                return "expense recorded successfully"
            else:
                return f"failed to record expense. status {response.status_code}, error: {response.text}"
    except httpx.TimeoutException:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error recording expense: {str(e)}"
