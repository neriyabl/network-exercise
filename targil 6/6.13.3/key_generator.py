import random


def key_generator(keys_len, key_len):
    keys = []
    for i in range(keys_len):
        key = set()
        while len(key) < key_len:
            key.add(random.randint(48, 122))
        key_lst = [chr(num) for num in key]
        random.shuffle(key_lst)
        random.shuffle(key_lst)
        print(''.join(key_lst))

        keys += [''.join(key_lst)]
    return keys


if __name__ == '__main__':
    print(key_generator(7, 32))
