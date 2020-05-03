from string import digits, ascii_letters
import random

WORDS_DELIMETER = ' '
CESAR_DICTIONARY = {'s': 'L', 'b': 's', 'w': 'O', 'z': 'G', 'c': 'o', 'J': 'y',
                    'V': 't', 'P': 'w', 'B': 'f', 'Z': 'q', 'F': 'k', 'O': 'N',
                    'u': 'A', 'W': 'r', 'K': 'K', 'a': 'D', 'v': 'l', 'g': 'S',
                    'f': 'x', 'x': 'c', 'N': 'e', 'p': 'b', 'U': 'a', 'j': 'P',
                    'o': 'Q', 'i': 'I', 'M': 'd', 't': 'U', 'H': 'V', 'X': 'i',
                    'Y': 'T', 'R': 'H', 'h': 'X', 'L': 'z', 'G': 'F', 'A': 'W',
                    'm': 'n', 'T': 'u', 'l': 'B', 'C': 'Z', 'q': 'p', 'D': 'v',
                    'I': 'g', 'n': 'h', 'y': 'C', 'S': 'j', 'k': 'M', 'd': 'J',
                    'Q': 'E', 'e': 'Y', 'r': 'R', 'E': 'm'}

INPUT_TEXT = 'The Zen of Python\n' \
             'Beautiful is better than ugly.\n' \
             'Explicit is better than implicit.\n' \
             'Simple is better than complex.\n' \
             'Complex is better than complicated.\n' \
             'Flat is better than nested.\n' \
             'Sparse is better than dense.\n' \
             'Readability counts.\n' \
             'Special cases are not special enough to break the rules.\n' \
             'Although practicality beats purity.\n' \
             'Errors should never pass silently.\n' \
             'Unless explicitly silenced.\n' \
             'In the face of ambiguity, refuse the temptation to guess.\n' \
             'There should be one-- and preferably only one --obvious way to do it.\n' \
             'Although that way may not be obvious at first unless you are Dutch.\n' \
             'Now is better than never.\n' \
             'Although never is often better than *right* now.\n' \
             'If the implementation is hard to explain, it is a bad idea.\n' \
             'If the implementation is easy to explain, it may be a good idea.\n' \
             'Namespaces are one honking great idea -- lets do more of those!\n'


def reverse_every_word(input_string, delimeter=WORDS_DELIMETER):
    """ Example : Hello world -> olleH dlrow"""
    words = input_string.split(delimeter)
    return delimeter.join(word[::-1] for word in words)


def reverse_dictionary(dictionary):
    """ Given a dictionary - where no two values or keys are identical - create a reverse dictionary"""
    return {value: key for (key, value) in dictionary.items()}


def translate_string_with_dictionary(input_string, dictionary):
    """ Convert a string to another string using a dictionary"""
    return "".join([dictionary[x] if x in dictionary else x for x in input_string])


def replace_character_with_random_digit(input_string, character_to_replace=WORDS_DELIMETER):
    """ Any character which is the given delimeter is chnaged to a random digit"""
    return "".join(random.choice(digits) if x == character_to_replace else x for x in input_string)


def replace_digits_with_character(input_string, character_to_insert=WORDS_DELIMETER):
    """ Any character which is a number is changed to the given delimeter"""
    for digit in digits:
        input_string = input_string.replace(digit, character_to_insert)
    return input_string


def alternative_replace_digits_with_characters(input_string, character_to_insert=WORDS_DELIMETER):
    return "".join(character_to_insert if x in digits else x for x in input_string)


def encrypt(input_string):
    """ Encrypt message:
    1. Reverse every word
    2. Remove digits, use spaces
    3. Apply the dictionary on the text
    """
    encrypted_string = reverse_every_word(input_string)
    encrypted_string = replace_character_with_random_digit(encrypted_string)
    encrypted_string = translate_string_with_dictionary(encrypted_string, CESAR_DICTIONARY)
    return encrypted_string


def decrypt(encrypted_string):
    """ Decrypt in the reverse order of enctyption:
    1. Create the reverse dictionary
    2. Apply the dictionary on the text
    3. Remove digits, use spaces
    4. Reverse every word
    """
    decription_dictionary = reverse_dictionary(CESAR_DICTIONARY)
    decrypted_string = translate_string_with_dictionary(encrypted_string, decription_dictionary)
    decrypted_string = replace_digits_with_character(decrypted_string)
    decrypted_string = reverse_every_word(decrypted_string)
    return decrypted_string


def main():
    encrypted_string = encrypt(INPUT_TEXT)
    with open('snake.txt', 'wb') as output_file:
        for char in encrypted_string:
            output_file.write(char.encode())
    with open('snake.txt', 'rb') as input_file:
        encrypted_string = input_file.read()
    decrypted_string = decrypt(encrypted_string)
    print(decrypted_string)


if __name__ == '__main__':
    main()
