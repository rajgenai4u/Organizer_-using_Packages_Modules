"""
mover.py
--------
Handles file moving, destination folder creation, and error scenarios like
duplicate files and permission issues.
"""

import os
import shutil
from .exceptions import DuplicateFileError


def move_file(source_path, destination_folder, logger):
    """
    Moves a file from source_path into destination_folder.
    Creates the destination folder if it doesn't exist.
    Handles duplicate files and permission errors, logging both successes and failures.
    """
    filename = os.path.basename(source_path)

    # 1. Check if source file exists
    if not os.path.exists(source_path):
        err_msg = f"Source file not found: '{source_path}'"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)

    # 2. Check and create destination folder with permission handling
    if not os.path.exists(destination_folder):
        try:
            os.makedirs(destination_folder, exist_ok=True)
            logger.info(f"Created missing destination folder: '{destination_folder}'")
        except PermissionError as e:
            err_msg = f"Permission denied while creating directory '{destination_folder}': {e}"
            logger.error(err_msg)
            raise PermissionError(err_msg)

    destination_path = os.path.join(destination_folder, filename)

    # 3. Check for duplicate filenames
    if os.path.exists(destination_path):
        err_msg = f"File '{filename}' already exists in '{destination_folder}'."
        logger.error(err_msg)
        raise DuplicateFileError(err_msg)

    # 4. Perform the file move operation with error logging
    try:
        shutil.move(source_path, destination_path)
        logger.info(f"Successfully moved: '{filename}' -> '{destination_folder}/'")
    except PermissionError as e:
        err_msg = f"Permission denied moving '{filename}' to '{destination_folder}': {e}"
        logger.error(err_msg)
        raise PermissionError(err_msg)
    except Exception as e:
        err_msg = f"Unexpected error moving '{filename}' to '{destination_folder}': {e}"
        logger.error(err_msg)
        raise Exception(err_msg)
