---
title: "From One Seed to a Thousand Leaves - Merkle's Authentication Tree"
date: 2026-08-03
---

<div style="font-style: italic; color: #734f96;">
	
An implementation of a small Merkle Tree can be found in <a href="https://github.com/0xkrt26/math_behind_security/blob/main/implementations/merkle_tree.py">my GitHub Repository</a>.

</div>
<br> 

The Great Seal of Realm - the sign of a royal approval. For centuries, Kings and Queens, Emperors and Empresses, Ladies and Lords used seals to leave their family names on the important documents. But what was left for us, ordinary commoners? Simple autographs were our low budget seals. Their uniqueness comes from a combination of pen pressure, speed and rhythm, letter slant, and spacing. 

But the world is evolving. We can hardly imagine navigating modern life without computer, mobile phone, or internet. And the problem with ordinary autographs in this setting is that they can be easily copy-pasted from one document to another just like a fancy sticker. It is very helpful when you don't want to print the document, only to sign it and then scan it again, since we all know the struggle of drawing with a touchpad or a computer mouse (at least I always get some weird doodles instead of a signature). But unfortunately, if you can copy-paste it, then anyone else can do the same. And I bet it won't feel very nice if one morning you wake up and all your stocks and investments are gone because someone forged your autograph on a gift deed, will it? 

But no worries. Already in 1979 Ralph Charles Merkle came up with an idea of a digital signature, which he described in his PhD thesis "Secrecy, Authentication, and Public Key Systems". Though to be accurate, the idea of a digital signature was not his. He improved an already existing Lamport-Diffie one-time signature, which, in turn, was an improved version of Rabin's signature, as Leslie Lamport mentions himself in the description to his report paper on the [Microsoft research forum](https://www.microsoft.com/en-us/research/publication/constructing-digital-signatures-one-way-function/).

<br>
### So what is that Lamport-Diffie one-time signature?

