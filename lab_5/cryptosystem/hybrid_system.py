from .asymmetric import AsymmetricRSA
from file_manager import FileManager
from .symmetric import Symmetric3DES


class HybridCryptoSystem:

    @staticmethod
    def generate_keys(key_length: int, private_path: str, public_path: str, symmetric_path: str) -> None:
        """
        Hybrid System Key Generation.
        :param key_length: Key length for 3DES (64, 128, 192)
        :param private_path: Path to file to save private key
        :param public_path: Path to file to save public key
        :param symmetric_path: Path to the file to save the encrypted symmetric key
        :return: None
        """
        private_key, public_key = AsymmetricRSA.generate_keys()
        symmetric_key = Symmetric3DES.generate_key(key_length)

        AsymmetricRSA.export_keys(private_key, public_key, private_path, public_path)
        c_symmetric_key = AsymmetricRSA.encrypt(symmetric_key, public_key)
        FileManager.save_bytes(symmetric_path, c_symmetric_key)

    @staticmethod
    def encrypt(file_path: str, private_path: str, symmetric_path: str, save_path: str) -> None:
        """
        Data encryption by hybrid system
        :param file_path: Path to the file to encrypt
        :param private_path: Path to file to load private key
        :param symmetric_path: Path to the file to load the encrypted symmetric key
        :param save_path: Path to file to save encrypted data
        :return:
        """
        c_symmetric_key = FileManager.load_bytes(symmetric_path)
        private_key = AsymmetricRSA.load_private_key(private_path)
        text = FileManager.read_file(file_path)

        symmetric_key = AsymmetricRSA.decrypt(c_symmetric_key, private_key)
        encrypted_text = Symmetric3DES.encrypt(text.encode('utf-8'), symmetric_key)
        FileManager.save_bytes(save_path, encrypted_text)

    @staticmethod
    def decrypt(file_path: str, private_path: str, symmetric_path: str, save_path: str) -> None:
        """
        Data decryption by hybrid system
        :param file_path: Path to the file to decrypt
        :param private_path: Path to file to load private key
        :param symmetric_path: Path to the file to load the encrypted symmetric key
        :param save_path: Path to file to save decrypted data
        :return:
        """
        c_symmetric_key = FileManager.load_bytes(symmetric_path)
        private_key = AsymmetricRSA.load_private_key(private_path)
        text = FileManager.load_bytes(file_path)

        symmetric_key = AsymmetricRSA.decrypt(c_symmetric_key, private_key)
        decrypted_text = Symmetric3DES.decrypt(text, symmetric_key)
        FileManager.write_file(save_path, decrypted_text.decode('utf-8'))

