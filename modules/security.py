import bcrypt


class Security:

    @staticmethod
    def hash_password(password):

        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

    @staticmethod
    def verify_password(
        password,
        hashed
    ):

        return bcrypt.checkpw(
            password.encode(),
            hashed.encode()
        )