Merkle explains it with a very nice and clear example. Imagine two people: Alice, who has a stock, and Bob - a broker. Alice wants to sell her stock, but Bob can accept neither a phone call nor a message as a confirmation (since it's so easy to deepfake someone's voice nowadays). So they remember that when Alice bought this stock she computed F(x)=y using a one-way function (some examples of such functions can be found in the previous [post](https://0xkrt26.github.io/math_behind_security/2026/06/09/the-story-of-the-hash-function.html)) and sent it to Bob. They even signed a contract that contained F and y, but not x, and agreed that if Alice wants to sell her share, she'll reveal her x to Bob.

<div style="font-style: italic; color: #734f96;">

Note that F is a one-way function, therefore irreversible, which means there is no other way for Bob to get x unless Alice reveals it to him. This is why we can claim that the 1-bit message that Alice sends is authenticated.

</div>

<br>
### And what if Alice wants to send a longer message?

Rarely does someone want to sell the entire stock at once. Much more often, people sell a certain number of shares. For example, Alice wants to sell 11 shares. For her to do that, the buying contract has to look a bit different. 

Alice would have had to choose j private keys x:

<div align="left">
$$
\begin{matrix}
x_1 \\
x_2 \\
x_3 \\
\vdots \\
x_j
\end{matrix}
$$
</div>

and compute $2j \cdot F(x_j)$. These values she then shares with Bob as a public key in the form of a vector X_i. 

<div style="font-style: italic; color: #734f96;">

The value j is a fixed number, representing the bit length of the message, that Alice can sign. For our example, we will use j=100.

</div>
<br>
So some time later, Alice wants to send a message m: "Sell 11 shares". 

First, she needs a binary representation of her message:

01010011 01100101 01101100 01101100 00100000 00110001 00110001 00100000 01110011 01101000 01100001 01110010 01100101 01110011

<div style="font-style: italic; color: #734f96;">

The length of this message is 112 bits, but since $j=100$, she has only 100 precomputed keys and therefore can sign only 100 bits.
<br>
Does it mean she has to make her message shorter?
<br>
Of course not. Instead we just use another one-way function to map all 112 bits to 100 bits. And if the message was too short, we would extend it with zeroes until it had exactly 100 bits.

</div>
<br>

So for each bit out of 100, she has a private key x_j and a public key y_j. To sign her message m, she sends Bob all the x_j of all the bits that equal 1 in her message (also in a vector form). So in our example for the letter s she sends:

<div align="left">
$$
\begin{array}{c}
\mathtt{01010011} \\[1ex]
x_2 \\
x_4 \\
x_7 \\
x_8
\end{array}
$$
</div>

For the next letter e, she reveals:

<div align="left">
$$
\begin{array}{c}
\mathtt{01100101} \\[1ex]
x_2 \\
x_3 \\
x_6 \\
x_8
\end{array}
$$
</div>

...and so on.

This way, Alice signs every bit of her message.

<br>
### So the message is secured?

Actually, not completely. There is a way for Bob to alter the message. He can just pretend he never got one of the private keys x_j from Alice, therefore changing 1 in the message to 0. This way he can say that instead of 11 shares:

00110001 00110001

Alice asked him to sell only 10 shares:

00110001 00110000

<br>
To avoid this, Lamport and Diffie suggest appending m' - a complement of m - to the end of the message. This way, if Bob wants to change 11 shares to 10 shares, he would have to reveal x_j that corresponds to 1 in the complement of m' (the very last bit of the forged message in the following example), which he can't do as Alice never sent him that private key.

<br>
Example:

Original mm'= 00110001 00110001 11001110 11001110

Forged mm'= 00110001 00110000 11001110 11001111
<br>

Everything seems to be working well now. But the problem is, such one-time signature requires too much storage space. So Ralph Merkle decided to improve the algorithm and suggested another way to sign messages.

<br>
### How does Merkle improve the Lamport-Diffie one-time signature?

Merkle's first solution was to reduce the actual length of the protected message. So Lamport suggested using the complement m' of m to protect Bob from altering the signature, right? That was a good idea, but it also made the message twice as long as it was.

To save some storage space, Merkle adds the amount of 0s to the end of the message m. For that he would need only $log_2 j$ (or in our example $log_2 100$) additional bits, which is significantly less than in Lamport's idea.

<div style="font-style: italic; color: #734f96;">

Why log_2?
<br>
The amount of zeroes is stored as a binary number, so to store 8 bits we need 3 bits, for 100 bits 4 bits since 100 is between 2^6=64 and 2^7=128.

</div>

<br>
### Can we store the number of 1s instead of 0s?

No, since that won't protect the signature from being altered.

You see, Bob can only change 1s to 0s, not the other way around. For changing 0 to 1, he would need a private key that he never got. 

Let's look at an example. We will have an 8-bit instead of a 100-bit message with five 0s:

10001**1**00 1**01**

Now Bob wants to forge the message by changing one bit from 0 to 1. Now message has six 0s:

10001**0**00 1**10**

As you can see, changing 1 to 0 in one part means also changing 0s to 1s in another part, which Bob can't do.
<br>
Now if instead of 0s, we were appending the number of 1s:

10001**1**00 1**1**

Bob would be able to forge it without any problem by just changing 1s to 0s in both parts:

10001**0**00 1**0**

<br>
### But do we have to store all those public keys that take up so much space?

Of course (if we use the Lamport-Diffie one-time signature). Otherwise, how would Bob know it's Alice who is sending him the keys? What if it was an enemy of Alice Eva who created all the public and private keys right before signing her evil message "Gift all my stocks to Eva. Alice" and sending it to Bob? It can only be fixed with some sort of prior arrangement. But as we can imagine, storing all those public keys takes a lot of Bob's storage. So Merkle came up with another solution called "tree authentication".

<br>
### How does tree authentication work?

The whole construction looks like a binary tree. The leaves are the Y_i values (the public keys calculated using the Lamport-Diffie method). The inner knots and the root are computed inductively using another one-way function H. We start from the leaves with:

$$H(i, i, Y) = F(Y_i)$$

and go up to the root using:

$$H(i, j, Y) = F\left( H\left(i, \frac{i+j}{2}, Y\right), H\left(\frac{i+j}{2} + 1, j, Y\right) \right)$$

This might seem complicated at first, but let's look at an example and try to understand how exactly the signing process works.

<br>
Example:

Let's assume Alice wants to be able to send eight signed messages to Bob. First she computes 8 vectors Y_1, Y_2,..., Y_8 using Lamport-Diffie signature. Then Alice calculates:

<div align="left">
$$
\begin{aligned}
H(1, 1, Y_1) &= F(Y_1) \\
H(2, 2, Y_2) &= F(Y_2) \\
&\;\;\vdots \\
H(8, 8, Y_8) &= F(Y_8)
\end{aligned}
$$
<div align="left">
	
Then she takes pairs of $H(i,i,Y)$ and creates inner nodes:

<div align="left">
$$
\begin{aligned}
H(1, 2, Y_{1,2}) &= F\big( H(1, 1, Y_1), H(2, 2, Y_2) \big) \\
H(3, 4, Y_{3,4}) &= F\big( H(3, 3, Y_3), H(4, 4, Y_4) \big) \\
H(5, 6, Y_{5,6}) &= F\big( H(5, 5, Y_5), H(6, 6, Y_6) \big) \\
H(7, 8, Y_{7,8}) &= F\big( H(7, 7, Y_7), H(8, 8, Y_8) \big)
\end{aligned}
$$
</div>

Then pairs the new Hs again:

<div align="left">
$$
\begin{aligned}
H(1, 4, Y_{1,4}) &= F\big( H(1, 2, Y_{1,2}), H(3, 4, Y_{3,4}) \big) \\
H(5, 8, Y_{5,8}) &= F\big( H(5, 6, Y_{5,6}), H(7, 8, Y_{7,8}) \big)
\end{aligned}
$$
</div>

And one more time:

$$H(1, 8, Y_{1,8}) = F\big( H(1, 4, Y_{1,4}), H(5, 8, Y_{5,8}) \big)$$

The value $H(1, 8, Y_1,8)$ that Alice gets is a root value R. This is the only value that Bob and Alice have to agree upon before signing any messages and therefore the only public key that Bob needs to store. 

<br>
### How does Alice actually sign the message?

Let's imagine in the form of dialogue between Alice and Bob how exactly the first message m_1 out of eight available messages is signed.

Alice:

$$H(5, 8, Y_{5,8})$$  
$$H(1, 4, Y_{1,4})$$


Bob:  
*(takes $H(1, 8, Y_{1,8})$ from the contract)*  

$$H(1, 8, Y_{1,8}) = F\big( H(1, 4, Y_{1,4}), H(5, 8, Y_{5,8}) \big)?$$  
If yes, proceed.

Alice:  
$$H(1, 2, Y_{1,2})$$  
$$H(3, 4, Y_{3,4})$$

Bob:  
$$H(1, 4, Y_{1,4}) = F\big( H(1, 2, Y_{1,2}), H(3, 4, Y_{3,4}) \big)?$$  
If yes, proceed.

Alice:  
$$H(1, 1, Y_1)$$  
$$H(2, 2, Y_2)$$

Bob:  
$$H(1, 2, Y_{1,2}) = F\big( H(1, 1, Y_1), H(2, 2, Y_2) \big)?$$  
If yes, proceed.

Alice:  
$$Y_1$$

Bob:  
$$F(Y_1) = H(1, 1, Y_1)?$$  
If yes, then the message is indeed from Alice, and the private keys can be revealed according to the Lamport-Diffie method.


<div style="font-style: italic; color: #734f96;">

After Alice uses all 8 available signatures, the root value R has to be changed, and the binary tree has to be computed once again.

</div>

<br>
### Does tree authentication really solve the problem of excessive storage?

Sure. Let's calculate. 

In our example of the Lamport-Diffie one-time signature, both of the hash functions that we used while compressing and signing, produce 100-bit outputs. 

<div align="left">
$$
\begin{aligned}
2 \cdot j \cdot s &= 2 \cdot 100 \cdot 100 = 20{,}000 \text{ bits} \\[1ex]
\text{where:} \\
2j &\text{ = amount of public and private keys} \\
s &\text{ = length of one public/private key}
\end{aligned}
$$
</div>

Now if Bob receives not just one but 1000 messages from Alice, the amount of storage needed to store all the public keys would be 

$$20{,}000 \cdot 1000 = 20{,}000{,}000 \text{ bits} = 2.5 \text{ MB}$$

And if Bob has other clients (let's say 1000), then the storage space needed will be about 2.5 GB. 

Of course, it is possible to store this amount of data, but what if the number of users and/or messages is even bigger? 

Now with Merkle's improvement, Bob only stores the root value R, which, just like all other values here, is a fixed-length 100-bits value.

2.5 Gb vs 100 bits. The difference is huge, isn't it?

<br>
### But Alice still has to store all those authentication paths, doesn't she? 

Not exactly. Let's look at the authentication paths for the tree from our example: 

<div align="left">
$$
\begin{aligned}
Y_1 &: H(2,2), H(3,4), H(5,8), H(1,8) \\
Y_2 &: H(1,1), H(3,4), H(5,8), H(1,8) \\
Y_3 &: H(4,4), H(1,2), H(5,8), H(1,8) \\
Y_4 &: H(3,3), H(1,2), H(5,8), H(1,8) \\
Y_5 &: H(6,6), H(7,8), H(1,4), H(1,8) \\
Y_6 &: H(5,5), H(7,8), H(1,4), H(1,8) \\
Y_7 &: H(8,8), H(5,6), H(1,4), H(1,8) \\
Y_8 &: H(7,7), H(5,6), H(1,4), H(1,8)
\end{aligned}
$$
</div>

You notice something interesting? If no, look at this modified version: 

<div align="left">
$$
\begin{aligned}
Y_1 &: H(2,2), H(3,4), H(5,8), H(1,8) \\
Y_2 &: H(1,1) \\
Y_3 &: H(4,4), H(1,2) \\
Y_4 &: H(3,3) \\
Y_5 &: H(6,6), H(7,8), H(1,4) \\
Y_6 &: H(5,5) \\
Y_7 &: H(8,8), H(5,6) \\
Y_8 &: H(7,7)
\end{aligned}
$$
</div>

That's the tree after we deleted all the duplicates. Already so much less to store, isn't it?

Moreover, the modified version is just the Merkle tree itself but with flipped inner knots. Just compare the authentication paths with this scheme:

![Merkle Tree](/math_behind_security/_posts/merkle_tree/merkle-tree1.png)

<div style="font-style: italic; color: #734f96;">

The inner nodes in the authentication paths are flipped because both functions F and H are known to Bob, so from Y_1 he can easily compute H(1,1), but would need H(2,2) to compute and therefore authenticate H(1,2).

</div>
<br>

What's even better is that there's no need for Alice to store most of the values till the next root change. She can delete the nodes that are not going to be used for the authentication again. For example, after computing Y_1, Y_2, and Y_3, we can just delete four inner nodes H(1,1), H(3,4), H(3,3) and H(2,2).

Here's the updated tree for better visualisation:

![Merkle Tree](/math_behind_security/_posts/merkle_tree/merkle-tree2.png)

<br>
### But Alice probably has to store all the unused private keys X_i and public keys Y_i anyway, right?

Nope. For this, Merkle also found a solution.
All Alice needs to store is a single 200-bit seedkey - 200 bits of random once-generated data. With just this seedkey, she would be able to restore all the eight 10700-bits-long private keys X_1 to X_8. For that to work, instead of choosing 8*107 random values for her private keys x_j in the very beginning, Alice would have to choose just this one secret seedkey 200 bits long and then generate:

$$x_{i,j} = C(\text{seedkey}, \langle i, j \rangle)$$
<br>
<div style="font-style: italic; color: #734f96;">

Here private key x has two indexes i and j. i shows the message number, and j indicates the position of the bit in the message.
<br>
C stands for cipher and performs as an encryption function. I will write about ciphers and encryption in much more detail once I finish covering the history of hashing. For now, imagine it as a generator of numbers that might look random but are actually determined through a special publicly known algorithm. 
<br>
Note that without the seedkey it is impossible to generate any of the x_i,j values. This means that only Alice can produce valid private keys for her messages
</div>
<br>

So since Alice can restore all the private keys from just a 200-bit seedkey, why store Y_i, when, as we know, those can also be easily computed through F(x)? Merkle calculated that computing all the keys from a seedkey doesn't take too much time and energy compared to the amount of storage we would need to keep all those keys. Today the time for such computation is even less, so it is definitely worth it.

<br>
### Does it mean Merkle authentication tree is still used today?

It is. In fact, Merkle tree is a fundamental part of a blockchain. Just instead of messages, leaf nodes contain hashes of transactions. 

Let's quickly take a look at what a blockchain is. The name speaks for itself: it's a chain of blocks. Each block contains a connection to the previous block and a Merkle tree with thousands of transactions as its leaves. 

The most common example of a blockchain would be Bitcoin. The paper "Bitcoin: A Peer-to-Peer Electronic Cash System" explicitly names Merkle tree as a solution for Simplified Payment Verification. This means if you are buying Bitcoin but first want to make sure it's not a fraud, you can verify a single transaction without downloading the entire blockchain. All you need is the relevant authentication path - exactly what Bob needed to verify a single message without storing the entire tree.

Now you may wonder, how is this whole construction relevant to the history of hashes we're currently covering? The thing is, those one-way functions H and F are hash functions. So each node of the Merkle tree basically stores a hash of some value. This saves a lot of storage space since the output of a hash function is always a fixed-length number and provides security, making the Merkle authentication tree a perfect foundation for a cryptocurrency.  


<br>
### My sources and further readings: 
[Ralph Charles Merkle's PhD thesis "Secrecy, Authentication, and Public Key Systems"](https://www.ralphmerkle.com/papers/Thesis1979.pdf)
<br>
["Constructing Digital Signatures from a One Way Function" by Leslie Lamport](https://www.microsoft.com/en-us/research/publication/constructing-digital-signatures-one-way-function/)
<br>
["Bitcoin: A Peer-to-Peer Electronic Cash System"](https://bitcoin.org/bitcoin.pdf)

<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
