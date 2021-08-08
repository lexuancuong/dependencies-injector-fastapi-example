from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

Base = declarative_base()

class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        # delare session entity
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    # This function is a decorator that can be used to define a factory function for with statement context managers
    @contextmanager
    def session(self):# -> Callable[..., AbstractContextManager[Session]]:
        # create a new session object
        session: Session = self._session_factory()
        try:
            yield session
            # yield mean that create a generator function.
            # it will always generate or keep connecting with database with session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()
