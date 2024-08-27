from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from .config import CONFIG


def connect_to_database() -> Session():
    """connect to database by sqlalchemy"""

    engine = create_engine(CONFIG["sql"]["url"])
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


if __name__ == "__main__":
    connect_to_database()
