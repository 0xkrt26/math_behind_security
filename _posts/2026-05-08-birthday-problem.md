---
title: "When is your birthday? - The Math Behind Hash Collisions"
date: 2026-05-08
---
<div style="font-style: italic; color: #3474B4;">

Note: This post turned out a little different from the previous ones. It's more of an essay than a dialogue. I tried restructuring it multiple times, but it kept wanting to be linear. And you know, sometimes the topic just has its own shape, so I left it like this. Enjoy!

</div>
<br>
What is the probability that you are sharing the same birthday with people around you? Well, if you're alone in the room, then it's most certainly zero. Also the more people there are around, the higher the chances should get. But what if I told you that in a room with only 23 people there's already a 50% chance for two of them to have matching birthdays? And I can quite easily prove it with just school math.

What does it mean to calculate a probability for at least two people to have a matching birthday? It's the same as calculating the  inverse probability for no one in the group to be born on the same day:

$$P(\text{at least one match}) = 1 - P(\text{no matches})$$

No matches means every birthday is unique. That means the first person can be born on any of the 365 days, person 2 must be born on a different day, so he has only 364 days to choose from, person 3 has only 363 days to choose from... and so on. So let's take n for the number of people in the room and derive this formula:

$$P(\text{no matches}) = \frac{365}{365} \cdot \frac{364}{365} \cdot \frac{363}{365} \dots \frac{365-n+1}{365} = \frac{365!}{365^n(365-n)!}$$

for n=23:

$$P(\text{no matches}) = \frac{365!}{365^{23}(365-23)!}= 0.4927$$ 

...or about 50%.

Another formula that you can often find on the internet after searching for the Birthday Paradox is an approximation based on calculating the probability for all the connections existing between 23 people:

$$1 - \frac{1}{365} = \frac{364}{365}$$

$$P = \left( \frac{364}{365} \right)^{\binom{23}{2}} \approx 0.4995$$

But let's take a look at something much cooler.

You see, the problem with those formulas is that they can only be used to find a pair that has the same birthday. But how rare is it for three out of 60 people to have matching birthdays?

In the 1930s, the employees of the math bureau of one of the insurance companies tried to find that out, since among their 60 coworkers, three shared the same birthday. Their calculations most probably looked something like this:

In the room with 60 people, Alice, Bob, and Ray have birthdays on the same day. The probability for their birthdays to match is

$$ \frac{1}{365} \cdot \frac{1}{365} \cdot \frac{1}{365} = \left( \frac{1}{365} \right)^3 $$

For the remaining 57 coworkers, the probability will be:

$$\left(\frac{364}{365}\right)^{57}$$

Also instead of Alice, Bob, and Ray, it could have been Mikel, Ida, and Ana or any other triple:

$$\binom{60}{3}$$

Now all there's to do left is to multiply all of those probabilities:

$$\binom{60}{3} \cdot \left(\frac{364}{365}\right)^{57} \cdot \left(\frac{1}{365}\right)^3 \approx 0.0006$$

So the result that math bureau employees got is only a few thousandth. And their calculations were right. But also... wrong.

And in 1939 an Austrian mathematician Richard von Mises explained why. His article "Über Aufteilungs- und Besetzungswahrscheinlichkeiten" was printed in the academic Journal of the University of Istanbul, where after being classified as Jewish and escaping the Nazi government, he became the professor of mathematics.

Von Mises didn't just change the calculations. He completely changed the perspective on the problem. The thing is, the human brain is quite self-centered and often misses the whole picture. The math bureau employees were trying to find the probability of the specific event: three people having birthday on one pre-chosen day. But what if instead we ask: "How often should we expect this type of event to occur in general?" 

Imagine there are 365 boxes in front of you. 60 balls are being thrown in these boxes randomly. Math bureau employees choose the third box. For them success is having three or more balls in  that exact box. Von Mises suggests watching all the boxes and count how many of them will have three or more balls in the end. It's clear that his definition of success is much broader, and therefore, the probability is also much higher.

<div style="font-style: italic; color: #3474B4;">
  
Mises calls such probability an occupancy probability, as it shows how many of the boxes or, in our case, days are occupied one, two, three, etc. times.

</div>
<br>
Let's take a look at his calculations. For this example we'll have n days and k people in the room.

The probability for each n to be occupied is 1/n, so for all k people it turns into:

$$\underbrace{\frac{1}{n} \times \frac{1}{n} \times \dots \times \frac{1}{n}}_{k \text{ times}} = \frac{1}{n^k} = n^{-k}$$

which is how we calculate the chance of one exact sequence happening.

Then we'll build the probability p1 for all the birthday distributions that have s people on the first calendar day. There are $$\binom{k}{s}$$ ways to choose s out of k people, and for the remaining n-1 days we have (k-s) remaining employees that can be distributed like this:

$$(n-1)^{k-s}$$

The complete formula for p1 is:

$$p_1 = \binom{k}{s} \cdot n^{-k} \cdot (n-1)^{k-s}$$

<br>
<br>
<div style="font-style: italic; color: #3474B4;">
  
We can also translate 'p1' into Bernoulli trials:

$$\begin{aligned}
p_1 &= \binom{k}{s} \cdot (n-1)^{k-s} \cdot n^{-k} \\
&= \binom{k}{s} \cdot \frac{(n-1)^{k-s}}{n^k} \\
&= \binom{k}{s} \cdot \frac{(n-1)^{k-s}}{n^s \cdot n^{k-s}} \\
&= \binom{k}{s} \cdot \left(\frac{1}{n}\right)^s \cdot \left(\frac{n-1}{n}\right)^{k-s} \\
&= \binom{k}{s} \cdot \left(\frac{1}{n}\right)^s \cdot \left(1 - \frac{1}{n}\right)^{k-s}
\end{aligned}$$

