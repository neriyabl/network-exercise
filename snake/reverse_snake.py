CESAR_DICTIONARY = {'s': 'L', 'b': 's', 'w': 'O', 'z': 'G', 'c': 'o', 'J': 'y',
                    'V': 't', 'P': 'w', 'B': 'f', 'Z': 'q', 'F': 'k', 'O': 'N',
                    'u': 'A', 'W': 'r', 'K': 'K', 'a': 'D', 'v': 'l', 'g': 'S',
                    'f': 'x', 'x': 'c', 'N': 'e', 'p': 'b', 'U': 'a', 'j': 'P',
                    'o': 'Q', 'i': 'I', 'M': 'd', 't': 'U', 'H': 'V', 'X': 'i',
                    'Y': 'T', 'R': 'H', 'h': 'X', 'L': 'z', 'G': 'F', 'A': 'W',
                    'm': 'n', 'T': 'u', 'l': 'B', 'C': 'Z', 'q': 'p', 'D': 'v',
                    'I': 'g', 'n': 'h', 'y': 'C', 'S': 'j', 'k': 'M', 'd': 'J',
                    'Q': 'E', 'e': 'Y', 'r': 'R', 'E': 'm'}


def decrypt_cesar(encrypted_txt):
    """
    decrypt every character with the reversed CESAR_DICTIONARY
    :param encrypted_txt: the encrypted text
    :return: decrypted text with the keys chars instead the values char in the dictionary
    """
    decrypted_dict = {value: key for (key, value) in CESAR_DICTIONARY.items()}
    return ''.join(decrypted_dict[char] if char in decrypted_dict else char for char in encrypted_txt)


def replace_digits(txt_with_digits):
    """
    replace all digits with space in the text
    :param txt_with_digits: the text with digits separators
    :return: the txt with space separator
    """
    return ''.join(' ' if char.isdigit() else char for char in txt_with_digits)


def reverse_words(input_txt):
    """
    reverse each word in the input text
    :param input_txt: text with space separator
    :return: string with reversed words from the input text
    """
    return ' '.join(word[::-1] for word in input_txt.split(' '))


def main():
    with open('snake.txt', 'r') as input_file:
        # read the text
        encrypted_string = input_file.read()

        # decrypt the cesar cipher
        cesar_decrypted_string = decrypt_cesar(encrypted_string)

        # replace all digits with spaces
        replaced_digits = replace_digits(cesar_decrypted_string)

        # reverse all words
        decrypted_string = reverse_words(replaced_digits)

    with open('snake.txt', 'w') as output_file:
        output_file.write(decrypted_string)
        print decrypted_string


if __name__ == '__main__':
    main()
