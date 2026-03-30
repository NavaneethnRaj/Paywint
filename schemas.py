from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    name: str

class ExpenseResponse(ExpenseCreate):
    id: int
    
    class Config:
        orm_mode = True