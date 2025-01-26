import random
import string

def generate_password(length=12, use_symbols=True, use_digits=True, use_uppercase=True):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    return ''.join(random.choice(characters) for _ in range(length))
