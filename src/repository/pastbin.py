from src.database.db import write_to_text_user, first_hash_from_free_urls, find_one_message, delete_one_from_free_urls, all_text_users

async def past(username: str, text: str):
    """
    Stores a user's text message with an associated hash and removes the hash from the database.

    Args:
    - username (str): The username of the person submitting the text.
    - text (str): The text message to be stored.

    Returns:
    - str or None: The hash associated with the text if successful, otherwise None.

    Steps:
    1. Retrieves the most recent hash from the database using `first_hash_from_free_urls`.
    2. If a hash is found:
       - Stores the text message in the database with the retrieved hash using `write_to_text_user`.
       - Deletes the hash from the database using `delete_one_from_free_urls`.
       - Returns the hash.
    3. If no hash is found, returns None.
    """
    free_hash = await first_hash_from_free_urls()
    if free_hash:
        await write_to_text_user(username, text, free_hash)
        await delete_one_from_free_urls(free_hash)
        return free_hash
    return None

async def read_message_with_id(message_id: str):
    """
    Retrieves a message from the database based on its unique identifier.

    Args:
    - message_id (str): The unique identifier of the message.

    Returns:
    - dict: A dictionary containing the message details (username and text) if found.

    Steps:
    1. Finds the message in the database using the `find_one_message` function with the given message ID.
    2. Returns the message details.
    """
    return await find_one_message({"id": message_id})

async def all_text():
    """
    Retrieves all text messages from the database and removes the MongoDB `_id` field from each document.

    Returns:
    - list: A list of dictionaries, each containing message details (username and text) with the `_id` field removed.

    Steps:
    1. Fetches all text documents from the database using the `all_text_users` function.
    2. Removes the `_id` field from each document.
    3. Returns the cleaned list of documents.
    """
    documents = await all_text_users()
    cleaned_documents = [{key: value for key, value in doc.items() if key != "_id"} for doc in documents]
    return cleaned_documents