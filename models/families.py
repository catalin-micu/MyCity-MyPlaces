import json
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Integer, Column, String, delete, select, update
from sqlalchemy.orm import relationship

from models import BaseTable, logger


class FamiliesColumns:
    FAMILY_ID = 'family_id'
    FAMILY_NAME = 'family_name'


FAMILY_COLUMNS_LIST = [FamiliesColumns.FAMILY_ID, FamiliesColumns.FAMILY_NAME]

ACCEPTED_IDENTIFIER_TYPES = {FamiliesColumns.FAMILY_ID}


class Families(BaseTable):
    __tablename__ = 'families'

    family_id = Column(Integer, primary_key=True)
    family_name = Column(String, nullable=False)

    family_members = relationship('FamilyMembers', back_populates='families')

    def insert_family(self, family_name: str) -> []:
        receipt = []

        insert_stmt = insert(Families).values({FamiliesColumns.FAMILY_NAME: family_name}).returning(
            Families.family_name)

        inserted_row = self.session.execute(insert_stmt)
        self.session.commit()

        for row in inserted_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully inserted family: \n\t\t{family_name}\n")

        return receipt
