from fastapi import FastAPI, Depends
from database import SessionLocal, Base, engine 
from schemas import ExpenseCreate, ExpenseResponse

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/expenses/")
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses/", response_model=List[schemas.ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    return expenses

@app.get("/expenses/month/{year}/{month}")
def get_expenses_by_month(year: int, month: int, db: Session = Depends(get_db)):
    startdate = datetime(year, month, 1)
    if month == 12:
        enddate = datetime(year + 1, 1, 1)
    else:        enddate = datetime(year, month + 1, 1)
    expenses = db.query(models.Expense).filter(models.Expense.date >= startdate, models.Expense.date < enddate).all()
    return expenses

@app.get("/expenses/week")
def get_expenses_by_week(db: Session = Depends(get_db)):
    today = datetime.today()
    startdate = today - timedelta(days=today.weekday())
    enddate = startdate + timedelta(days=7)
    expenses = db.query(models.Expense).filter(models.Expense.date >= startdate, models.Expense.date < enddate).all()
    return expenses

@app.get("expenses/day/")
def get_expenses_by_day(db: Session = Depends(get_db)):
    today = datetime.today()
    startdate = datetime(today.year, today.month, today.day)
    enddate = startdate + timedelta(days=1)
    expenses = db.query(models.Expense).filter(models.Expense.date >= startdate, models.Expense.date < enddate).all()
    return expenses

@app.get("/expenses/category/{category}")
def get_expenses_by_category(category: str, db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).filter(models.Expense.category == category).all()
    return expenses

@app.get("totals/")
def get_total_expenses(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    total_expense = sum(expense.amount for expense in expenses)
    remaining_amount = expenses - total_expense
    return {"total": total_expense, "remaining": remaining_amount}

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)