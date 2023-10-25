def left_caesar(text, shift):
    decrypt_text = ""
    for character in text:
        if 'a' <= character <= 'z':
            new_index = (ord(character) - ord('a') - shift) % 26
            decrypted_character = chr(ord('a') + new_index)
            decrypt_text += decrypted_character
        else:
            decrypt_text += character
    return decrypt_text

def right_caesar(text, shift):
    encrypted_text = ""
    for character in text:
        if 'a' <= character <= 'z':
            new_index = (ord(character) - ord('a') + shift) % 26
            encrypted_character = chr(ord('a') + new_index)
            encrypted_text += encrypted_character
        else:
            encrypted_text += character
    return encrypted_text


def right_rotation(text):
    return text[-1:] + text[:-1]

def left_rotation(text):
    return text[1:] + text[:1]


ENCRYPTION_TYPES = [
    "rotation",
    "caesar"
]

ENCRYPTION_DIRECTIONS = ['left', 'right']