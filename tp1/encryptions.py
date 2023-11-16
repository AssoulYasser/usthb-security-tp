import string
import random

def pgcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_encryption(text, a, b):
    m = 26  
    a_inverse = mod_inverse(a, m)
    if a_inverse is None:
        raise ValueError("The 'a' key has no modular inverse in Z26. Choose another key 'a'.")
    encrypted_text = ""
    for character in text:
        if character.isalpha():
            if character.islower():
                offset = ord('a')
            else:
                offset = ord('A')
            x = ord(character) - offset
            x_encrypted = (a * x + b) % 26
            character_encrypted = chr(x_encrypted + offset)
            encrypted_text += character_encrypted
        else:
            encrypted_text += character
    return encrypted_text

def affine_decryption(encrypted_text, a, b):
    m = 26  
    a_inverse = mod_inverse(a, m)
    if a_inverse is None:
        raise ValueError("The 'a' key has no modular inverse in Z26. Choose another key 'a'.")
    decrypted_text = ""
    for character in encrypted_text:
        if character.isalpha():
            if character.islower():
                offset = ord('a')
            else:
                offset = ord('A')
            y = ord(character) - offset
            y_decrypted = (a_inverse * (y - b)) % 26
            character_decrypted = chr(y_decrypted + offset)
            decrypted_text += character_decrypted
        else:
            decrypted_text += character
    return decrypted_text

def caesar_encrypt(text, shift, direction):
    if (shift == 0):
        shift = 5
    elif ((shift% 26)==0): 
        shift = 25
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                if(direction == 'right'):
                     encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                elif(direction == 'left'): 
                    encrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            elif char.islower():
                if(direction == 'right'):
                    encrypted_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
                elif(direction == 'left'): 
                    encrypted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
        else:
            encrypted_char = char  # Conserve les caractères spéciaux inchangés
        encrypted_text += encrypted_char
    return encrypted_text

def caesar_decrypt(encrypted_text, shift,direction):
    if (shift == 0):
        shift = 5
    elif ((shift% 26)==0): 
        shift = 25
    decrypted_text = ""
    for char in encrypted_text:
        if char.isalpha():
            if char.isupper():
                if(direction == 'right'):
                    decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
                elif(direction == 'left'): 
                    decrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            elif char.islower():
                if(direction == 'right'):
                    decrypted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
                elif(direction == 'left'): 
                    decrypted_char = chr(((ord(char) -ord('a') + shift) % 26) +ord('a'))
        else:
            decrypted_char = char  # Conserve les caractères spéciaux inchangés
        decrypted_text += decrypted_char
    return decrypted_text

def cryptage_rotation(sentence,direction):
    words = sentence.split()  # Split the sentence into words
    rotated_words = []

    for word in words:

            if(direction == 'left'):
                rotated_word = word[1:] + word[:1]  # Left rotation
                rotated_words.append(rotated_word)
            elif(direction == 'right'): 
                rotated_word = word[-1:] + word[:-1] # right rotation
                rotated_words.append(rotated_word)

    rotated_sentence = " ".join(rotated_words)
    return rotated_sentence

def decryptage_rotation(sentence, direction):
    words = sentence.split()  # Split the sentence into words
    rotated_words = []

    for word in words:
  
            if(direction == 'left'):
                rotated_word = word[-1:] + word[:-1] # right rotation
                rotated_words.append(rotated_word)
                
            elif(direction == 'right'):
                rotated_word = word[1:] + word[:1]  # Left rotation
                rotated_words.append(rotated_word)
    rotated_sentence = " ".join(rotated_words)
    return rotated_sentence

def mirror_encrypt_phrase(phrase, extra_char):
    string = phrase

    new_string = string[::-1]

    if(new_string == string):
        length = int(len(string) / 2)
        new_string = string[:length] + extra_char + string[length:]

    return new_string

def mirror_decrypt_phrase(phrase, extra_char):
    return phrase[::-1] if extra_char not in phrase else phrase.replace(extra_char, '')[::-1]

ENCRYPTION_TYPES = [
    "rotation",
    "caesar",
    "mirror",
    "affine"
]

ENCRYPTION_DIRECTIONS = ['left', 'right']