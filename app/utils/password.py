from passlib.hash import bcrypt_sha256


def hash_password(password: str) -> str:
  return bcrypt_sha256.hash(str(password))


def verify_password(password: str, hashed: str) -> bool:
  return bcrypt_sha256.verify(str(password), hashed)
