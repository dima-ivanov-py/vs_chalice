from pydantic import BaseModel, validator


class OrderModel(BaseModel):
    username: str
    uid: str
    status: str
    product_username: str
    product_uid: str
    amount: int

    @validator("amount")
    def amount_between_one_and_ten_inclusive(cls, value):
        if value < 1 or value > 10:
            raise ValueError("Amount must be between 1 and 10 (inclusive)")
        return value


ORDER_STATUSES = {"pending": "PENDING"}
