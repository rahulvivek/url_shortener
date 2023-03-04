import string
import random

def get_code(length):
    """Method to generate a random string."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))