import random
import string

def generate_uniqid(length):
    return ''.join(
        random.choice(string.lowercase+string.digits) for i in range(length)
    )
