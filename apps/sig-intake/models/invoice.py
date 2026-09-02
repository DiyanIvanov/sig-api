from pydantic import BaseModel, computed_field
from typing import List


class Product(BaseModel):
    name: str
    price: float
    quantity: int


class Invoice(BaseModel):
    invoice_id: int
    invoice_date: str
    customer: str
    products: List[Product]
