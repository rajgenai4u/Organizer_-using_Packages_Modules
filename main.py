"""
main.py
-------
Executable script that orchestrates folder scanning, category detection,
and file moving while handling and logging failures.
"""

import os
from organizer.detector import detect_category
from organizer.mover import move_file
from organizer.logger_config import setup_logger
from organizer.exceptions import UnsupportedFileError, DuplicateFileError

# Initialize system logger
logger = setup_logger()


def organize_folder(source_folder: str, destination_base: str):
    """
    Scans a source folder, detects file categories, and moves files into subfolders.

    Parameters:
    - source_folder (str): Directory containing unorganized files.
    - destination_base (str): Base output directory where category subfolders are created.
    """
    # Verify input directory existence
    if not os.path.exists(source_folder):
        logger.error(f"Source folder '{source_folder}' does not exist.")
        return

    # Iterate over all items in the target directory
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)

        # Skip subdirectories to only process files
        if os.path.isdir(item_path):
            continue

        try:
            # Detect file category and build targeted subfolder path
            category = detect_category(item_path)
            target_dir = os.path.join(destination_base, category)

            # Relocate file to category folder
            move_file(item_path, target_dir, logger)

        # Catch specific failures to allow remaining batch execution
        except UnsupportedFileError as e:
            logger.warning(f"Skipping unsupported file '{item}': {e}")
        except DuplicateFileError as e:
            logger.warning(f"Skipping duplicate file '{item}': {e}")
        except PermissionError as e:
            logger.error(f"Skipping '{item}' due to permission error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing '{item}': {e}")


if __name__ == "__main__":
    # Define source and output destination directories
    SOURCE_DIRECTORY = "./input_folder"
    DESTINATION_DIRECTORY = "./organized_output"

    # Start folder organization batch loop
    organize_folder(SOURCE_DIRECTORY, DESTINATION_DIRECTORY)
