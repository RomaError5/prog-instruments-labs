from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import UnsupportedAlgorithm

from file_manager import FileManager


class AsymmetricRSA:
    @staticmethod
    def generate_keys() -> (rsa.RSAPrivateKey, rsa.RSAPublicKey):
        """
        Generates public and private RSA keys
        :return: Private key, public key
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def export_keys(private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey,
                    private_path: str, public_path: str) -> None:
        """
        Serialization of asymmetric keys
        :param private_key: Private key
        :param public_key: Public key
        :param private_path: Path to file to save private key
        :param public_path: Path to file to save public key
        :return: None
        """
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        FileManager.save_bytes(private_path, private_pem)
        FileManager.save_bytes(public_path, public_pem)

    @staticmethod
    def load_private_key(path: str) -> rsa.RSAPrivateKey:
        """
        Loads a private key from a file and deserializes it
        :param path: Path to file to load private key
        :return: private key
        """
        try:
            key_data = FileManager.load_bytes(path)
            private_key = serialization.load_pem_private_key(
                key_data,
                password=None,
                backend=default_backend()
            )
            return private_key
        except UnsupportedAlgorithm:
            raise Exception("Unsupported key algorithm")
        except ValueError:
            raise Exception("Invalid key format")

    @staticmethod
    def encrypt(data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
        """
        Encrypting data with public RSA key with using OAEP encrypting standard with SHA256 hash-algorithm
        :param data: Data for encryption
        :param public_key: Public key
        :return: Encrypted data
        """
        return public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def decrypt(data: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
        """
        Decrypting data with public RSA key with using OAEP encrypting standard with SHA256 hash-algorithm
        :param data: Data for decryption
        :param private_key: Private key
        :return: Decrypted data
        """
        return private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )