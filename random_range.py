#!/usr/bin/env python3
import sys
import os
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
        # Number of lines in the wordlist file
        self.keyspace = sum(1 for line in open(self.words))
        # Initialise a RandomInRange object
        self.r = RandomInRange(1, self.keyspace)
        self.make_list()

    def make_list(self, n=None):
        """
        Randomly select words from a wordlist and append them to a list.
        Uses a modular range-reduced random number to make the selection
        without modulo bias.
        """
        n = n if n else self.n
        for i in range(0, n):
            r_num = self.r.random_number()
            self.random_words.append(self.get_one_line(r_num).decode('utf-8').rstrip())

    def get_one_line(self, line_number):
        """
        sed is a reasonable way to get a line from a file indexed by line number.
        If there is a more Pythonic way of doing this, please leave a comment.
        """
        return check_output([
            "sed",
            "-n",
            "%sp" % line_number,
            self.words
            ])

    def print_words(self):
        for w in self.random_words:
            print(w)

def main():
    r = RandomWords(24)
    r.print_words()

if __name__ == '__main__':
    main()