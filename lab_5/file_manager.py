import json
import logging


logger = logging.getLogger(__name__)

class FileManager:

    @staticmethod
    def save_bytes(path: str, data: bytes) -> None:
        """
        Writing data to a file
        :param path: path to file to save
        :param data: data to save
        :return: None
        """
        try:
            logger.debug(f"Saving file: {path}")
            with open(path, "wb") as f:
                f.write(data)
            logger.debug(f"File {path} saved successfully, size: {len(data)} characters")
        except FileNotFoundError:
            logger.error(f"The file was not found: {path}")
        except Exception as e:
            logger.error(f"An error occurred with the file: {str(e)}")

    @staticmethod
    def load_bytes(path: str) -> bytes:
        """
        Reading data from a file
        :param path: path to the file
        :return: bytes format object
        """
        try:
            logger.debug(f"Reading file: {path}")
            with open(path, "rb") as f:
                content = f.read()
                logger.debug(f"File {path} successfully read, size: {len(content)} characters")
                return content
        except FileNotFoundError:
            logger.error(f"The file was not found: {path}")
        except Exception as e:
            logger.error(f"An error occurred with the file: {str(e)}")

    @staticmethod
    def load_json(json_path: str) -> dict:
        """
        Method read json file as a dict with requirements
        :param json_path: path of json file
        :return: dictionary
        """
        try:
            logger.debug(f"Reading file: {json_path}")
            with open(json_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                logger.debug(f"File {json_path} successfully read, size: {len(content)} characters")
                return content
        except FileNotFoundError:
            logger.error(f"JSON file not found: {json_path}")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in file: {json_path}")

    @staticmethod
    def read_file(filename: str) -> str:
        """
        Opens text file from given directory
        :param filename: Directory to file
        :return: String with file contents
        """
        try:
            logger.debug(f"Reading file: {filename}")
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
                logger.debug(f"File {filename} successfully read, size: {len(content)} characters")
                return content
        except FileNotFoundError as e:
            logger.error(f"File doesn't exist or the path specified is invalid: {e}")
        except PermissionError as e:
            logger.error(f"Can't access this file: {e}")
        except Exception as e:
            logger.error(f"Error reading file: {e}. Check for correct data")

    @staticmethod
    def write_file(filename: str, data: str) -> None:
        """
        Saves string to .txt file
        :param filename: Path to .txt file
        :param data: Contents for file
        :return: None
        """
        try:
            logger.debug(f"Saving file: {filename}")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(data)
            logger.debug(f"File {filename} saved successfully, size: {len(data)} characters")
        except Exception as e:
            logger.error(f"Something went wrong: {e}")