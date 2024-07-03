from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Extra, Field, conint

from app.core.constants import (
    MIN_CHARITY_PROJECT_NAME_CHAR,
    MAX_CHARITY_PROJECT_NAME_CHAR,
    MIN_CHARITY_PROJECT_DESCRIPTION_CHAR,
)


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_CHARITY_PROJECT_NAME_CHAR,
        max_length=MAX_CHARITY_PROJECT_NAME_CHAR,
    )
    description: str = Field(
        ...,
        min_length=MIN_CHARITY_PROJECT_DESCRIPTION_CHAR,
    )
    full_amount: conint(strict=True, gt=0) = Field(
        ...,
    )

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_CHARITY_PROJECT_NAME_CHAR,
        max_length=MAX_CHARITY_PROJECT_NAME_CHAR,
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_CHARITY_PROJECT_DESCRIPTION_CHAR,
    )
    full_amount: Optional[conint(strict=True, gt=0)] = Field(
        None,
    )

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
