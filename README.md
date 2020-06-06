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

This will introduce a bias if the maximum random number % keyspace is not equal to the keyspace - 1.

References
----------
* [Modulo Bias, stack overflow][2]

[1]: https://blog.webernetz.net/password-strengthentropy-characters-vs-words/
[2]: https://stackoverflow.com/questions/10984974/why-do-people-say-there-is-modulo-bias-when-using-a-random-number-generator
