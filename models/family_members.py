import json
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Integer, Column, String, delete, select, update, ForeignKey
from sqlalchemy.orm import relationship, backref

from models import BaseTable, logger


class FamilyMembersColumns:
    FAMILY_MEMBERS_ID = 'family_members_id'
    FAMILY_ID = 'family_id'
    USER_ID = 'user_id'


FAMILY_MEMBERS_COLUMNS_LIST = [FamilyMembersColumns.FAMILY_MEMBERS_ID, FamilyMembersColumns.FAMILY_ID,
                               FamilyMembersColumns.USER_ID]

ACCEPTED_IDENTIFIER_TYPES = {FamilyMembersColumns.FAMILY_MEMBERS_ID, FamilyMembersColumns.FAMILY_ID,
                             FamilyMembersColumns.USER_ID}


class FamilyMembers(BaseTable):
    __tablename__ = 'family_members'

    family_members_id = Column(Integer, primary_key=True)
    family_id = Column(Integer, ForeignKey('families.family_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    users = relationship('Users', backref=backref('family_members', uselist=False))
    families = relationship('Families', backref=backref('family_members', uselist=False))

    def insert_family_member(self, family_id: int, user_id: int) -> []:
        receipt = []

        insert_stmt = insert(FamilyMembers).values({FamilyMembersColumns.FAMILY_ID: family_id,
                                                    FamilyMembersColumns.USER_ID: user_id}).returning(
            FamilyMembers.family_members_id)

        inserted_row = self.session.execute(insert_stmt)
        self.session.commit()

        for row in inserted_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully added user '{user_id}' to family '{family_id}'")

        return receipt
