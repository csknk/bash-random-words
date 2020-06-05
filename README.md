# Generate Random Words
Bash project for Linux.

Generate a set of pseudo-random words.

1. The user is prompted for the number of words required.
2. Words are obtained by using a random value sourced from `/dev/urandom`
3. The entropy of the pseudo-random words is computed
4. Results are output on stdout.

Issues
------
The index value is computed by taking the remainder of the random number modulo the size of the keyspace (i.e. the number of words selected from).

This will introduce a bias if the maximum random number % keyspace is not equal to the keyspace - 1.


@TODO: fix this. 


[1]: ihttps://blog.webernetz.net/password-strengthentropy-characters-vs-words/
