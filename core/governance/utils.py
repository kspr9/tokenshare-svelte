import logging
from typing import Dict, List

def validate_data(data: Dict[str, object], required_fields: List[str]) -> bool:
    """
    Validate that all required fields are present in the data.

    Parameters:
    - data (dict): The data dictionary to validate.
    - required_fields (list): A list of required field names.

    Returns:
    - bool: True if all validations pass, False otherwise.
    """
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
    return True

def log_error(message: str, context: Dict[str, object] = None) -> None:
    """
    Log an error message with optional context.

    Parameters:
    - message (str): The error message to log.
    - context (dict, optional): Additional context for the error.

    """
    logging.error(f"Error: {message}, Context: {context}")