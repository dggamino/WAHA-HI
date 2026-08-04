"""Hash utility functions."""
import hashlib, secrets, uuid
def generate_id(): return uuid.uuid4().hex
def hash_string(input_string, algorithm="sha256"):
    encoded = input_string.encode("utf-8")
    if algorithm == "sha256": return hashlib.sha256(encoded).hexdigest()
    elif algorithm == "sha512": return hashlib.sha512(encoded).hexdigest()
    elif algorithm == "md5": return hashlib.md5(encoded).hexdigest()
    else: raise ValueError(f"Unsupported hash algorithm: {algorithm}")
def generate_token(length=32): return secrets.token_hex(length // 2 + 1)[:length]
