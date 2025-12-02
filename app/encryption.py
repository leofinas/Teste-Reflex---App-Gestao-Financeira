import os
import logging
from cryptography.fernet import Fernet

_cipher = None
_using_temp_key = False


def _get_cipher() -> Fernet:
    global _cipher, _using_temp_key
    if _cipher is not None:
        return _cipher
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        if not _using_temp_key:
            logging.warning(
                "⚠️ ENCRYPTION_KEY not found in environment. Generating temporary key. Data will NOT persist after restart."
            )
        key = Fernet.generate_key()
        _using_temp_key = True
    elif isinstance(key, str):
        key = key.encode()
    try:
        _cipher = Fernet(key)
    except Exception as e:
        logging.exception(f"Invalid ENCRYPTION_KEY provided: {e}. Using temporary key.")
        _cipher = Fernet(Fernet.generate_key())
        _using_temp_key = True
    return _cipher


def is_using_temp_key() -> bool:
    """Check if the application is using a temporary encryption key."""
    _get_cipher()
    return _using_temp_key


def encrypt_value(value: float | int) -> str:
    """Encrypts a numeric value to a string."""
    try:
        cipher = _get_cipher()
        str_val = str(value)
        token = cipher.encrypt(str_val.encode())
        return token.decode("utf-8")
    except Exception as e:
        logging.exception(f"Error encrypting value: {e}")
        return str(value)


def decrypt_value(value: str | float | int) -> float:
    """Decrypts a value back to float."""
    if isinstance(value, (float, int)):
        return float(value)
    try:
        cipher = _get_cipher()
        token = value.encode("utf-8")
        decrypted_bytes = cipher.decrypt(token)
        decrypted_str = decrypted_bytes.decode("utf-8")
        return float(decrypted_str)
    except Exception as e:
        try:
            return float(value)
        except ValueError:
            logging.exception(f"Error decrypting value '{value}': {e}")
            return 0.0