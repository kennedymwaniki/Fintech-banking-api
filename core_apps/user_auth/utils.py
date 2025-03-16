import random
import string


def generate_otp(length=6) -> string:
    return "".join(random.choices(string.digits, k=length))
