---
title: "Searching smarter - Plagiarism Detection with Rolling Hashes"
date: 2026-04-25
---

1987 Michael O. Rabin and Richard M. Karp introduced rolling hashes and polynomial hashing — concepts that reappear throughout modern cryptography and are widely used for plagiarism detection.

### How does it work?

This is what polynomial hash looks like:
```
	H=c1*b^(n-1)+c2*b^(n-2)+...cn*b^(0) mod p,
		where cn = character n of the plaintext
		n = number of characters in the plaintext
		p = suitable prime number
		b = base of the code system (256 etc)
```
*Note: if we leave mod p away, we'll be left with the same algorithm we use to convert numbers for example  from binary to decimal system (for binary b = 2).*

### But why calculating hash function when we can just straight ahead compare characters?

This is a legitimate way to compare strings called a naive string comparison, but i wouldn't recommend it for large texts. It will be too long and not as elegant as Rabin-Karp algorithm. Take a look yourself: imagine you have a string out of 17 letters, for example "abbrabraarbababra", and you need to write a program that will find how many times in this string there's a 3-letter combination "abr". If you use a naive string comparison you'll probably write something like this:
```
	text = "abbrabraarbababra"
	pattern = "abr"

	for each character i in the text:
    	    if text[i] == 'a':
        	if text[i+1] == 'b':
           	    if text[i+2] == 'r':
               		print "found at position", i
```
This algorithm checks every single character, some of them even multiple times.

Now Rabin-Karp algorithm uses what's called rolling hash function that is much faster and more efficient than the naive comparison.

### What makes Rolling Hash function faster?

It works pretty simply. Instead of calculating a hash function for each triple from scratch, Rolling hash function calculates the next hash value with old hash value using this formula:
```
	Hnew = (b*(Hold -c1*b^(n-1))+cnew) mod p,
```
which basically removes first character of the triple and adds the next one.

### Is Rabin-Karp algorithm always efficient?

Unfortunately no. But good news: even in the worst case scenario, where all calculated hashes are identical, the efficiency will be the same as by naive comparison. So it's definitely worth trying.

### Wait, why would hashes be identical? Aren't they all unique?

While it's our goal to make hashes unique and do our best to avoid collisions, some poorly chosen variables can still lead to the pigeonhole principle (it's a fancy name for having collisions, you can read more about it here:  https://math.mit.edu/~fgotti/docs/Courses/C.%20Combinatorial%20Analysis/1.%20Pigeonhole%20Principle/Pigeonhole%20Principle.pdf). That's why even after hash values match, Rabin-Karp algorithm still compares string values to exclude collisions.

### But why do collisions happen?

To answer this question, let's take a look at polynomial hash again. We have two variables that are chosen independently from the plaintext: b and p. 

### Oh, so collisions happen because b is too small? 

Not exactly, the number of collisions (preferably their absence) depends primarily on the chosen p value. The larger p is the less collisions we'll get. Why? Let's imagine:
```
	p = 7,

		then 1 mod 7 = 1
		2 mod 7 = 2
		3 mod 7 = 3
		...
		6 mod 7 = 6
		7 mod 7 = 0
	
		and...
		all over again: 8 mod 7 = 1
				9 mod 7 = 2
				etc.
```
Which gives us only seven unique values. Now if we took p = 23, we would have had 23 unique values. And so on. The bigger prime number we take, the less likely we will have repetitions. But also keep in mind that it shouldn't be too big, otherwise it can lead to performance issues.


### Why does p have to be a prime number? 

It doesn't have to, but it again reduces collisions. Imagine p as a number of baskets we can put our numbers in. If we take p=12, then we have 12 baskets. At first, if we do the same modulo operations we did for p=7 in the previous example, we'll end up with the same distribution. But in real life numbers usually don't come in as a perfectly sorted row. Worst Case scenario: we get only numbers dividable by 3. So instead of:
```
	1, 2, 3, 4, 5, 6... 11, 12, etc,
```
we get:
```
	3, 6, 9, 12, 15, 18, etc.
```
That will lead to an uneven distribution, where baskets 3, 6, 9 and 0 will be full, whereas other baskets will be completely empty. Therefore we need to reduce the number of dividers, to prevent a worst case scenario and achieve an even distribution. 

*If you are looking for illustrations and more detailed but simple explanation, you can find them here https://cs.stackexchange.com/a/157627)*


### So if the number of collisions is defined by p, why would we need to use b? Why not just adding character values and mod them? 

The problem is, that different strings can result in the same sum. Let's take a look at this example (instead of ascii we'll just take the alphabet position of the letter):
 ```		
		be = 2+5 = 7
		eb = 5+2 = 7, 
		just like cd = 3+4 = 7 
```
Those b constructions add weight to each value making repetitions less likely.

### But what size for b should we choose?

Depends on the alphabet you're using. Usually the value of b is 256, which covers all ASCII characters), but it can also be smaller or bigger. Just make sure it covers all the characters your alphabet has, otherwise it'll also lead to collisions. But be careful: if the value of b is too big it can result in overflow.

### And how exactly is Rabin-Karp method used in modern cryptography?

Even though the Rabin-Karp algorithm is nowadays used primarily for spell checking and bio-informatics, just like other string matching algorithms, it can also be used in network intrusion detection systems to verify the data packets traveling through the network or in digital forensics to find evidence within digital data. Rabin-Karp algorithm introduced a concept of polynomial hashing, however, cryptographic hashing required fundamentally different construction that we'll talk about next time.

### My sources and further readings: 
[MIT Rabin-Karp Algorithm](https://people.csail.mit.edu/alinush/6.006-spring-2014/rec06-rabin-karp-spring2011.pdf)
[MIT Pigeonhole](https://math.mit.edu/~fgotti/docs/Courses/C.%20Combinatorial%20Analysis/1.%20Pigeonhole%20Principle/Pigeonhole%20Principle.pdf)
[Michael O. Rabin Biography](https://cacm.acm.org/news/in-memoriam-michael-o-rabin/)
[Research about String Matching Algorithms](https://www.researchgate.net/publication/332773245_Exact_String_Matching_Algorithms_Survey_Issues_and_Future_Research_Directions)
[Oxford Rabin-Karp in Bioinformatics](https://academic.oup.com/bioinformaticsadvances/article/3/1/vbad162/7413189)
[More about Rabin-Karp Algorithm](https://www.geeksforgeeks.org/dsa/rabin-karp-algorithm-for-pattern-searching/)
[More about Hash Functions](https://www.geeksforgeeks.org/dsa/hash-functions-and-list-types-of-hash-functions/)
