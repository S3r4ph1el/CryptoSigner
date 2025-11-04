from typing import Optional
import random

def pad_message(message: bytes, block_size: int = 64) -> bytes:

    message_length = len(message) * 8  # length in bits
    padded_message = message + b'\x80'

    while (len(padded_message) * 8) % (block_size * 8) != (block_size * 8 - 64):
        padded_message += b'\x00'

    padded_message += message_length.to_bytes(8, 'big')

    return padded_message

def split_blocks(message: bytes, block_size: int = 64) -> list:
    return [message[i:i + block_size] for i in range(0, len(message), block_size)]

def initialize_hash_values(salt: Optional[bytes] = None) -> list:

    if salt is None:
        salt = random.randbytes(8)

    seed = int.from_bytes(salt, 'big', signed=False)
    rng = random.Random(seed)
    h1 = rng.getrandbits(64)
    h2 = rng.getrandbits(64)
    return [h1, h2], salt

def compression_function(block: bytes, state: list) -> list:

    h1, h2 = state
    for byte in block:
        h1 = (h1 + byte) & 0xFFFFFFFFFFFFFFFF  # Ensure 64-bit overflow
        h2 = (h2 ^ byte) & 0xFFFFFFFFFFFFFFFF
    return [h1, h2]

def sha64(message: bytes, salt: Optional[bytes] = None):

    padded_message = pad_message(message)
    blocks = split_blocks(padded_message)
    state, salt = initialize_hash_values(salt)

    for block in blocks:
        state = compression_function(block, state)

    final_hash = state[0].to_bytes(8, 'big') + state[1].to_bytes(8, 'big')
    return final_hash, salt