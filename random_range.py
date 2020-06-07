#!/usr/bin/env python3
import sys
import os
from subprocess import check_output

class RandomInRange:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
#        self.wordlist = list()
        self.set_parameters()
        self.set_config()


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
        
    def set_config(self):
        self.random_src_path = '/dev/urandom'
#        self.words = '/usr/share/dict/cracklib-small'

    def random_number(self):
        with open(self.random_src_path, 'rb') as file:
            while True:
                data = os.urandom(self.n_bytes)
                data = int.from_bytes(data, "big")
                if data < self.max_allowed:
                    break
        return (data % self.m) + self.lower

class RandomWords:
    def __init__(self, n):
        self.n = n
        self.wordlist = list()
        self.words = '/usr/share/dict/cracklib-small'
        self.keyspace = sum(1 for line in open(self.words))
        self.r = RandomInRange(1, self.keyspace)
        self.make_list()

    def make_list(self, n=None):
        n = n if n else self.n
        for i in range(0, n):
            r_num = self.r.random_number()
            self.wordlist.append(self.get_one_line(r_num).decode('utf-8').rstrip())

    def get_one_line(self, line_number):
            return check_output([
                "sed",
                "-n",
                "%sp" % line_number,
                self.words
                ])

    def print_words(self):
        for w in self.wordlist:
            print(w)


def main():
    r = RandomWords(24)
    r.print_words()

if __name__ == '__main__':
    main()
