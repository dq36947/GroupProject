import re
from random import SystemRandom
from cryptography_functions import *
import string
import math

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



def caesar_shift(message: str, shift: int, decode: bool = False) -> str:
    """
    Performs a caesar shift on the string.
    
    Args:
        message: string to encode/decode
        shift: how many positions to move
        decode: flag to determine if we are encoding or decoding with the shift
    
    Returns:
        encoded/decoded string
    """

    message = normalise_string(message)

    # for decoding, just use a negative shift
    shift = -shift if decode else shift

    new_chars = []
    # shift every char
    for char in message:
        if not (char.isalpha() and char.isascii()):
            new_chars.append(char)
            continue

        shifted = shift_char(char, shift)
        new_chars.append(shifted)


    return "".join(new_chars)

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


######## Q3 HELPERS ##############

def vigenere_key_generator(length):
    rng = SystemRandom()
    return "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))

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


###### Q4 ##########

# class Letter:
#     """stores information about the letter, including encoding"""
#     def __init__(self, letter: str, bigram_count: int) -> None:
#         self.letter = letter
#         self.bigram_count = bigram_count

#     @property
#     def letter(self) -> str:
#         return self._letter

#     @letter.setter
#     def letter(self, value: str) -> None:
#         if not isinstance(value, str):
#             raise TypeError(f"letter must be a str, not {type(value).__name__}")
#         if len(value) != 1 or not value.isalpha():
#             raise ValueError(f"letter must be a single alphabetic character, got {value!r}")
#         self._letter = value

#     def mask_to_bigrams(self, available_bigrams: list[str], proportion: float) -> list[str]:
#         """Masks the letter to a random "number of bigrams based on frequency"""
#         n = math.floor(self.bigram_count * proportion)

#         # chose n bigrams from the available ones randomly
#         chosen_bigrams = []


        
def allocate_bigram_counts(bigram_count: int) -> dict[str, int]:
    """Randomly allocates a number of bigrams to each letter in the alphabet, based on frequency"""  
    proportions_list = [0.08037039814236689, 0.015117150118007613, 0.024395416696672795, 0.044492718223755896, 0.12465622874050229, 0.021875149257295695, 0.020489794079994735, 0.0659013804304599, 0.06877652449081763, 0.0011344173156033607, 0.00789018919576395, 0.040189653589438434, 0.0248324544321343, 0.07166824925801336, 0.07463644325525305, 0.01773789169135831, 0.0011260032255661632, 0.05811859461928841, 0.06489490677806922, 0.0901250507010793, 0.02645191929105847, 0.010320376377095758, 0.02331717580572955, 0.0015897680705575894, 0.01890448052769213, 0.0009876656864251773]
    letter_proportions = dict(zip(string.ascii_lowercase, proportions_list))

    # ensure each letter gets at least 1, so -26 from bigram_count
    bigram_count -= 26
    total = 0

    allocation = {}
    for letter, freq in letter_proportions.items():
        count = 1 + math.floor(bigram_count * freq)
        allocation[letter] = count
        total+=count

    # flooring will remove some from the count, randomly add back in the leftover
    leftover = bigram_count + 26 - total
    rng = SystemRandom()
    for _ in range(leftover):
        selected_letter = rng.choice(string.ascii_lowercase)
        current_count = allocation.get(selected_letter, 1)
        allocation[selected_letter] = current_count + 1

    return allocation


def random_bigrams(n: int) -> set[str]:
    """Randomly creates a list of n bigrams excluding aa, bb ect"""
    rng = SystemRandom()

    # cap n to 650
    n = min(n, 650)

    # faster to remove from full set rather than build from nothing
    all_bigrams =  [f"{a}{b}" 
           for a in string.ascii_lowercase
           for b in string.ascii_lowercase
           if a!=b]

    # pick n from all possible bigrams
    chosen_bigrams = rng.sample(all_bigrams, n)
    return set(chosen_bigrams)



def create_bigram_masks(bigram_count: int) -> dict[str, set[str]]:
    """Chooses a list of bigrams for each letter and returns it as a dict"""

    counts = allocate_bigram_counts(bigram_count)
    available_bigrams = random_bigrams(bigram_count)

    masks = {}
    rng = SystemRandom()

    for letter, count in zip(string.ascii_lowercase, counts.values()):
        chosen_bigrams = set(rng.sample(sorted(available_bigrams), count))
        available_bigrams -= chosen_bigrams

        masks[letter] = chosen_bigrams

    
    return masks

def mask_string_bigrams(message: str, bigrams: dict[str, set[str]]) -> str:
    """Masks the given message by randomgly using the bigrams. Preserves case."""
    rng = SystemRandom()

    masked_string = []
    for char in message:
        bigram_masks = bigrams.get(char.lower(), set())

        # sorted needed for choice to handle sets
        mask = rng.choice(sorted(bigram_masks))
        
        if char == char.upper():
            masked_string.append(mask.upper())
        else: 
            masked_string.append(mask)

    return "".join(masked_string)

def unmask_string_bigrams(message: str, bigrams: dict[str, set[str]]) -> str:
    """Unapplies the bigram effect on the messsage"""
    unmasked_string = []
    # reversed_bigrams = {bigramset: letter for letter, bigramset in bigrams.values()}

    for i in range(0, len(message), 2):
        bigr = message[i: i+2]

        # loop over bigrams to get the corresponding letter
        for letter, masks in bigrams.items():
            if bigr.lower() in masks:
                cased_letter = letter.upper() if bigr == bigr.upper() else letter
                unmasked_string.append(cased_letter)

    return "".join(unmasked_string)


def create_hybrid_key(vigerene_key: str, bigrams: dict[str, set[str]]) -> str:
    """
    Puts the vigerene key and bigram information into 1 string.
    The bigrams are appended to the end of the key in a special format
    """

    def set_to_string(s: set[str]) -> str:
        """Custom encoding of a set to a string"""
        body = ",".join(s)
        return f"|{body}|"


    delimiter = ";"
    body = []
    for letter, masks in bigrams.items():
        mask_string = set_to_string(masks)
        body.append(f"{letter}:{mask_string}")

    ending_string = f"&{delimiter.join(body)}"
    return f"{vigerene_key}{ending_string}"

def read_hybrid_key(key: str) -> tuple[str, dict[str, set[str]]]:
    """Reads the hybrid key to a vigerne key and a python dict"""

    def string_to_set(encoded: str) -> set[str]:
        match = SET_PATTERN.match(encoded)
        if match is None:
            raise ValueError(f"Not a valid encoded set: {encoded}")
        body = match.group(1)
        return set(body.split(",")) if body else set()

    parts = key.split("&")

    SET_PATTERN = re.compile(r"^\|([^|]*)\|$")
    
    constructed_mappings = {}

    plaintext_dict = parts[1].split(";")
    for pair in plaintext_dict:
        letter, mask_string = pair.split(":")
        masks = string_to_set(mask_string)
        constructed_mappings[letter] = masks

    return (parts[0], constructed_mappings)

    