$$p = \frac{1}{n} \quad \text{(probability of success)}$$

$$q = 1 - \frac{1}{n} \quad \text{(probability of failure)}$$

This leaves us with the formula of the Bernoulli sequence we learned at high school.

</div>
<br>
<br>

The same formula works for p2, p3,.. pn and gives us: 

$$p_1 + p_2 + p_3 + \dots + p_n = n \cdot p_1$$

This sum covers all the distributions that have at least one day with s birthdays. All of them that have more than one such day will be counted multiple times. For example, if there are two days with s birthdays, the distribution will be counted twice, for three days - three times, and so on. 

<br>
<br>
<div style="font-style: italic; color: #3474B4;">
  
It's like having a lot of arrays that represent the number of birthdays on each day (in this example we'll have only four days):<br>

For s = 7:<br>

Distributions (Birthdays per day):

$$\begin{aligned}
\text{Distribution}_1 &: [8, \mathbf{7}, 4, 6] \\
\text{Distribution}_2 &: [4, 5, 3, 2] \\
\text{Distribution}_3 &: [\mathbf{7}, 4, 5, \mathbf{7}]
\end{aligned}$$

Arrays (The days being checked for exactly $s$):

$$\begin{aligned}
\text{Array}_1 &: [8, 4, \mathbf{7}] \quad \text{(Day 1)} \\
\text{Array}_2 &: [\mathbf{7}, 5, 4] \quad \text{(Day 2)} \\
\text{Array}_3 &: [4, 3, 5] \quad \text{(Day 3)} \\
\text{Array}_4 &: [6, 2, \mathbf{7}] \quad \text{(Day 4)}
\end{aligned}$$

Distribution1 appears only in Array2, therefore will be counted only once, while Distribution3 is a part of both Array1 and Array4, therefore will be counted twice.

</div>
<br>
<br>

This means that $$n \cdot p1$$ provides us with a weighted sum and can be interpreted as an expected value 'E(x_s)'. All we have to do is paste the formula for p1 that we've already derived before:

$$E(x_s) = n \cdot \binom{k}{s} \cdot (n-1)^{k-s} \cdot n^{-k}$$

or

$$E(x_s) = n \cdot \binom{k}{s} \cdot \left(\frac{1}{n}\right)^s \cdot \left(1 - \frac{1}{n}\right)^{k-s}$$

To prove that it's much more common for a group of 60 people to have a triple match of birthdays, let's try this formula with our numbers:

$$\begin{aligned}
n &= 365 \\
k &= 60 \\
s &= 3 \\
E(x_3) &= 365 \times \frac{60!}{3! \times (60-3)!} \times \left(\frac{1}{365}\right)^3 \times \left(1 - \frac{1}{365}\right)^{60-3} \approx 0.2196
\end{aligned}$$

or about 0.22, which aligns with the value von Mises gives in his paper.

It might seem that '0.22' is too little, but it actually means that, on average, in every 4-5 groups of 60 people, there will be about one triply-shared birthday. 

$$\frac{1}{0.22} \approx 4.5454$$

Doesn't seem that rare anymore, does it? Especially if we compare it to the possibility of a few thousandths, that, on the other hand, will happen only about once in every 1500-2000 groups of 60 people. Now that's actually rare.

<div style="font-style: italic; color: #3474B4;">
  
Of course, these calculations don't consider seasonal variation in birth density, twins, selection bias, leap years etc. which von Mises himself explicitly mentions at the end of his article. If you look at statistics, in the Northern Hemisphere, children are more often born in summer; in the U.S., they're more likely to be conceived on Christmas and New Year's Eve; and due to C-sections and induced labor, Mondays and Tuesdays also have higher birth rates.

</div>
<br>
In his paper, von Mises goes on to calculate the exact probability distribution, but the expected value is all we need to prove that the math bureau was looking at the problem through the wrong lens. 

The expected value also allows us to get the approximate representation of the number of collisions that will occur in the hash table depending on the values we choose.

Moreover, there is a special brute-force attack in cybersecurity called the Birthday Attack that uses the math behind the Birthday Problem to create collisions that will break the system. The attacker generates random inputs until two of them produce the same hash output. That will happen after about √n attempts. For example, SHA-256 has $$2^{256}$$ outputs. That would requier $$2^{128}$$ attempts to crack. Notice that the attacker is not waiting for a specific hash value to occur double, any collision would be enough to stop the system from working. 

We have already talked a bit about collisions in the hash tables [last time.](https://0xkrt26.github.io/math_behind_security/2026/04/28/the-accidental-ancestor-Luhn-algorithm.html) Now we know that the math behind hash tables' collisions is the math behind the Birthday Problem: days become table fields, people turn into hashes, but the calculations remain unchanged.


### My sources and further readings: 
[Richard Von Mises, "Über Aufteilungs- und Besetzungswahrscheinlichkeiten" (p. 313)](http://alexander.shen.free.fr/vonMises_64_SelectedPapersVol2OCR.pdf)
[Richard von Mises Biography](https://link.springer.com/content/pdf/10.1007/978-3-0348-8787-8_13)
[University of Connecticut lecture](https://www.phys.uconn.edu/~rozman/Courses/P2400_24S/downloads/birthday.pdf)

<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
