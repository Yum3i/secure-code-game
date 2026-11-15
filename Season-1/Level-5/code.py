# Welcome to Secure Code Game Season-1/Level-5!

# This is the last level of our first season, good luck!

import secrets
import os
import bcrypt

class Random_generator:

    # generates a random token
    def generate_token(self, length=8, alphabet=(
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )):
        # secrets instead of random: random is predictable and not meant for security
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    # generates salt
    def generate_salt(self, rounds=12):
        # the salt is made by bcrypt itself, from a secure random source
        return bcrypt.gensalt(rounds)

class Bcrypt_hasher:

    # hashes the password with bcrypt, which is slow on purpose and salts every hash
    # note: bcrypt only uses the first 72 bytes of the password
    def password_hash(self, password, salt=None):
        if salt is None:
            salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)
        return password_hash.decode('ascii')

    # checks the password against the stored hash (the salt is read from the hash)
    def password_verification(self, password, password_hash):
        return bcrypt.checkpw(password.encode(), password_hash.encode('ascii'))

# old names are kept so that existing code still works,
# but both now use bcrypt: plain SHA-256 and MD5 are too fast to brute-force
SHA256_hasher = Bcrypt_hasher
MD5_hasher = Bcrypt_hasher

# a collection of sensitive secrets necessary for the software to operate
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
# secrets are read from the environment, not stored in the source code
SECRET_KEY = os.environ.get('SECRET_KEY')
PASSWORD_HASHER = 'Bcrypt_hasher'


# Contribute new levels to the game in 3 simple steps!
# Read our Contribution Guideline at github.com/skills/secure-code-game/blob/main/CONTRIBUTING.md