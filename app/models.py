#models.py
from pydantic import BaseModel

class IndexCreate(BaseModel):
    name: str
    value: float

class CurrencyPairCreate(BaseModel):
    baseCurrency: str
    quoteCurrency: str
    exchangeRate: float
