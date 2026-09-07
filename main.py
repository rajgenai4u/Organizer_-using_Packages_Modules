import os
from organizer.detector import detect_category
from organizer.mover import move_file
from organizer.logger_config import setup_logger
from organizer.exceptions import UnsupportedFileError, DuplicateFileError

logger = setup_logger()

def organize_folder(source_folder: str, destination_base: str):
    """
    Scans source_folder, detects category for each file, and moves it to destination_base.
    """
    if not os.path.exists(source_folder):
        logger.error(f"Source folder '{source_folder}' does not exist.")
        return

    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)

        # Skip directories to process files only
        if os.path.isdir(item_path):
            continue

        try:
            category = detect_category(item_path)
            target_dir = os.path.join(destination_base, category)
            move_file(item_path, target_dir)

        except UnsupportedFileError as e:
            logger.warning(f"Skipping unsupported file '{item}': {e}")
        except DuplicateFileError as e:
            logger.warning(f"Skipping duplicate file '{item}': {e}")
        except PermissionError as e:
            logger.error(f"Skipping '{item}' due to permission error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing '{item}': {e}")

if __name__ == "__main__":
    SOURCE_DIRECTORY = "./input_folder"
    DESTINATION_DIRECTORY = "./organized_output"

    organize_folder(SOURCE_DIRECTORY, DESTINATION_DIRECTORY)
