from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from app import lib_storage


def generate_key_pair(identifier, size=2048):
    private_key = RSA.generate(size)
    public_key = private_key.publickey()

    pem_private = private_key.export_key()
    pem_public = public_key.export_key()

    filepath = "storage/private_keys/{identifier}".format(identifier=identifier) + "/private.pem"

    lib_storage.save(filepath, pem_private)

    return pem_public.decode()


def generate_rsa_key_pair(bits=2048):
    """
    Generate RSA key pair.

    :param bits: Number of bits for the RSA key (default: 2048).
    :return: Tuple containing (private_key, public_key) in PEM format.
    """
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    return private_key, public_key


def rsa_encrypt(public_key_pem, plaintext):
    """
    Encrypt plaintext using RSA public key.

    :param public_key_pem: RSA public key in PEM format.
    :param plaintext: Plaintext to encrypt.
    :return: Encrypted ciphertext.
    """
    rsa_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    ciphertext = cipher_rsa.encrypt(plaintext.encode())

    return ciphertext


def rsa_decrypt(private_key_pem, ciphertext):
    """
    Decrypt ciphertext using RSA private key.

    :param private_key_pem: RSA private key in PEM format.
    :param ciphertext: Ciphertext to decrypt.
    :return: Decrypted plaintext.
    """
    rsa_key = RSA.import_key(private_key_pem)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    plaintext = cipher_rsa.decrypt(ciphertext).decode()

    return plaintext
