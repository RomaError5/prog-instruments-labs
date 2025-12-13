import argparse

from cryptosystem.hybrid_system import HybridCryptoSystem
from file_manager import FileManager


def parse_arguments() -> argparse.Namespace:
    """
    Function parses arguments from cmd
    :return: Object with arguments
    """
    parser = argparse.ArgumentParser(
        description = "Hybrid crypto system (RSA + 3DES)",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-s', '--settings', default='settings.json',
                        help = 'Path to JSON file containing settings')

    parser.add_argument('-k', '--key_length', type = int, choices = [64, 128, 192], default = 192,
                        help = 'Symmetric key length in bits (64, 128 or 192)')

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-gen', '--generation', action = 'store_true', help = 'Generate keys')
    group.add_argument('-enc', '--encryption', action = 'store_true', help = 'Encrypt file')
    group.add_argument('-dec', '--decryption', action = 'store_true', help = 'Decrypt file')

    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        if args.key_length not in (64, 128, 192):
            raise ValueError("3DES key length must be 64, 128 or 192 bits")
        settings = FileManager.load_json(args.settings)

        if args.generation:
            HybridCryptoSystem.generate_keys(
                args.key_length,
                settings["private_key"],
                settings["public_key"],
                settings["symmetric_key"]
            )
            print(
                f"Keys generated and saved:\n"
                f" - Private key: {settings['private_key']}\n"
                f" - Public key: {settings['public_key']}\n"
                f" - Symmetric key: {settings['symmetric_key']}"
            )
        elif args.encryption:
            HybridCryptoSystem.encrypt(
                settings["initial_file"],
                settings["private_key"],
                settings["symmetric_key"],
                settings["encrypted_file"]
            )
            print(f"File encrypted and saved to {settings['encrypted_file']}")
        elif args.decryption:
            HybridCryptoSystem.decrypt(
                settings["encrypted_file"],
                settings["private_key"],
                settings["symmetric_key"],
                settings["decrypted_file"]
            )
            print(f"File decrypted and saved to {settings['decrypted_file']}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()