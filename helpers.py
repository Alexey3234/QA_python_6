def generate_phone_number():
    from random import randint
    return f"8{randint(1000000000, 9999999999)}"

def generate_random_string(length=10):
    import random
    import string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))