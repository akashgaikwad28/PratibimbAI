from cryptography.fernet import Fernet
from app.core.config import settings

# Security Versioning (Task 6)
# Allows for future key rotation or algorithm changes
VERSION = "v1"

def _get_cipher() -> Fernet:
    if not settings.API_KEY_ENCRYPTION_SECRET:
        raise RuntimeError("API_KEY_ENCRYPTION_SECRET is not set.")
    return Fernet(settings.API_KEY_ENCRYPTION_SECRET.encode())


def encrypt_api_key(plaintext: str) -> str:
    """
    Encrypts a plaintext string and prefixes it with the current security version.
    """
    encrypted = _get_cipher().encrypt(plaintext.encode()).decode()
    return f"{VERSION}:{encrypted}"


def decrypt_api_key(ciphertext: str) -> str:
    """
    Decrypts a versioned ciphertext.
    """
    if ":" not in ciphertext:
        # Legacy support for unversioned keys (initial transition)
        return _get_cipher().decrypt(ciphertext.encode()).decode()
    
    version, actual_ciphertext = ciphertext.split(":", 1)
    
    if version == "v1":
        return _get_cipher().decrypt(actual_ciphertext.encode()).decode()
    
    raise ValueError(f"Unsupported encryption version: {version}")
