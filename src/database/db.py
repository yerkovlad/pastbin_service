from pymongo import MongoClient
from src.conf.config import config

# Initialize MongoDB clients and databases
client_users_info = MongoClient(config.DB_USERS_INFO)
client_free_urls = MongoClient(config.DB_FREE_URLS)
client_text_user = MongoClient(config.DB_TEXT_USER)

db_users_info = client_users_info["users_info"]["users_info"]
db_free_urls = client_free_urls["free_urls"]["free_urls"]
db_text_user = client_text_user["text_user"]["text_user"]

async def write_to_free_urls(hash):
    """
    Inserts a hash into the 'free_urls' collection.

    Parameters:
    - hash (str): The hash string to be inserted into the database.

    Actions:
    - Attempts to insert the hash into the 'free_urls' collection.
    - If an exception occurs, it is silently passed.

    Returns:
    - None
    """
    try:
        db_free_urls.insert_one({"free_hash": hash})
    except Exception as e:
        pass

async def write_to_text_user(username: str, text: str, message_id: str):
    """
    Inserts a new text message into the 'text_user' collection.

    Parameters:
    - username (str): The username associated with the message.
    - text (str): The text content of the message.
    - message_id (str): A unique identifier for the message.

    Actions:
    - Inserts the message into the 'text_user' collection.

    Returns:
    - None
    """
    db_text_user.insert_one({"username": username, "text": text, "id": message_id})

async def find_one_message(f: dict):
    """
    Finds a single message in the 'text_user' collection based on a filter.

    Parameters:
    - f (dict): A dictionary containing the filter criteria for finding a message.

    Actions:
    - Searches the 'text_user' collection using the filter.

    Returns:
    - dict: A dictionary containing the 'username' and 'text' of the found message.
    """
    req = db_text_user.find_one(f)
    output = {"username": req["username"], "text": req["text"]}
    return output

async def first_hash_from_free_urls():
    """
    Retrieves the first hash from the 'free_urls' collection.

    Parameters:
    - None

    Actions:
    - Fetches the first document from the 'free_urls' collection.

    Returns:
    - str: The 'free_hash' value from the first document.
    """
    return db_free_urls.find_one()["free_hash"]

async def delete_one_from_free_urls(free_hash: str):
    """
    Deletes a document from the 'free_urls' collection based on the hash.

    Parameters:
    - free_hash (str): The hash string used to identify the document to delete.

    Actions:
    - Deletes the document matching the given hash from the 'free_urls' collection.

    Returns:
    - None
    """
    db_free_urls.delete_one({"free_hash": free_hash})

async def find_one_user(f: dict):
    """
    Finds a single user in the 'users_info' collection based on a filter.

    Parameters:
    - f (dict): A dictionary containing the filter criteria for finding a user.

    Actions:
    - Searches the 'users_info' collection using the filter.

    Returns:
    - dict: The document found in the 'users_info' collection, or None if not found.
    """
    return db_users_info.find_one(f)

async def write_new_user(new_user: dict):
    """
    Inserts a new user document into the 'users_info' collection.

    Parameters:
    - new_user (dict): A dictionary containing the new user's details.

    Actions:
    - Inserts the new user's document into the 'users_info' collection.

    Returns:
    - None
    """
    db_users_info.insert_one(new_user)

async def update_one_user_token(to: dict, in_to: dict):
    """
    Updates a user's document in the 'users_info' collection.

    Parameters:
    - to (dict): A filter to identify the user document to update.
    - in_to (dict): The updates to apply to the user's document.

    Actions:
    - Updates the user document matching the filter with the specified updates.

    Returns:
    - None
    """
    db_users_info.update_one(to, in_to)

async def all_text_users():
    """
    Retrieves all documents from the 'text_user' collection.

    Parameters:
    - None

    Actions:
    - Fetches all documents from the 'text_user' collection.

    Returns:
    - pymongo.cursor.Cursor: A cursor to iterate over the documents in the collection.
    """
    return db_text_user.find()