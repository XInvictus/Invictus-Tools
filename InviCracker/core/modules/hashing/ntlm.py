import hashlib
def ntlm_hash(password):
    return hashlib.new("md4", password.encode("utf-16le")).digest()