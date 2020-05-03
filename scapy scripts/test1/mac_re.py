import re


def valid_mac(mac):
    return bool(re.fullmatch(r'^(([0-9a-fA-F]){2}:){5}([0-9a-fA-F]){2}$', mac))


def main():
    user_mac = input('enter mac in the format "aa:bb:cc:dd:ee:ff"\n')
    if valid_mac(user_mac):
        print(user_mac[:8].upper())


if __name__ == '__main__':
    main()
