---
title: How to build a collision-resistant hash function? - Merkle-Damgård 1989 construction
date: 2026-11-13
---

<style>
mjx-container[display="true"] {
  text-align: left !important;
  margin-left: 0 !important;
  overflow-x: auto;
  overflow-y: hidden;
  max-width: 100%;
}
</style>

<div style="font-style: italic; color: #734f96;">

A Python implementation for a Merkle-Damgård construction is available in <a href="https://github.com/0xkrt26/math_behind_security/blob/main/implementations/merkle-damgard.py"> my GitHub repository</a>

</div>
<br> 

1978\. Michael O. Rabin proposes his idea of a hash function. But what is so interesting about it? Hash functions were not something new for that time. Already a few years before [Diffie-Hellman](https://0xkrt26.github.io/math_behind_security/2026/06/09/the-story-of-the-hash-function.html) suggested their version of a one-way function for digital signatures. Well, Rabin's function had a very useful property that Diffie-Hellman lacked. The input didn't have to be a short message anymore. Thanks to a chaining mechanism, one function could produce a fingerprint of the whole book!  

Unfortunately, this hash function was not secure. Already a year later in 1979, Gideon Yuval publishes an article, "How to swindle Rabin", that makes it obvious: Rabin forgot to check one of the most important properties of a good hash function - collision resistance. In that time a construction was considered unbreakable if the attacker needed to brute force through more than <span markdown="0">$2^{56}$</span> operations to break it. This number comes from a collision formula <span markdown="0">$2^{n/2}$</span>, where <span markdown="0">$n$</span> is the output length, which was created thanks to [the Birthday Problem](https://0xkrt26.github.io/math_behind_security/2026/05/08/birthday-problem.html). For Rabin's function, it was possible to find two different inputs that produced the same output already after only <span markdown="0">$2^{32}$</span> operations.

<br>

### So how do we build a collision-resistant hash function?

Let's not start from zero, but try to upgrade Rabin's idea. He split the message into chunks, then built sort of a conveyer chain out of [DES](https://0xkrt26.github.io/math_behind_security/2026/09/16/doodles-to-des.html) applications and used each chunk as a key for DES. The first plaintext that the conveyer took in was a predefined initial state (IV). Further, the plaintext input was used for the carry-on output of the previous round.

```
      M1     M2            M3
       |      |            |
IV -> DES -> DES -> ... -> DES -> h(M)
```

And everything seems to work well, but... DES is a block cipher. So yes, it compresses the input, but it still can be reversed by decryption. And if the foundation of the chain is so vulnerable, how can the chain itself be secure?

There's a quick fix for this problem, though. All we have to do is XOR the DES' output with the original plaintext: 

<div markdown="0">
$$f(\text{key}, \text{plaintext}) = \text{ENCRYPT}(\text{key}, \text{plaintext}) \oplus \text{plaintext}$$
</div>

This is called a Davies-Meyer compression function. It breaks the block cipher's reversibility. Now even if you try to treat the output of <span markdown="0">$f$</span> as DES output, decrypt it, and get two valid inputs, to create a collision you would have to run these through <span markdown="0">$f$</span> again, and XOR will destroy the found "collision". So the only way to find the input is to brute force. 

Another minor change: instead of using message chunks as keys, we will treat complete DES input as a field for our message chunk. This will allow us to take in more bits per cycle.

What we have built is called a compression function. And we could have stopped here, but is <span markdown="0">$f$</span> really collision resistant?

<br>

### How to make a compression function collision-resistant?

Right now the output of <span markdown="0">$f$</span> is only 64 bits long, the input is 120 bits. By the collision formula we mentioned earlier, for the security level of <span markdown="0">$2^{56}$</span> bits we would need an output of at least 112 bits. So what can we do to get 112 bits in the end? Nothing complicated. Let's concatenate two outputs of our <span markdown="0">$f$</span> function and call it <span markdown="0">$F_1$</span>:

<div markdown="0">
$$F_1 = \text{First112bitsOf}\left( f(\text{"0"}, x) \,\|\, f(\text{"1"}, x) \right)$$
</div>

Outputs had to be different, otherwise such concatenation wouldn't have made a lot of sense. That's why we used two predefined bits: "0" for the first input and "1" for the second one. Of course, we had to shorten the input of <span markdown="0">$F_1$</span> by one bit, but that's not such a big price to pay for security. 

<div style="font-style: italic; color: #734f96;">

<br>
Why couldn't we just take the first and last 119 bits of the input?
<br><br>
While this idea saves us that one extra bit, it doesn't always guarantee different inputs. Imagine the input of <span markdown="0">$F_1$</span> was 1111...11111. Then both the first and the last 119 bits would be just 1s. But if we force the first bit of each input to be different, we will definitely get different inputs. Even if the difference is only by that one bit. 
<br><br>
Why do we take only 112 bits of the output instead of leaving 128 bits for additional security?
<br><br>
As we already know, the compression function will be applied multiple times for longer texts in a chain, so we would wish for the carry-on output to be as much smaller than the input as it's possible without affecting security. And since in this case cutting the output of <span markdown="0">$F_1$</span> doesn't affect security in any way, we can just throw those bits away and free up some space.

</div>
<br>

### We took care of security, but what about efficiency? 

Our hash function needs to be secure but also efficient. No one would want to wait hours for a fingerprint to be computed. So let's calculate the efficiency of <span markdown="0">$F_1$</span>:

<div markdown="0">
$$\begin{aligned}
\text{input}_1 &: 119 \text{ bits} \\
\text{output}_1 &: 112 \text{ bits} \\
\text{input}_2 &: \text{output}_1 + \text{new bits} = 112 + \mathbf{7} = 119
\end{aligned}$$
</div>

Right now our compression function <span markdown="0">$F_1$</span> takes in only 7 new bits per iteration. And since each iteration has two DES applications, we're using DES (the longest and the most computationally expensive part of our construction) every 3.5 bits. I bet we could do better. 

<br>

### How to make the compression function more efficient? 

We could increase the difference between the input and the output. For that, let's try and use more DES per cycle. Sounds inefficient at first, but let's not go ahead of ourselves. 

As we remember, each DES application had its own predefined bits to ensure the difference of the inputs. For four DES we will have to use bits 00, 01, 11, and 10, so each input of <span markdown="0">$f$</span> is now only 118 bits long.

<div markdown="0">
$$F_2 = f\big(\text{"00"},\, f(\text{"01"}, x_1) \,\|\, x_2\big),\; f\big(\text{"10"},\, f(\text{"11"}, x_1) \,\|\, x_2\big)$$
</div>
<br>
The bit math for <span markdown="0">$F_2$</span> looks like this:

<div markdown="0">
$$\begin{array}{lcl}
 & \text{"01"} + 118 \xrightarrow{\text{DES, XOR}} 64 \;\;+\;\; \text{"00"} + 54 \xrightarrow{\text{DES, XOR}} 64 & \\
172 \text{ bits} \rightarrow & & += 128 \text{ bits} \\
 & \text{"11"} + 118 \xrightarrow{\text{DES, XOR}} 64 \;\;+\;\; \text{"10"} + 54 \xrightarrow{\text{DES, XOR}} 64 &
\end{array}$$
</div>

<br>
<div style="font-style: italic; color: #734f96;">

We left the output 128 bits long. Why not cut it down to 112 bits again? 
<br><br>
To be honest, I had the same question. I tried to untangle it, but I'm still not 100% sure that I got it right, so read it with some criticism. 
<br><br>
Look at our bit math. We are squeezing 118 bits into 64 bits twice. This creates sort of a bottleneck, which compromises the randomness of the function and the security of the proof. It can happen that the middle values collide, which will lower the security level from the desired <span markdown="0">$2^{56}$</span> operations.

</div>
<br>

Time to evaluate the efficiency of <span markdown="0">$F_2$</span>:

<div markdown="0">
$$\begin{aligned}
172 - 128 &= 44 \\
44 : 4 &= 11
\end{aligned}$$
</div>

So our upgraded compression function takes 44 new bits per iteration and applies DES only every 11 bits. This is already much better than what we had after our first try. 

<br>

### But can it be even better?

Adding more DES worked, so let's stick to it:

<div markdown="0">
$$F_3 = f\big(\text{"00"},\, \text{First59bitsOf}(f(\text{"100"}, x_1)) \,\|\, \text{First59bitsOf}(f(\text{"101"}, x_2))\big) \,\|\, f\big(\text{"01"},\, \text{First59bitsOf}(f(\text{"110"}, x_1)) \,\|\, \text{First59bitsOf}(f(\text{"111"}, x_2))\big)$$
</div>

<br>
Now here's the bit math: 

<div markdown="0">
$$234 \text{ bits} = 117\text{(F - first)} + 117\text{(L - last)}$$
</div>

<div markdown="0">
$$\begin{array}{lll}
 & \text{"100"} + 117\text{(F)} \xrightarrow{\text{DES, XOR}} 64 \rightarrow 59 & \\
 & & + \text{"00"} \xrightarrow{\text{DES, XOR}} 64 \\
 & \text{"101"} + 117\text{(L)} \xrightarrow{\text{DES, XOR}} 64 \rightarrow 59 & \\
234 \text{ bits} \rightarrow & & += 128 \text{ bits} \\
 & \text{"110"} + 117\text{(F)} \xrightarrow{\text{DES, XOR}} 64 \rightarrow 59 & \\
 & & + \text{"01"} \xrightarrow{\text{DES, XOR}} 64 \\
 & \text{"111"} + 117\text{(L)} \xrightarrow{\text{DES, XOR}} 64 \rightarrow 59 &
\end{array}$$
</div>
<br>
And the efficiency:

<div markdown="0">
$$\begin{aligned}
234 - 128 &= 106 \\
106 : 6 &= 17.7
\end{aligned}$$
</div>

This upgrade lets us add 106 new bits per iteration, which means we have to apply DES only every 17.7 bits. Now that's progress!

<br>

### How many more DES per iteration can we use? 

The bit math scheme of <span markdown="0">$F_3$</span> looks like a binary tree, which means that theoretically it could grow bigger and bigger. 

However, there are two "be careful" points: the distance between gained bits gets smaller and smaller (<span markdown="0">$3.5 \rightarrow 11 \rightarrow 17.7$</span>) and the chance of collision without additional security methods gets bigger and bigger. Notice that already for the next upgrade, 128 bits won't be enough to keep the <span markdown="0">$2^{56}$</span> operations security level. So it might not be worse it. 

Therefore, let's stop at <span markdown="0">$F_3$</span> for now. 

<br>

### And finally, what does the chaining look like? 

There's nothing new here. We can just take Rabin's chaining, but instead of DES blocks, we use our <span markdown="0">$F_3$</span> function (let's notate it as <span markdown="0">$F$</span> with indices for each cycle):

```
      M1     M2            Mn
       |      |            |
IV -> F_1 -> F_2 -> ... -> F_n -> H(M)
```

Let's define the initial value as zero so that the first chunk <span markdown="0">$M_1$</span> could take all the input bits. Note that each message chunk should have the same length. That's why if <span markdown="0">$M_n$</span> is too short, we complete it with padding zeroes. 

Adding padding zeroes, however, creates a new problem. Imagine we have two messages that are less than one chunk long: 

<div markdown="0">
$$\begin{aligned}
\mathrm{Mn}_1 &= 010101100 \\
\mathrm{Mn}_2 &= 0101011
\end{aligned}$$
</div>

And let's say, each chunk has to be 16 bits. Then after padding, we get two identical strings for both <span markdown="0">$\mathrm{Mn}_1$</span> and <span markdown="0">$\mathrm{Mn}_2$</span>:

<div markdown="0">
$$\begin{aligned}
\mathrm{Mn}_1 &= \mathbf{010101100}0000000 \\
\mathrm{Mn}_2 &= \mathbf{0101011}000000000
\end{aligned}$$
</div>

This creates a collision. And we don't want that to happen, so we add length blocks into those chunks. They can show the length of padding or the length of the message. It doesn't really matter which length to encode, but we will go with the length of the message. You'll see later why. So this is what our message chunks look like after we added a length block:

<div markdown="0">
$$\begin{aligned}
\mathrm{Mn}_1 &= \mathbf{010101100}000\mathbf{1001} \\
\mathrm{Mn}_2 &= \mathbf{0101011}00000\mathbf{0111}
\end{aligned}$$
</div>

<br>


### How do we know that the construction that we've built is secure?

We've built a collision-resistant compression function <span markdown="0">$F_3$</span>. Now we need to make sure the chaining is also collision-resistant. Let's prove it in two steps:

<br>

  **1. If compression function <span markdown="0">$F$</span> is collision-resistant, then a hash function <span markdown="0">$H$</span> is also collision-resistant for all the inputs of the same length.**

This step can be proved by induction. 

**Basis:**

If the input consists only of one chunk <span markdown="0">$M$</span>, the compression function <span markdown="0">$F$</span> will be applied only once. So in this case, the hash function <span markdown="0">$H$</span> is just our compression function <span markdown="0">$F$</span>. And if <span markdown="0">$F$</span> is collision-resistant, so is <span markdown="0">$H$</span>.

**Induction:**

Now we can assume a compression function <span markdown="0">$F$</span> applied to <span markdown="0">$k$</span> inputs is collision-resistant. We will call the output of it <span markdown="0">$H(M_k)$</span>. Now we need to prove that it's also secure for <span markdown="0">$k+1$</span> inputs (that <span markdown="0">$H(M_{k+1})$</span> is secure).

To do that, let's take two different messages <span markdown="0">$M$</span> and <span markdown="0">$M'$</span> of the same length that produce the same outputs and look at the last compression function application <span markdown="0">$F_{k+1}$</span> and the inputs of it: last chunks <span markdown="0">$M_{k+1}$</span> and <span markdown="0">$M_{k+1}'$</span> and outputs of <span markdown="0">$H(M_k)$</span> and <span markdown="0">$H(M_k')$</span>. 

<br>

**Case 1:** The inputs of <span markdown="0">$F_{k+1}$</span> are different.

<div markdown="0">
$$\begin{aligned}
(H(M_k), M_{k+1}) &\neq (H(M_k'), M_{k+1}') \\
H(M_{k+1}) &= H(M_{k+1}')
\end{aligned}$$
</div>

The inputs were different, but the function <span markdown="0">$F_{k+1}$</span> produced the identical outputs. That's a collision. This would mean that the compression function <span markdown="0">$F$</span> that is collision-resistant per definition is not collision-resistant. This is a contradiction.

<br>

**Case 2:** The inputs of <span markdown="0">$F_{k+1}$</span> are identical.

<div markdown="0">
$$(H(M_k), M_{k+1}) = (H(M_k'), M_{k+1}')$$
</div>

We know that <span markdown="0">$M$</span> and <span markdown="0">$M'$</span> are two different messages, so either <span markdown="0">$M_{k+1}$</span> and <span markdown="0">$M_{k+1}'$</span> are different (contradicts the Case 2 assumption), or one of the chains <span markdown="0">$H(M_k)$</span> or <span markdown="0">$H(M_k')$</span> produced the same output for different inputs, and therefore, is not collision-resistant (contradiction to the induction hypothesis). 

This means a hash function <span markdown="0">$H$</span> can produce the same output for two messages only if either those messages were identical or the compression function <span markdown="0">$F$</span> was not collision resistant. 

<br>

  **2. If a hash function <span markdown="0">$H$</span> is collision-resistant for all the inputs of the same length, then it is collision-resistant for all the inputs of the different length (considering the input included the length block).**

This one is even easier to prove. Assume we have two inputs of different lengths: <span markdown="0">$M$</span> and <span markdown="0">$M'$</span>. Let's say <span markdown="0">$M$</span> is shorter than <span markdown="0">$M'$</span>, and their hashes happen to be equal:

<div markdown="0">
$$\begin{aligned}
M &\neq M' \\
|M| &\lt |M'| \\
H(M) &= H(M')
\end{aligned}$$
</div>

But we know that the last chunks of <span markdown="0">$M$</span> and <span markdown="0">$M'$</span> must have been different, since they included the length blocks. And because the lengths of <span markdown="0">$M$</span> and <span markdown="0">$M'$</span> are different, the outputs should have been different. Or there was a collision in the last <span markdown="0">$F$</span>, which is impossible, since, as we've said in the last proof, <span markdown="0">$F$</span> was defined as a collision-resistant function. 

To sum this proof up: If the hashes match, there was a collision in the last application of <span markdown="0">$F$</span>, so either the lengths of messages were equal (contradiction) or <span markdown="0">$F$</span> was not collision-resistant (also a contradiction).

<br>

### Congratulations! We've built the...

Merkle-Damgård construction! It was developed simultaneously by Ralph Merkle and Ivan Damgård and presented by both of them independently on the CRYPTO'89 Conference. We've built Merkle's version today. Damgård's idea differs just slightly. For example, he uses the padding-length instead of the message-length, and therefore his proof also differs. If you're interested in his version of this hash construction, check his paper ["A Design Principle for Hash Functions"](https://www.researchgate.net/publication/221354712_A_Design_Principle_for_Hash_Functions).

Merkle-Damgård construction became the base of the modern hash functions. Its core - chaining, the Davies-Meyer step, a secure symmetric block cipher inside - was used in MD5, SHA 1, and SHA 2. However, some of those hash functions were still broken later. Why? You'll have to wait for my next post to find out.

<br>

### My sources and further readings:

[Ralph Merkle "One Way Hash Functions and DES"](https://link.springer.com/content/pdf/10.1007/0-387-34805-0_40.pdf)
<br>
[Ivan Damgård "A Design Principle for Hash Functions"](https://www.researchgate.net/publication/221354712_A_Design_Principle_for_Hash_Functions)
<br>
[Gideon Yuval "How to swindle Rabin"](https://www.tandfonline.com/doi/abs/10.1080/0161-117991854025) 
<br>
[Michael O. Rabin "Digitalized signatures"](https://scispace.com/pdf/foundations-of-secure-computation-1ehszkx7l1.pdf)

<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
