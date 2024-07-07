from sqlalchemy import UUID


def safe_str_to_uuid(uuid_str: str | None) -> UUID | None:
    """
    Safely convert a string to a UUID object, handling None and invalid UUID strings.

    Args:
        uuid_str (str | None): The string to be converted to UUID. Can be None.

    Returns:
        UUID | None: The UUID object if the string is a valid UUID, None otherwise.
    """
    if uuid_str is None or uuid_str.strip() == "":
        # Return None if the input is None or an empty/whitespace-only string
        return None

    try:
        # Attempt to create a UUID object from the string
        return UUID(uuid_str)
    except ValueError:
        # UUID string is not valid, return None
        return None
