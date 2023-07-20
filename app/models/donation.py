from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import ProjectDonation


class Donation(ProjectDonation):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)