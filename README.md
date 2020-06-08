# Generate Random Words
Bash project for Linux.

Generate a set of pseudo-random words.

1. The user is prompted for the number of words required.
2. Words are obtained by using a random value sourced from `/dev/urandom`
3. The entropy of the pseudo-random words is computed
4. Results are output on stdout.

Correct for Modulo Bias
-----------------------
The index value used to select a word from the wordlist pseudo-randomly is computed by taking the remainder of the random number modulo the size of the keyspace (i.e. the number of words selected from).

This will introduce a bias if the maximum random number + 1 (mod keyspace) is not congruent to zero.

We correct for this by calculating the maximum random value that fulfills these requirements, and discarding any random numbers that exceed this.

Once we have a random number free from modulo bias, this is used to index a line number in the wordlist.

Wordlist
--------
This project is for Ubuntu, which ships with a wordlist file `/usr/share/dict/cracklib-small`.

I have ignored all lines in this file that do not contain characters `[A-Za-z]` in order to discount words with apostrophes and numbers. This still provides 49138 words.

For a 24 word selection, this provides an entropy of 374.

For a 12 word passphrase, entropy is 187.

I suspect this level of entropy is massive overkill.

References
----------
* [Modulo Bias, stack overflow][2]

[1]: https://blog.webernetz.net/password-strengthentropy-characters-vs-words/
[2]: https://stackoverflow.com/questions/10984974/why-do-people-say-there-is-modulo-bias-when-using-a-random-number-generator
