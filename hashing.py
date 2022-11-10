from passlib.context import CryptContext

pwd_context = CryptContext(schemes='bcrypt', deprecated="auto")


##using hashing algorithm bcrypt //
##deprecated="auto" na halda ni hucha, it just provides legacy support


class Hasher:

    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)
