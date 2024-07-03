from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base
from app.models.mixins import InvesititionsMixin, DateMixin


class Donation(InvesititionsMixin, DateMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
