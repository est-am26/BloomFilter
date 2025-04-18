# Bloom Filter Implementation

This project implements a Bloom Filter in Python for storing and querying membership of English words. It uses a Bit Vector, multiple hash functions, and supports estimation of theoretical and measured false positive rates.

## Features

- Supports configurable number of expected keys, hash functions, and target false positive rate.
- Inserts and queries words from `wordlist.txt` (~225,000 English words).
- Validates no false negatives for inserted items.
- Computes actual false positive rate using non-inserted items.
