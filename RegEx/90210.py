import re

PATTERN_250_255 = r'25[0-5]'
PATTERN_200_249 = r'2[0-4][0-9]'
PATTERN_100_199 = r'1[0-9][0-9]'
PATTERN_0_99 = r'[1-9]?[0-9]'


def main():
    with open('90210.txt', 'rb') as in_file:
        pattern_range = r'({}|{}|{}|{})'.format(PATTERN_250_255, PATTERN_200_249, PATTERN_100_199, PATTERN_0_99)
        ips = re.findall(r'{0}\.{0}\.{0}\.{0}'.format(pattern_range), in_file.read().decode())
    print('\n'.join('.'.join(ip) for ip in ips))


if __name__ == '__main__':
    main()
