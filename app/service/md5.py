import hashlib


def calculate_md5(text: str):
    """
    Calculate the MD5 hash of the given text.

    Args:
        text (str): The text to calculate the MD5 hash for.

    Returns:
        MD5 hash.
    """
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    return md5_hash
