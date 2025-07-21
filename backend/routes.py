from fastapi import APIRouter, HTTPException
from model import Warehouse, Expenses
from sqlmodel import Session, select
from db.database import DB_SESSION 

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
def add_to_expense(expense:Expenses,session: DB_SESSION):
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense
