import hashlib
import os


class Hasher:
    @staticmethod
    def generate_salt():
        return os.urandom(16)

    @staticmethod
    def hash(input_string, salt=b""):
        hasher = hashlib.sha256()
        hasher.update(salt + input_string.encode("utf-8"))

        return hasher.hexdigest()

    @staticmethod
    def compare(hashed_string, input_string, salt=b""):
        return (Hasher.hash(input_string, salt=salt) == hashed_string)
