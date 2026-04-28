---
title: "The Accidental Ancestor — How a Computer for Verifying Numbers Shaped Modern Hashing"
date: 2026-04-28
---

1954, Hans Peter Luhn filed for a US patent on a Computer for Verifying Numbers. This is one of the earliest examples of using mathematical transformations to verify data integrity, a 
concept that became a foundation for modern hashes. Today you can find it under names Luhn Algorithm, Luhn Formula or Modulus 10 Algorithm.

### How does this algorithm work?

Imagine you have a number. Let's take 
```
3846205
```
### Step 1. 

Find a substitution digit.

To do that multiply the original digit by two. If  result is 10 or bigger, add the digits. A substitution for the first digit from our example would be
```
3*2 = 6,
```
but if the original number was 7, its substitution would be
```
7*2 = 14 = 1+4 = 5
```
### Step 2.  

Starting from the first digit on the right and moving left, replace every other digit with its substitution. Later the check digit will be appended in its original form on the rightmost position. This way we can avoid unnecessary calculations, as we won't have to calculate its substitution.
```
3846205 -> 6886401
```
### Step 3.

Determine a check digit. 

To do that add all the digits from the number from step 2. Take modulo 10 of this sum and subtract it from 10. That's your check digit.

In our example, check digit is 7:
```
6+8+8+6+4+0+1 = 33 mod 10 = 3
10-3 = 7
```
*In the original paper Luhn performs modulo 10 operation each time the addition happens*
```
(6+8) mod 10 = 4
(4+8) mod 10 = 2
etc
```
*However, it gives the same result* 

### Step 4.

Append this check digit to the rightmost position of the number from step 2.

```
68864017
```
### And how does verifying work?

To verify the number perform a step 2 on the original number that already includes the check digit. Add all the digits. Take modulo 10 of this sum. The result should equal zero.
```
Original number with a check digit: 75689034
With substitutions: 55389064

Verification: 5+5+3+8+9+0+6+4 = 40 mod 10 = 0
```
Otherwise the number is invalid. For example if instead of 6 in the original number we accidentally type 7, the result of verification will be:
```
 5+5+5+8+9+0+6+4 = 42 mod 10 = 2
```
### Does it really work for all the numbers?

Almost. Luhn Algorithm can catch all the single digit errors. Let's take a look at this table that shows all 10 possible digits and their substitution:

| Original digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Substitution | 0 | 2 | 4 | 6 | 8 | 1 | 3 | 5 | 7 | 9 |

We can see, that the second row is just a permutation of the first one. This means that every original digit gets assigned its unique substitution and therefore each mistype will result in a changed checksum. For example:
```
Original digits: 2 6
Substitutions: 4 6
Original sum: 10

Mistype digits: 3 6
Substitutions: 6 6
Malicious sum: 12

```
Luhn Algorithm can also catch all the transposition of neighboring digits errors, except for the transposition of 09 or 90, because as we can see from the table above, their substitutions equal the original values.

### So is it a cryptographically secured hash function?

No. Luhn Algorithm was created to protect against accidental errors, not malicious attacks. For example, it can't detect two digit errors, as many of them result in an unchanged sum:
```
Original digits: 2 6
Substitutions: 4 6
Original sum: 10

Malicious digits: 6 7
Substitutions: 3 7
Malicious sum: 10
```
That's why nowadays, numbers that require verification, like your credit card number or your id number, use additional security or better protected algorithms.

### Further notes

A year before, in 1953 Luhn introduced the concept that would later serve as a foundation for the hash tables. In the internal IBM memo, he introduces the idea of using math to organize data into searchable buckets, which is basically what we call hash tables nowadays. 

As it was an internal IBM memo, it doesn't have any public access, therefore all the information can be taken only from the secondary source, an [IEEE Spectrum article](https://spectrum.ieee.org/hans-peter-luhn-and-the-birth-of-the-hashing-algorithm). Rather than repeat it here, I'd recommend reading the [IEEE Spectrum article](https://spectrum.ieee.org/hans-peter-luhn-and-the-birth-of-the-hashing-algorithm) directly. It explains the idea with a clear telephone number database example.

The mathematics behind Luhn's concept for such information storage had to be modified later to improve transformation, guarantee even distribution and minimize collisions. [Rabin-Karp algorithm](https://0xkrt26.github.io/math_behind_security/2026/04/25/searching-smarter-rolling-hashes.html) that I've already written about provides some solutions to these problems. 

### My sources and further readings: 
[IEEE Article about Hans Peter Luhn](https://spectrum.ieee.org/hans-peter-luhn-and-the-birth-of-the-hashing-algorithm) 
[Luhn's Patent on a Computer for Verifying Numbers](https://docs.google.com/viewer?url=patentimages.storage.googleapis.com/pdfs/US2950048.pdf)
[Luhn "A new method of recording and searching information"](https://fermatslibrary.com/s/a-new-method-of-recording-and-searching-information)
