import logging
from functools import wraps
from typing import TypeVar, Callable

T = TypeVar('T')

# Configure logging
logger = logging.getLogger(__name__)


def handle_db_errors(operation_name: str, default_return=None):
    """
    Decorator for consistent database error handling.

    Wraps a function to catch exceptions, log them properly, and return
    a default value if specified.

    :param operation_name: Description of the operation (e.g., "add employee")
    :type operation_name: str
    :param default_return: Value to return on error (if None, re-raises exception)
    :type default_return: Any
    :return: Decorated function
    :rtype: Callable

    Example:
        @handle_db_errors("add employee", default_return=False)
        def addEmployee(self, person, table):
            # ... database operations ...
            return True
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {operation_name}: {repr(e)}")
                print(f"Error in {operation_name}: {repr(e)}")  
                if default_return is not None:
                    return default_return
                raise
        return wrapper
    return decorator
