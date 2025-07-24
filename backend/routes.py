from fastapi import APIRouter, HTTPException
from model import Warehouse, Expenses
from sqlmodel import Session, select
from db.database import DB_SESSION 
from typing import Optional
from datetime import datetime
from schemas import ExpenseCreate, test_class
import json

router = APIRouter()

@router.get('/')
def welcome():
    response = {"message": "Expense Categorizer Application is running"}
    print("Returning:", response)  # Check terminal logs
    return response

@router.post('/warehouse')
def add_to_warehouse(warehouse_data:Warehouse,session: DB_SESSION):
    session.add(warehouse_data)
    session.commit()
    session.refresh(warehouse_data)
    return warehouse_data

@router.post('/add_expense')
def add_to_expense(expense_data:ExpenseCreate, session: DB_SESSION):
    expense_data_dict = expense_data.dict() 
    expense = Expenses(**expense_data_dict)
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense

@router.get('/report')
def get_report(session : DB_SESSION,
               category: Optional[str] = None,
                start_date: Optional[str] = None,
                end_date: Optional[str] = None,
):
    query = select(Expenses)
    if category:
        query = query.where(category==Expenses.category)
    if start_date:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.where(Expenses.transaction_date >= start_date_obj)
    if end_date:
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.where(Expenses.transaction_date <= end_date_obj)

    answer = session.exec(query).all()
    print(type(answer))
    # json_answer = json.dumps(answer.__dict__)
    # print(type(json_answer))

    return answer