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

def mirror_encrypt_word(word, extra_char):
    reversed_word = word[::-1]  # Reverse the word
    if word == reversed_word:  # If the reversed word is equal to the original word
        middle_index = len(word) // 2  # Find the middle of the word (divide by two and round)
        reversed_word = reversed_word[:middle_index] + extra_char + reversed_word[middle_index:]  # Add the extra char in the middle of the word
    return reversed_word

def mirror_decrypt_word(word, extra_char):
    if len(extra_char) != 0:  # If the extra char is present
        word = word.replace(extra_char, '')  # Remove the extra char
    reversed_word = word[::-1]  # Reverse the word
    return reversed_word

def mirror_encrypt_phrase(phrase, extra_char):
    words = phrase.split()  # Split the string of characters into a list
    reversed_phrase = ''  # Initialize the reversed phrase
    for word in words:  # For each word in the words list
        if word is None:  # If the for loop has completed its iteration
            return reversed_phrase
        word = mirror_encrypt_word(word, extra_char)  # Encrypt each word
        reversed_phrase = reversed_phrase + " " + word  # Assemble all the words
    reversed_phrase = reversed_phrase[1:]  # Remove the initial space
    return reversed_phrase

def mirror_decrypt_phrase(phrase, extra_char):
    words = phrase.split()
    reversed_phrase = ''
    for word in words:
        if word is None:
            return reversed_phrase
        word = mirror_decrypt_word(word, extra_char)
        reversed_phrase = reversed_phrase + " " + word
    reversed_phrase = reversed_phrase[1:]
    return reversed_phrase

ENCRYPTION_TYPES = [
    "rotation",
    "caesar",
    "mirror"
]

ENCRYPTION_DIRECTIONS = ['left', 'right']