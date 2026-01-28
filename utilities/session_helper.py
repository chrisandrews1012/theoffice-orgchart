from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine


@contextmanager
def get_session(engine: Engine):
    """
    Reusable session context manager for write operations.

    Automatically commits on success and rolls back on error.
    Always closes the session.

    :param engine: SQLAlchemy engine instance
    :type engine: Engine
    :yield: SQLAlchemy session
    :rtype: Session

    Example:
        with get_session(self.connection) as session:
            session.execute(insert_stmt)
            # Auto-commits if no error occurs
            # Auto-rollbacks if error occurs
    """
    session = Session(engine)
    try:
        yield session
        session.commit()  # Auto-commit on success
    except Exception:
        session.rollback()  # Auto-rollback on error
        raise
    finally:
        session.close()  # Always close


@contextmanager
def get_readonly_session(engine: Engine):
    """
    Read-only session (no commit needed).

    Use this for SELECT queries where no data modification occurs.
    Always closes the session.

    :param engine: SQLAlchemy engine instance
    :type engine: Engine
    :yield: SQLAlchemy session
    :rtype: Session

    Example:
        with get_readonly_session(self.connection) as session:
            result = session.query(table).all()
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
