import random
import string


def create_verification_code():
    return ''.join(random.choices(string.digits, k=4))


def create_invite_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))
