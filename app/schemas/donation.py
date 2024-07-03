from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, conint


class DonationBase(BaseModel):
    full_amount: conint(strict=True, gt=0) = Field(...)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationRegularUserDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationSuperUserDB(DonationRegularUserDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
