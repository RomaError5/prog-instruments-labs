import json


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
            with open(path, "wb") as f:
                f.write(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file was not found: {path}")
        except Exception as e:
            raise Exception(f"An error occurred with the file: {str(e)}")

    @staticmethod
    def load_bytes(path: str) -> bytes:
        """
        Reading data from a file
        :param path: path to the file
        :return: bytes format object
        """
        try:
            with open(path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file was not found: {path}")
        except Exception as e:
            raise Exception(f"An error occurred with the file: {str(e)}")

    @staticmethod
    def load_json(json_path: str) -> dict:
        """
        Method read json file as a dict with requirements
        :param json_path: path of json file
        :return: dictionary
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {json_path}")

    @staticmethod
    def read_file(filename: str) -> str:
        """
        Opens text file from given directory
        :param filename: Directory to file
        :return: String with file contents
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError as e:
            print(f"File doesn't exist or the path specified is invalid: {e}")
        except PermissionError as e:
            print(f"Can't access this file: {e}")
        except Exception as e:
            print(f"Error reading file: {e}. Check for correct data")

    @staticmethod
    def write_file(filename: str, data: str) -> None:
        """
        Saves string to .txt file
        :param filename: Path to .txt file
        :param data: Contents for file
        :return: None
        """
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(data)
        except Exception as e:
            print(f"Something went wrong: {e}")