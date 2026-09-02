from pydantic import BaseModel, computed_field
from typing import List


class Product(BaseModel):
    name: str
    price: float
    quantity: int

    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * self.quantity

class Invoice(BaseModel):
    invoice_id: int
    invoice_date: str
    customer: str
    products: List[Product]

    @computed_field
    @property
    def total_price(self) -> float:
        return sum(product.total_price for product in self.products)