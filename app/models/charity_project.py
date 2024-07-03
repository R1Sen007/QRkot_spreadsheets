from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.mixins import InvesititionsMixin, DateMixin
from app.core.constants import MAX_CHARITY_PROJECT_NAME_CHAR


class CharityProject(InvesititionsMixin, DateMixin, Base):
    name = Column(String(MAX_CHARITY_PROJECT_NAME_CHAR),
                  unique=True, nullable=False)
    description = Column(Text, nullable=False)
