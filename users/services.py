import random
import string


def create_verification_code():
    return ''.join(random.choices(string.digits, k=4))
