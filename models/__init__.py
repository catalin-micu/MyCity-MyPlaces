from sqlalchemy import create_engine
from sqlalchemy.engine import Row
from sqlalchemy.orm import sessionmaker, declarative_base
from custom_logger import create_logger

con_url = 'postgresql://postgres:password@localhost:5432/my_city_my_places'
engine = create_engine(con_url)
Session = sessionmaker(bind=engine)


Base = declarative_base()
logger = create_logger(__name__, '%(name)s.%(module)s.%(funcName)s -> %(levelname)s: %(message)s')


class BaseTable(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = Session()

    @staticmethod
    def _transform_row_into_dict(r: Row, columns: []) -> dict:
        result = dict()
        for c in columns:
            result[c] = getattr(r._data[0], c)

        return result

    @staticmethod
    def _transform_table_obj_into_dict(t, columns) -> dict:
        result = dict()
        for c in columns:
            result[c] = getattr(t, c)

        return result