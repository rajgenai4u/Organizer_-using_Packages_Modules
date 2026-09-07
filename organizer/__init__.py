"""
__init__.py
-----------
Exposes module functions and custom exceptions at the package level.
"""

from .detector import detect_category
from .mover import move_file
from .logger_config import setup_logger
from .exceptions import UnsupportedFileError, DuplicateFileError

__all__ = [
    "detect_category",
    "move_file",
    "setup_logger",
    "UnsupportedFileError",
    "DuplicateFileError"
]