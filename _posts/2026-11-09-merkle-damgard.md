---
title: How to build a collision-resistant hash function? - Merkle-Damgård 1989 construction
date: 2026-11-09
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

A Python implementation for a Merkle-Damgård construction is available in <a href="https://github.com/0xkrt26/math_behind_security/blob/main/implementations/merkle-damgard.py">my GitHub repository</a>

</div>
<br>

We have a problem! We need a secure hash function that will be computed fast enough even for long texts. But no worries, that's exactly what Ralph Merkle solved in 1989. He developed a method for creating a strong hash function by just compressing a symmetrical block cipher. Though let's not jump straight to the solution and try to build the construction step by step.

<br>
### First thing first, what makes a hash function secure?

A secure hash function has all the following properties:

1. It works for all the lengths of inputs (both for one sign and for the longest book there is)
2. It produces a fixed-size output (in our case 112 or 128 bits long. I'll explain a bit later where the number comes from)
3. It's easy to compute
4. It's pre-image resistant: you can't decrypt it or reverse it even if you know the function (more about it in my post about [Diffie-Hellman](https://0xkrt26.github.io/math_behind_security/2026/06/09/the-story-of-the-hash-function.html))
5. It's second preimage resistant: you can't find another input <span markdown="0">$x'$</span> that will produce the same output as your input <span markdown="0">$x$</span>
6. It is collision resistant: it'd take too long to find two inputs that produce the same output (read more about [the birthday problem here](https://0xkrt26.github.io/math_behind_security/2026/05/08/birthday-problem.html))

Now the whole construction of the hash function can be divided into two layers: a collision-resistant compression function and a chain for messages of any length.

<br>
### Layer one.

<br>
### First try.

Let's take a secure symmetrical block cipher like DES (if you don't know what it is, take a look at my [previous post](https://0xkrt26.github.io/math_behind_security/2026/09/16/doodles-to-des.html).

<div markdown="0">
$$\text{DES} = \text{ENCRYPT}(\text{key}, \text{plaintext})$$
</div>

<div style="font-style: italic; color: #734f96;">

Today DES is no longer considered secure, so you'd have to use its successor AES or any other secure blockcipher. Security standards mentioned in this post have also changed.

</div>
<br>

DES takes 64 bits of plaintext and a 56-bit key. Therefore, the total input is:

<div markdown="0">
$$64 + 56 = 120 \text{ bits}$$
</div>

The output of the DES function is 64 bits long. 

We could've just stopped here, but DES is not preimage resistant. If you have an output, you can create a random key and still get a valid matching input by just "decrypting" DES. The easiest way to ensure that such "decryption" can't be done is to XOR the DES output with the original plaintext: 

<div markdown="0">
$$f(\text{key}, \text{plaintext}) = \text{ENCRYPT}(\text{key}, \text{plaintext}) \oplus \text{plaintext}$$
</div>

This is called a Davies-Meyer compression function. It makes the output random and therefore preimage resistant (irreversible). But Davies-Meyer alone can't handle big texts, so we should build further. 

The function <span markdown="0">$f_0$</span> has a 120-bit input, a 64-bit output and is preimage resistant. But it's not collision resistant yet. To make it secure against square root attacks (also called birthday attacks), we will need a 112-bit long output. To keep it simple, we can just concatenate two <span markdown="0">$f_0$</span> outputs and define it as a new function <span markdown="0">$F_1$</span>:

<div markdown="0">
$$F_1 = \text{First112bitsOf}\left( f(\text{"0"}, x) \,\|\, f(\text{"1"}, x) \right)$$
</div>

Though we must make sure that outputs are not identical, otherwise it won't give us much security - the attacker can easily see the pattern and reduce it back to 64 bits. We can make the input 119 bits instead of 120 and use the 120th bit as fixed padding: 0 for the left part and 1 for the right part to guarantee different outputs.

<div style="font-style: italic; color: #734f96;">

Why can't we just take the first 119 and last 119 bits of the input?
<br><br>
To ensure that inputs are truly different, we have to add some forced uniqueness. Imagine the input is 1111...11111, then both the first and the last 119 bits are just 1s. But if we force the first bit of each input to be different, we will definitely get different outputs.
<br><br>
Why do we take only 112 bits of the output?
<br><br>
First, we simply don't need more. In the era of DES, 112 bits were giving enough security against collision attacks. The number comes from a formula that shows how many operations it takes to find a collision for an <span markdown="0">$n$</span>-bit long hash function (about <span markdown="0">$2^{n/2}$</span> operations). Moreover, for long texts, the function <span markdown="0">$F_1$</span> will be applied several times, and since DES input is at most 120 bits, we will have to get rid of the rest anyway. Besides, we would want to add some new bits before each new cycle. How many bits we can add defines how efficient our function <span markdown="0">$F_1$</span> is. So the fewer bits we carry on from the last cycle, the better.

</div>
<br>

The output of <span markdown="0">$F_1$</span> is: 

<div markdown="0">
$$64 + 64 = 128 \text{ bits}$$
</div>

Since we don't need all the 128 bits, we can just take the first 112 bits and keep both efficiency and security.

Congratulations, we've built a collision-resistant compression function!

Now let's see how efficient it is for inputs longer than 119 bits. 

<div markdown="0">
$$\begin{aligned}
\text{input}_1 &: 119 \text{ bits} \\
\text{output}_1 &: 112 \text{ bits} \\
\text{input}_2 &: \text{output}_1 + \text{new bits} = 112 + 7 = 119
\end{aligned}$$
</div>

After one cycle we have a 112-bit output. Next input is 119 bits, 112 bits of which is output_1, which gives us only 7 new bits per iteration. Each iteration has two DES, so on average we use DES every 3.5 bits. Not very efficient and very time-consuming for long texts. Let's try and see if we can fix it.

<br>
### Second try

Let's see if using more DES per round can increase the efficiency of our function. Just like in the first try, we need to assign to each iteration its unique part. This time instead of 1 first bit (0, 1), we will have to use 2 first bits (00, 01, 11, 10), so each DES input can be only 118 bits. To get an output of 112 bits, we will have to concatenate two DES outputs. To satisfy all these conditions, we create a new function <span markdown="0">$F_2$</span>:

<div markdown="0">
$$F_2 = f\big(\text{"00"},\, f(\text{"01"}, x_1) \,\|\, x_2\big),\; f\big(\text{"10"},\, f(\text{"11"}, x_1) \,\|\, x_2\big)$$
</div>

Bit math will look like this:

<div markdown="0">
$$\begin{array}{lcl}
 & \text{"01"} + 118 \xrightarrow{\text{DES, XOR}} 64 \;\;+\;\; \text{"00"} + 54 \xrightarrow{\text{DES, XOR}} 64 & \\
172 \text{ bits} \rightarrow & & += 128 \text{ bits} \\
 & \text{"11"} + 118 \xrightarrow{\text{DES, XOR}} 64 \;\;+\;\; \text{"10"} + 54 \xrightarrow{\text{DES, XOR}} 64 &
\end{array}$$
</div>

<br>
<div style="font-style: italic; color: #734f96;">

Notice that here we leave the output 128 bits long, instead of cutting it down to only 112 bits how we did it before. Why? It was a part that I couldn't understand for some time, but it turned out to be a bit simpler than it sounded. 
<br><br>
Look at our bit math. We are squeezing 118 bits into 64 bits twice. This creates sort of a bottleneck, which compromises the randomness of the function and the security of the proof. It can happen that middle values collide, which will make it a little bit "easier" for the attacker to brute force. Merkle proves that keeping all 128 bits should return a security level of somewhat more than <span markdown="0">$2^{56}$</span> operations for <span markdown="0">$F_2$</span>.

</div>
<br>

During the first part we use 118 bits padded with "01" or "11". Those 54 bits that we have left from the input will be added to the outputs of the first part (also padded with "00" or "10") and become the new inputs for the second part. Exactly those 54 bits make our function more efficient:

<div markdown="0">
$$\begin{aligned}
172 - 128 &= 44 \\
44 : 4 &= 11
\end{aligned}$$
</div>

So our new <span markdown="0">$F_2$</span> takes 44 new bits per iteration and applies DES only every 11 bits. This is much better than what we had after our first try. But can it be even more efficient?

<br>
### Third try

So adding DES per cycle made our hash function more efficient. So why not use six DES? 

<div markdown="0">
$$F_3 = f\big(\text{"00"},\, \text{First59bitsOf}(f(\text{"100"}, x_1)) \,\|\, \text{First59bitsOf}(f(\text{"101"}, x_2))\big) \,\|\, f\big(\text{"01"},\, \text{First59bitsOf}(f(\text{"110"}, x_1)) \,\|\, \text{First59bitsOf}(f(\text{"111"}, x_2))\big)$$
</div>

The bit math is also analogous to what we had before, just the input is bigger now:

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

Now let's look at the efficiency:

<div markdown="0">
$$\begin{aligned}
234 - 128 &= 106 \\
106 : 6 &= 17.7
\end{aligned}$$
</div>

The new <span markdown="0">$F_3$</span> lets us add 106 new bits per iteration, which means we have to apply DES only every 17.7 bits. Now that's progress!

<br>
### Fourth, fifth, sixth try?

Now can it get even faster? Maybe you noticed that the bit math scheme looks like a binary tree. And theoretically it can grow even bigger. Though at some point its expansion won't make much of a difference for efficiency, as the distance between gained bits gets smaller and smaller (<span markdown="0">$3.5 \rightarrow 11 \rightarrow 17.7$</span>). 

More importantly, with each additional round of DES we compromise security more and more. For <span markdown="0">$F_2$</span>, the safety margin of 128 bits was giving security of a bit more than <span markdown="0">$2^{56}$</span> operations. For <span markdown="0">$F_3$</span>, the security level is already slightly below that standard. So for eight and more DES per iteration, we would have to come up with additional security methods.

Therefore, let's stop at <span markdown="0">$F_3$</span> for now. 

<br>
### Layer two.

We have built a compression function. Now if we apply <span markdown="0">$F_3$</span> to all the chunks of the message in the chain, we will get a hash function. The feeding machine looks like this:

<div markdown="0">
$$\begin{array}{ccccccccc}
 & & M_1 & & M_2 & & M_n & & \\
 & & \downarrow & & \downarrow & & \downarrow & & \\
\text{IV} & \rightarrow & f_1 & \rightarrow & f_2 & \rightarrow \cdots \rightarrow & f_n & \rightarrow & h(M)
\end{array}$$
</div>

This construction is called a Merkle-Damgård construction. It was developed simultaneously by multiple researchers and was named after those two who introduced it independently at CRYPTO'89: Ralph Merkle and Ivan Damgård. Both authors proved that the secure compression function f will create a secure hash function <span markdown="0">$h(M)$</span>. In this post I covered mostly Merkle's paper, as Damgård's proofs are much more formal and therefore more complicated for understanding. But for the curious and more advanced ones, here's a link to [Damgård's paper](https://www.researchgate.net/publication/221354712_A_Design_Principle_for_Hash_Functions). Now let's see how Merkle-Damgård construction works.

The IV is the initial value. For example, Merkle starts with <span markdown="0">$\text{IV} = 0$</span>. This IV and the first message chunk are fed into <span markdown="0">$f_1$</span> (<span markdown="0">$f_1, f_2, \ldots, f_n$</span> is the same compression function, for example, <span markdown="0">$F_3$</span>. The indices are used to differentiate between iterations). The output of <span markdown="0">$f_1$</span> and the new message chunk <span markdown="0">$M_2$</span> become the input of <span markdown="0">$f_2$</span>. This goes further as a chain until the end of the message. If the last block is too short, we pad it with extra bits.

Both Merkle and Damgård also append a length block as the last chunk <span markdown="0">$M_n$</span>. It can be the length of padding or (which is more beneficial for our proofs later) the length of the message. It is done to get different results even after padding. For example, before padding, you had two messages like this:

<div markdown="0">
$$\begin{aligned}
m_1 &= 010101100 \\
m_2 &= 0101011
\end{aligned}$$
</div>

After padding (let's say the chunk has to be 16 bits), we get the same sequences for both <span markdown="0">$m_1$</span> and <span markdown="0">$m_2$</span>:

<div markdown="0">
$$\begin{aligned}
m_1 &= \textbf{010101100}\,0000000 \\
m_2 &= \textbf{0101011}\,000000000
\end{aligned}$$
</div>

The length block will help to differentiate such inputs:

<div markdown="0">
$$\begin{aligned}
m_1 &= \textbf{010101100}\,000\,\textit{1001} \\
m_2 &= \textbf{0101011}\,00000\,\textit{0111}
\end{aligned}$$
</div>

<br>
### Some proofs that Merkle-Damgård construction works.

We created a chain out of compression functions. But how do we know it's still collision-resistant? We will prove it in two steps.

If compression function f is collision-resistant, then a hash function h is also collision-resistant for all inputs of the same length.

This step can be proved by induction. 

Basis:

If the input consists only of one chunk m, the compression function f will be applied only once. So in this case, the hash function h is just our compression function f. And if f is collision-resistant, so is h.

Induction:

From the basis we can assume that <span markdown="0">$f_n$</span> is collision-resistant for all the inputs <span markdown="0">$m_1, m_2, \ldots, m_n$</span>. Now let's prove that <span markdown="0">$f_{n+1}$</span> is also collision-resistant. The input of <span markdown="0">$f_{n+1}$</span> is the output of <span markdown="0">$f_n$</span> and the next input chunk <span markdown="0">$m_{n+1}$</span>. We can also write it like this:

<div markdown="0">
$$f_{n+1}(f_n, m_{n+1})$$
</div>

Assume there are two other values, <span markdown="0">$f_n'$</span> and <span markdown="0">$m_{n+1}'$</span>, that are not equal to <span markdown="0">$f_n$</span> and <span markdown="0">$m_{n+1}$</span> but have the same output for <span markdown="0">$f_{n+1}$</span>:

<div markdown="0">
$$\begin{aligned}
(f_n', m_{n+1}') &\neq (f_n, m_{n+1}) \\
f_{n+1}(f_n', m_{n+1}') &= f_{n+1}(f_n, m_{n+1})
\end{aligned}$$
</div>

This would mean that our compression function f is not collision resistant (collision resistance means that it's too hard to find two different inputs that produce the same output). So it contradicts the properties of f.

Now let's assume only one part of the input (either <span markdown="0">$f_n$</span> or <span markdown="0">$m_{n+1}$</span>) is identical to <span markdown="0">$f_n'$</span> and <span markdown="0">$m_{n+1}$</span>:

<div markdown="0">
$$f_n = f_n' \quad \text{or} \quad m_{n+1} = m_{n+1}'$$
</div>

Then, according to the hypothesis, another part of the input has to be identical too. Otherwise, the collision resistance assumption will be contradicted again.

Therefore, if <span markdown="0">$f_{n+1}$</span> outputs are identical, all the previous inputs and outputs must be identical too. So inputs <span markdown="0">$x$</span> and <span markdown="0">$x'$</span> have to be equal too. 

2. If a hash function h is collision-resistant for all the inputs of the same length, then it is collision-resistant for all the inputs of the different length (considering the input included length block)

This one is even easier to prove. Assume we have two inputs of different lengths: <span markdown="0">$x$</span> and <span markdown="0">$x'$</span>. Let's say <span markdown="0">$x$</span> is shorter than <span markdown="0">$x'$</span>, and their hashes happen to be equal:

<div markdown="0">
$$\begin{aligned}
x &\neq x' \\
|x| &< |x'| \\
h(x) &= h(x')
\end{aligned}$$
</div>

We know that <span markdown="0">$x$</span> is shorter than <span markdown="0">$x'$</span>. From the proof above, we know that for their hashes to match, <span markdown="0">$x$</span> has to be the postfix of <span markdown="0">$x'$</span> (last input chunks of <span markdown="0">$x'$</span> are input chunks of <span markdown="0">$x$</span>). But as we remember, the very last chunk has to have a length block, which means either by <span markdown="0">$x'$</span> or by <span markdown="0">$x$</span> this length block was supposed to differ. If it doesn't, the length was calculated incorrectly. 

To sum this proof up: If the hashes match, there was a collision in the length block, so either their lengths are equal (contradiction) or f is not collision-resistant (also a contradiction).

This proves that a hash function that is collision-resistant for inputs of the same length is also collision-resistant for inputs of different lengths, considering it has a length block appended.

<br>
### Why is Merkle-Damgård construction worth talking about?

Merkle-Damgård construction is a construction that became part of the modern hash functions. Its core: chaining, the Davies-Meyer step, a secure symmetric blockcipher inside - was used in MD5, SHA 1, SHA 2. Some of those hash functions were still broken later. Why? You'll have to wait for my next post to find out.

<br>
### My sources and further readings:

[Ralph Merkle "One Way Hash Functions and DES"](https://link.springer.com/content/pdf/10.1007/0-387-34805-0_40.pdf)
<br>
[Ivan Damgård "A Design Principle for Hash Functions"](https://www.researchgate.net/publication/221354712_A_Design_Principle_for_Hash_Functions)
<br>
[Ilya Mironov "Hash functions: Theory, attacks, and applications"](https://crypto.stanford.edu/~mironov/papers/hash_survey.pdf)

<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
