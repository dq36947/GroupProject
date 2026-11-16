import string
import re
from random import SystemRandom

# need cryptography_functions.py locally
from cryptography_functions import *

###############################################
# Helpers from earlier, pasted for completeness
###############################################

def get_char_index(char: str) -> int:
    """Returns the index of the letter. Case-insensitive. Indexed a=0"""
    if len(char) != 1:
        raise ValueError("Use length 1 strings")
    
    # ord returns ascii index of char, a=97 ect so subtract 65
    return ord(char.lower()) - 97

def get_char_from_index(index: int, upper: bool = False) -> str:
    """Returns the letter given index, preserving uppercase if required. Indexed a=A=0"""
    # uppercase starts with ascii A=65, lower with a=97
    shift = 65 if upper else 97
    return chr(index + shift)


def normalise_string(text: str) -> str:
    """Uses regex to remove non-alphabetic chars"""
    return re.sub(r"[^a-zA-Z]", "", text)

def shift_char(char: str, shift: int) -> str:
    """Shifts a char by shift places and returns the new char"""
    current_index = get_char_index(char)
    new_index = (current_index + shift) % 26
    return get_char_from_index(new_index, char.isupper())


def vigenere(message: str, key: str, decode: bool = False) -> str:
    """
    Uses the vigerene cypher on the message.
    
    Args:
        message: string to encode/decode
        key: key to use
        decode: flag to determine if we are encoding or decoding with the shift
    
    Returns:
        encoded/decoded string
    """
    message = normalise_string(message)

    # get the shifts from the key
    if not decode:
        shifts = [get_char_index(char) for char in key]
    else:
        shifts = [-get_char_index(char) for char in key]
    

    new_chars = []
    for i, char in enumerate(message):
        shift_index = i % len(shifts)
        new_chars.append(shift_char(char, shifts[shift_index]))

    return "".join(new_chars)






########################################
# Q3
########################################


def vigenere_key_generator(length):
    rng = SystemRandom()
    return "".join(rng.choice(string.ascii_uppercase) for _ in range(length))

def slice_key(key: str) -> list[str]:
    """Slices the key into manageably small chunks"""
    # can change this later, 16 feels good for now 
    max_chunk_length = 16
    parts = []
    for i in range(0, len(key), max_chunk_length):
        parts.append(key[i: i + max_chunk_length])

    return parts

def encrypt_rsa(key: str, pk: tuple[int, int]) -> list[int]:
    """Slices the key, converts it to ints and returns encrypted ints"""
    n, e = pk
    parts = slice_key(key)
    int_parts = [convert_to_integer(p) for p in parts]

    encrypted = [pow(m, e, n) for m in int_parts]
    return encrypted

def decrypt_rsa(encrypted: list[int], pk: tuple[int, int], sk: int) -> list[int]:
    """Returns list of decrypted ints"""
    n, e = pk
    decrypted = [pow(c, sk, n) for c in encrypted]
    return decrypted



####################
# keys and message
####################

ALICE_KEYS = dict(zip(["pk", "sk", "factors"], RSA_key_generator()))
BOB_MESSAGE = "The Quick Brown Fox Jumps Over The Lazy Dog"
VIGENERE_KEY = vigenere_key_generator(20)

print(f"Using key\n{VIGENERE_KEY}\n")


### BOB ###
normed = normalise_string(BOB_MESSAGE)

message_encoded = vigenere(normed, VIGENERE_KEY)
print(f"Vigerene encrypted message:\n{message_encoded}\n")

# Bob uses Alice's public key to encode the vigerene key
encrypted_key = encrypt_rsa(VIGENERE_KEY, ALICE_KEYS.get("pk"))

#### Pretend Bob sends message_encoded and encrypted_key to Alice ####

### ALICE ###

# alice decrypts the key and converts it to text
decrypted_key = decrypt_rsa(encrypted_key, ALICE_KEYS.get("pk"), ALICE_KEYS.get("sk"))
recovered_key = "".join(convert_to_text(m) for m in decrypted_key)

# decode with vigenere
message_decoded = vigenere(message_encoded, recovered_key, decode=True)

print(f"Alice got the message:\n{message_decoded}")
