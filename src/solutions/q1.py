import re

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


