import logging

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
import os


logger = logging.getLogger(__name__)

class Symmetric3DES:
    @staticmethod
    def generate_key(key_length: int) -> bytes:
        """
        Generate a 3DES key of the selected length
        :param key_length: Key length (64, 128, 192)
        :return: Unencrypted symmetric key
        """
        key = os.urandom(key_length // 8)
        logger.debug(f"Symmetric key of size {key_length} bits was generated")
        return key

    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        """
        Encrypting data with 3DES algorythm in Cipher Block Chaining mode with random initialization vector
        :param data: Data for encryption
        :param key: Symmetric key
        :return: Encrypted data
        """
        logger.debug(f"3DES encryption, text size: {len(data)} characters")
        iv = os.urandom(8)  # 3DES block size
        padder = sym_padding.PKCS7(algorithms.TripleDES.block_size).padder()  # 64 bits = 8 bytes block size
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(
            algorithms.TripleDES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        logger.debug(f"3DES encryption completed, result size: {len(iv + ciphertext)} characters")
        return iv + ciphertext

    @staticmethod
    def decrypt(data: bytes, key: bytes) -> bytes:
        """
        Decrypting data with 3DES algorythm in Cipher Block Chaining mode with random initialization vector
        :param data: Data for decryption
        :param key: Symmetric key
        :return: Decrypted data
        """
        logger.debug(f"3DES decryption, text size: {len(data)} characters")
        iv = data[:8]
        ct = data[8:]

        cipher = Cipher(
            algorithms.TripleDES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ct) + decryptor.finalize()

        unpadder = sym_padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        logger.debug(f"3DES decryption completed, result size: {len(data)} characters")
        return data