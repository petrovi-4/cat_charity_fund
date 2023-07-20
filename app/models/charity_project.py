from sqlalchemy import Column, String, Text

from .base import ProjectDonation


class CharityProject(ProjectDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)