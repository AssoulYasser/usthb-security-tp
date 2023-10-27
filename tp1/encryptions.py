import string
import random

def caesar_encrypt(text, shift, direction):
    if ((shift% 26)==0): 
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
    if ((shift% 26)==0): 
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

def right_rotation(text):
    return text[-1:] + text[:-1]

def left_rotation(text):
    return text[1:] + text[:1]

def generate_random_string():
    length = random.randint(1, 10)
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits  # You can customize this based on your requirements

    # Use random.choices to generate a random string of the desired length
    random_string = ''.join(random.choices(characters, k=length))

    return random_string

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

def mirror_encrypt_phrase(phrase):
    extra_char = generate_random_string()
    words = phrase.split()  # Split the string of characters into a list
    reversed_phrase = ''  # Initialize the reversed phrase
    for word in words:  # For each word in the words list
        if word is None:  # If the for loop has completed its iteration
            return reversed_phrase
        word = mirror_encrypt_word(word, extra_char)  # Encrypt each word
        reversed_phrase = reversed_phrase + " " + word  # Assemble all the words
    reversed_phrase = reversed_phrase[1:]  # Remove the initial space
    return {"encrypted_data":reversed_phrase, "extra_char": extra_char}

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