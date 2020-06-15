#!/usr/bin/env python3
import sys
import os
import re
import argparse
from subprocess import check_output

class RandomInRange:
    """
    Class that provides a pseudo-random number within a given range,
    corrected for modulo bias.
    """
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.random_src_path = '/dev/urandom'
        self.set_parameters()

    def set_parameters(self):
        max_bytes = {
            1: (1 <<  8) - 1,
            2: (1 << 16) - 1,
            3: (1 << 24) - 1,
            4: (1 << 32) - 1
            }
        
        # Compute modulus m that will be used to restrict range
        self.m = self.upper - self.lower + 1
        try:
            assert(self.m < max_bytes[4]), "Max value exceeded."
        except AssertionError as error:
            print(error)
            print("The range magnitude {} is too large.".format(self.m)) 
            sys.exit(1)

        # Determine number of pseudo random bytes needed and the related max random value
        for i in range(1, 4):
            if self.m <= max_bytes[i]:
                self.n_bytes = i
                self.max_random = max_bytes[i]
                break

        self.excess = (self.max_random % self.m) + 1
        self.max_allowed = self.max_random - self.excess
        
    def random_number(self):
        while True:
            data = os.urandom(self.n_bytes)
            data = int.from_bytes(data, "big")
            if data < self.max_allowed:
                break
        return (data % self.m) + self.lower


class RandomWords:
    """
    Class that builds a list of randomly-selected words.
    """
    def __init__(self, n):
        # Number of words
        self.n = n
        # Initialise an empty list for the randomly selected words
        self.random_words = list()
        # The word list to select from (Ubuntu/Debian)
        self.words = '/usr/share/dict/cracklib-small'
        # Dictionary has many duplicate words with apostrophes - ignore by applying the following regex rule
        self.allowed_chars = re.compile('[A-Za-z]+')
        # Number of lines in the wordlist file
        self.keyspace = sum(1 for line in open(self.words) if self.allowed_chars.fullmatch(line.rstrip()))
        
        # Initialise a RandomInRange object
        self.r = RandomInRange(1, self.keyspace)
        self.make_list()
        self.compute_entropy()

    def make_list(self, n=None):
        """
        Randomly select words from a wordlist and append them to a list.
        Uses a modular range-reduced random number to make the selection
        without modulo bias.
        """
        n = n if n else self.n
        for i in range(0, n):
            r_num = self.r.random_number()
            self.random_words.append(self.get_one_line(r_num).rstrip())

    def get_one_line_sed(self, line_number):
        """
        sed is a reasonable way to get a line from a file indexed by line number.
        If this method is used, you need to decode the bytes object to a string.
        """
        return check_output([
            "sed",
            "-n",
            "%sp" % line_number,
            self.words
            ])

    def get_one_line(self, target_line_number):
        """
        Loop through the dictionary file to get the target line number, disregarding lines that contain
        anything other than the allowed character set.
        """
        with open(self.words) as fp:
            line_number = 0
            for line in fp:
                if self.allowed_chars.fullmatch(line.rstrip()):
                    line_number += 1
                    if line_number == target_line_number: break
        return line

    def compute_entropy(self):
        import math
        r = math.log(self.keyspace ** self.n, 2)
        self.entropy = round(r, 2)

    def print_words(self):
        for i, w in enumerate(self.random_words, start=1):
            print("{}:\t{}".format(i, w))
        print("Entropy: {}".format(self.entropy))

def main(n):
    r = RandomWords(n)
    r.print_words()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="The number of random words to generate", type=int, nargs='?', default=None)
    n = parser.parse_args().n
    n = n if n is not None else int(input("Enter n: "))
    main(n)
