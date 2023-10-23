def left_shift(text, shift):
    decrypt_text = ""
    for character in text:
        if 'a' <= character <= 'z':
            new_index = (ord(character) - ord('a') - shift) % 26
            decrypted_character = chr(ord('a') + new_index)
            decrypt_text += decrypted_character
        else:
            decrypt_text += character
    return decrypt_text

def right_shift(text, shift):
    encrypted_text = ""
    for character in text:
        if 'a' <= character <= 'z':
            new_index = (ord(character) - ord('a') + shift) % 26
            encrypted_character = chr(ord('a') + new_index)
            encrypted_text += encrypted_character
        else:
            encrypted_text += character
    return encrypted_text


def right_rotation(text, shift):
    shift = shift % len(text)
    return text[-shift:] + text[:-shift]

def left_rotation(text, shift):
    shift = shift % len(text)
    return text[shift:] + text[:shift]


ENCRYPTION_TYPES = {
    "1": {
        "name":"left_shift",
        "encryption":left_shift,
        "decryption":right_shift
    },
    "2": {
        "name":"right_shift",
        "encryption":right_shift,
        "decryption":left_shift
    },
    "3": {
        "name":"left_rotation",
        "encryption":left_rotation,
        "decryption":right_rotation
    },
    "4": {
        "name":"right_rotation",
        "encryption":right_rotation,
        "decryption":left_rotation
    },
}

