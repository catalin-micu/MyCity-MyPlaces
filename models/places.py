from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Integer, Column, String, delete, select, update, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from models import BaseTable, logger


class PlacesColumns:
    PLACE_ID = 'place_id'
    GOOGLE_ID = 'google_id'
    USER_ID = 'user_id'
    IS_PRIVATE = 'is_private'


PLACES_COLUMNS_LIST = [PlacesColumns.PLACE_ID, PlacesColumns.GOOGLE_ID, PlacesColumns.USER_ID,
                               PlacesColumns.IS_PRIVATE]

ACCEPTED_IDENTIFIER_TYPES = {PlacesColumns.PLACE_ID, PlacesColumns.GOOGLE_ID, PlacesColumns.USER_ID}


class Places(BaseTable):
    __tablename__ = 'places'

    place_id = Column(Integer, primary_key=True)
    google_id = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    is_private = Column(Boolean, default=True)

    users = relationship('Users', backref=backref('places', uselist=False))

    def insert_place(self, place_data: dict) -> []:
        receipt = []

        insert_stmt = insert(Places).values(place_data).returning(Places.google_id)

        inserted_row = self.session.execute(insert_stmt)
        self.session.commit()

        for row in inserted_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully inserted place: \n\t\t{place_data}\n")

        return receipt

    def delete_place(self, identifier: str, identifier_type: str):
        if identifier_type not in ACCEPTED_IDENTIFIER_TYPES:
            logger.error(f"Unknown identifier type: '{identifier_type}'")
            raise StopIteration

        delete_stmt = delete(Places)
        if identifier_type == PlacesColumns.PLACE_ID:
            delete_stmt = delete_stmt.where(Places.place_id == identifier)
        else:
            delete_stmt = delete_stmt.where(Places.google_id == identifier)
        delete_stmt = delete_stmt.returning(Places.google_id)

        deleted_rows = self.session.execute(delete_stmt).fetchall()
        self.session.commit()

        logger.info(f"Successfully deleted place:\n\t\t{deleted_rows[0]}")

    def get_places(self, identifier, identifier_type):
        if identifier_type not in ACCEPTED_IDENTIFIER_TYPES:
            logger.error(f"Unknown identifier type: '{identifier_type}'")
            raise StopIteration

        select_stmt = select(Places).where(Places.__table__.c[identifier_type].in_([identifier]))
        rows = self.session.execute(select_stmt).fetchall()
        rows = [super(Places, Places)._transform_row_into_dict(r, PLACES_COLUMNS_LIST) for r in rows]

        return rows
