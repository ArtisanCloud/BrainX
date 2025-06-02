import hashlib

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

from app import local_client_storage
from app.cache.factory import CacheFactory
from app.core.exception.exceptions import PrivateKeyNotFoundError

prefix_hybrid = b"HYBRID:"


def get_tenant_private_key_path(tenant_uuid):
    bucket_name = "private_keys/{identifier}".format(identifier=tenant_uuid)
    filepath = "private.pem"
    return bucket_name, filepath


def generate_key_pair(identifier, size=2048):
    private_key = RSA.generate(size)
    public_key = private_key.publickey()

    pem_private = private_key.export_key()
    pem_public = public_key.export_key()

    bucket_name, filepath = get_tenant_private_key_path(identifier)

    local_client_storage.save(bucket_name, filepath, pem_private)

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
    rsa_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA256)

    # 随机生成 AES key
    aes_key = hashlib.sha256(rsa_key.publickey().export_key()).digest()[:32]
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)

    ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext.encode())

    # RSA 加密 AES key
    enc_aes_key = cipher_rsa.encrypt(aes_key)

    return (
            prefix_hybrid +
            enc_aes_key +
            cipher_aes.nonce +
            tag +
            ciphertext
    )


def rsa_decrypt(tenant_uuid: str, ciphertext):
    rsa_key, cipher_rsa = get_decrypt_decoding(tenant_uuid)

    plaintext = decrypt_content_with_decoding(ciphertext, rsa_key, cipher_rsa)

    return plaintext


def get_decrypt_decoding(tenant_uuid):
    bucket_name, filename = get_tenant_private_key_path(tenant_uuid)
    filepath = bucket_name + "/" + filename
    cache_key = "tenant_privkey:{hash}".format(hash=hashlib.sha3_256(filepath.encode()).hexdigest())

    cache_client = CacheFactory.get_cache()
    private_key = cache_client.get(cache_key)
    if not private_key:
        try:
            private_key = local_client_storage.load_once(filepath)
        except FileNotFoundError:
            raise PrivateKeyNotFoundError(f"Private key not found, tenant_uuid: {tenant_uuid}")

        cache_client.set(cache_key, private_key, 120)

    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA256)

    return rsa_key, cipher_rsa


def decrypt_content_with_decoding(encrypted_text, rsa_key, cipher_rsa):
    if encrypted_text.startswith(prefix_hybrid):
        encrypted_text = encrypted_text[len(prefix_hybrid):]

        enc_aes_key = encrypted_text[: rsa_key.size_in_bytes()]
        nonce = encrypted_text[rsa_key.size_in_bytes(): rsa_key.size_in_bytes() + 16]
        tag = encrypted_text[rsa_key.size_in_bytes() + 16: rsa_key.size_in_bytes() + 32]
        ciphertext = encrypted_text[rsa_key.size_in_bytes() + 32:]

        aes_key = cipher_rsa.decrypt(enc_aes_key)

        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        decrypted_text = cipher_aes.decrypt_and_verify(ciphertext, tag)
    else:
        decrypted_text = cipher_rsa.decrypt(encrypted_text)

    return decrypted_text.decode()
