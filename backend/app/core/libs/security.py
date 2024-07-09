import hashlib
import bcrypt


def encode_password(plain_password: str) -> str:
    encoded = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return encoded


def hash_password(encoded_password: str) -> str:
    hashed = bcrypt.hashpw(encoded_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def hash_plain_password(plain_password: str) -> str:
    encoded_password = encode_password(plain_password)
    hashed_password = hash_password(encoded_password)
    return hashed_password


def check_password(customer_password: str, req_password: str):
    if not bcrypt.checkpw(req_password.encode('utf-8'), customer_password.encode('utf-8')):
        raise Exception("密码不正确")
    return True
