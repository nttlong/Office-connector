import json
from hashlib import sha256


def hash_chunk(data: bytes) -> str:
    """
  Calculates the SHA256 hash of a byte chunk.

  Args:
      data: The byte chunk to hash.

  Returns:
      The SHA256 hash as a hexadecimal string.
  """
    hasher = sha256()
    hasher.update(data)
    return hasher.hexdigest()

def has_dict(data:dict)->str:
    json_txt = json.dumps(data)
    hasher = sha256()
    hasher.update(json_txt.encode('utf8'))
    return hasher.hexdigest()