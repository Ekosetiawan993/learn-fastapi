from passlib.context import CryptContext

# what hashing algo that used
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hashing_password(password: str):
    return pwd_context.hash(password)


def verify_login(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
