import httpx
from agents import function_tool
import chainlit as cl
from typing import Optional
import json

BACKEND_URL = "http://127.0.0.1:8001"

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

@function_tool
async def get_expense_report(category: Optional[str] = None,
                                start_date: Optional[str] = None,
                                    end_date: Optional[str] = None,
                                      ):
    """
    Retrieves an expense report based on specified criteria.
    Args:
        category (str, optional): Filter by expense category.
        start_date (str, optional): Start date for the report in YYYY-MM-DD format.
        end_date (str, optional): End date for the report in YYYY-MM-DD format.
    """
    try:
        params = {"category": category}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
    
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/report",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            report_data = response.json()
            await cl.Message(content="Report extracted successfully! ✅").send()
            json_data = json.dumps(report_data) 
            print(json_data)
            return json_data
    except Exception as e:
        # Handle or log the error appropriately
        print(f"Error fetching expense report: {e}")
        raise