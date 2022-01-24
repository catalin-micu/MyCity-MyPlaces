import json
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Integer, Column, String, delete, select, update
from sqlalchemy.orm import relationship

from models import BaseTable, logger


class UsersColumns:
    USER_ID = 'user_id'
    USER_NAME = 'user_name'
    ADDRESS_LINE = 'address_line'
    CITY = 'city'
    EMAIL = 'email'
    PASSWD = 'passwd'


USER_COLUMNS_LIST = [UsersColumns.USER_ID, UsersColumns.USER_NAME, UsersColumns.ADDRESS_LINE, UsersColumns.CITY,
                     UsersColumns.EMAIL, UsersColumns.PASSWD]

ACCEPTED_IDENTIFIER_TYPES = {UsersColumns.USER_ID, UsersColumns.EMAIL}


class Users(BaseTable):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    address_line = Column(String, nullable=False)
    city = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    passwd = Column(String, nullable=False)

    def insert_user(self, user_data: dict) -> list:
        """
        inserts a new user in the db if entry doesn't already exist
        :param user_data: dict with column name as keys and appropriate values
        :return: receipt list
        """
        if self.check_user_existence(identifier=user_data.get(UsersColumns.EMAIL), identifier_type=UsersColumns.EMAIL):
            logger.error(f"User with email '{user_data.get(UsersColumns.EMAIL)}' already exists")
            raise StopIteration

        receipt = []

        insert_stmt = insert(Users).values(user_data).returning(Users.user_name, Users.email)

        inserted_row = self.session.execute(insert_stmt)
        self.session.commit()

        for row in inserted_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully inserted user: \n\t\t{[user_data.get(UsersColumns.USER_NAME)]}\n")

        return receipt

    def check_user_existence(self, identifier: str, identifier_type: str) -> bool:
        """
        check if a user already exists in the db
        :param identifier: value of the unique identifier that is being used
        :param identifier_type: column name of the identifier
        :return: true if user is found else false
        """
        if identifier_type not in ACCEPTED_IDENTIFIER_TYPES:
            logger.error(f"Unknown identifier type: '{identifier_type}'")
            raise StopIteration

        select_stmt = select(Users).where(Users.__table__.c[identifier_type] == identifier)

        exec_result = self.session.execute(select_stmt)
        return bool(len(exec_result.fetchall()))

    def delete_rows(self, rows_to_delete: list, identifier_type: str) -> []:
        """
        deletes rows based on an unique identifier (user_id / email, according to table definition)
        :param rows_to_delete: list of values that uniquely identify a row
        :param identifier_type: identifier for delete statement
        :return: list of dicts with info about deleted rows(name, email, phone_number)
        """
        receipt = []
        if identifier_type not in ACCEPTED_IDENTIFIER_TYPES:
            logger.error(f"Unknown identifier type: '{identifier_type}'")
            raise StopIteration

        delete_stmt = delete(Users)
        if identifier_type == UsersColumns.USER_ID:
            delete_stmt = delete_stmt.where(Users.user_id.in_(rows_to_delete))
        else:
            delete_stmt = delete_stmt.where(Users.email.in_(rows_to_delete))
        delete_stmt = delete_stmt.returning(Users.user_name, Users.email)

        deleted_rows = self.session.execute(delete_stmt).fetchall()
        self.session.commit()

        logger.info(f"Successfully deleted users with '{identifier_type}' identifier = '{rows_to_delete}'")

        for row in deleted_rows:
            receipt.append(dict(row._mapping))

        return receipt

    def update_user(self, identifier: str, identifier_type: str, update_data: dict) -> []:
        if not self.check_user_existence(identifier=identifier, identifier_type=identifier_type):
            logger.error(f"User with '{identifier_type}' identifier = '{identifier}' does not exist")
            raise StopIteration

        receipt = []

        update_stmt = update(Users).where(Users.__table__.c[identifier_type] == identifier).values(update_data). \
            returning(Users.user_name, Users.email)

        updated_row = self.session.execute(update_stmt)
        self.session.commit()

        for row in updated_row:
            receipt.append(dict(row._mapping))

        logger.info(f"Successfully updated user with '{identifier_type}' identifier = '{identifier}'\n\t"
                    f"with data {update_data}")

        return receipt

    def get_user_data(self, identifier: str, identifier_type: str) -> dict:
        if identifier_type not in ACCEPTED_IDENTIFIER_TYPES:
            logger.error(f"Unknown identifier type: '{identifier_type}'")
            raise StopIteration

        if not self.check_user_existence(identifier=identifier, identifier_type=identifier_type):
            logger.error(f"User with '{identifier_type}' identifier = '{identifier}' does not exist")
            raise StopIteration

        select_stmt = select(Users).where(Users.__table__.c[identifier_type] == identifier)
        exec_result = self.session.execute(select_stmt).fetchall()

        user_data = super(Users, Users)._transform_row_into_dict(exec_result[0], USER_COLUMNS_LIST)

        return user_data
