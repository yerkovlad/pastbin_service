import hashlib
import string as stri
import random

from src.database.db import write_to_free_urls

async def generate_string_hash():
    """
    Generates a random string of characters and creates a SHA-256 hash of it.

    Returns:
    - string_hash (str): A hexadecimal string representing the SHA-256 hash of the generated string.

    Steps:
    1. A random string of 50 characters, consisting of lowercase letters and digits, is generated.
    2. The string is encoded to bytes using UTF-8.
    3. A SHA-256 hash object is created and the encoded string is hashed.
    4. The resulting hash is returned as a hexadecimal string.
    """
    N = 50
    string = ''.join(random.choices(stri.ascii_lowercase + stri.digits, k=N))
    string = string.encode("utf-8")

    sha256 = hashlib.sha256()
    sha256.update(string)

    string_hash = sha256.hexdigest()
    return string_hash

async def free_urls():
    """
    Generates a unique hash and stores it in the database.

    Returns:
    - dict: A dictionary with a message indicating the status of the operation.

    Steps:
    1. A unique hash is generated using the `generate_string_hash` function.
    2. This hash is then written to the database using the `write_to_free_urls` function.
    3. A message indicating that URL processing has started is returned.
    """
    g_hash = await generate_string_hash()
    await write_to_free_urls(g_hash)
    return {"message": "URL processing started in the background"}