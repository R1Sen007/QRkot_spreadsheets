from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.orm import declarative_mixin

from app.core.constants import INVESTED_START_AMOUNT


@declarative_mixin
class InvesititionsMixin:
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=INVESTED_START_AMOUNT)
    fully_invested = Column(Boolean, default=False)


@declarative_mixin
class DateMixin:
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
