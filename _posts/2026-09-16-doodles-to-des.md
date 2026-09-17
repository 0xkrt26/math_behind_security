---
title: "How to Keep a Secret — From Doodles to DES"
date: 2026-09-16
---

<style>
mjx-container[display="true"] { text-align: left !important; margin-left: 0 !important; }
.scheme-container { width: 100%; max-width: 800px; margin: 0 auto; }
.scheme-container svg { width: 100%; height: auto; display: block; }
.box { fill: #cdd6df; }
.s-box { fill: #e2e8f0; stroke: #a0aab5; stroke-width: 1.5; }
.text { fill: #333333; font-size: 14px; font-weight: 600; text-anchor: middle; alignment-baseline: middle; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.small-text { fill: #333333; font-size: 11px; font-weight: 500; text-anchor: middle; alignment-baseline: middle; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.line { stroke: #a0aab5; stroke-width: 1.5; fill: none; }
.dashed-line { stroke: #a0aab5; stroke-width: 1.5; fill: none; stroke-dasharray: 5, 5; }
.pin { stroke: #a0aab5; stroke-width: 1; }
</style>

<div style="font-style: italic; color: #734f96;">

All the implementations can be found in <a href="https://github.com/0xkrt26/math_behind_security/tree/main/implementations/ciphers">my GitHub Repository</a>.

</div>
<br>

Remember how when you were a kid, you and your friends came up with your own secret alphabet? Mine consisted out of weird doodles that looked too alike, was used only a few times, and soon forgotten. But most importantly, this alphabet fulfilled its purpose. It allowed us kids to communicate secretly with each other, using a code known only to us - a secret society of friends.

Though kids are not the only ones who want to hide their secrets. In the adult world, such code is called a cipher or an encryption function. Only the person who has a right key gets access to the hidden information.

<br>
### What encryption functions are there?

I'm sure you have heard of the Caesar cipher, one of the oldest ciphers in history. It creates a new alphabet by shifting letters of the old one by n positions. So if we had a word, CAESAR, and we would want to encrypt it with a key n=3, we would get:

```
CAESAR -> FDHVDU
```

This is a very simple encryption. Therefore, it's also very easy to crack either by brute force (just trying out all 26 keys) or by linguistic analysis that looks at letter frequencies in the plaintext and compares them to the letter frequencies in the cipher. So, for example, the most common letter in the English language is "E", therefore it's most likely that the most frequently occurring letter in the cipher might be "E". (An example of the program that breaks Caesar cipher can be found [here](https://github.com/0xkrt26/math_behind_security/blob/main/implementations/ciphers/break_caesar.py))

Another example is a Vigenère cipher. This one is more complicated, as the key is a word out of letters, so basically two alphabets are being shifted separately. Both encryption and decryption can be performed using the same Vigenère square:

<div style="overflow-x: auto; font-family: monospace; font-size: 12px; line-height: 1.5; margin: 1rem 0;">
<pre>
   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
A  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
B  B C D E F G H I J K L M N O P Q R S T U V W X Y Z A
C  C D E F G H I J K L M N O P Q R S T U V W X Y Z A B
D  D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
E  E F G H I J K L M N O P Q R S T U V W X Y Z A B C D
F  F G H I J K L M N O P Q R S T U V W X Y Z A B C D E
G  G H I J K L M N O P Q R S T U V W X Y Z A B C D E F
H  H I J K L M N O P Q R S T U V W X Y Z A B C D E F G
I  I J K L M N O P Q R S T U V W X Y Z A B C D E F G H
J  J K L M N O P Q R S T U V W X Y Z A B C D E F G H I
K  K L M N O P Q R S T U V W X Y Z A B C D E F G H I J
L  L M N O P Q R S T U V W X Y Z A B C D E F G H I J K
M  M N O P Q R S T U V W X Y Z A B C D E F G H I J K L
N  N O P Q R S T U V W X Y Z A B C D E F G H I J K L M
O  O P Q R S T U V W X Y Z A B C D E F G H I J K L M N
P  P Q R S T U V W X Y Z A B C D E F G H I J K L M N O
Q  Q R S T U V W X Y Z A B C D E F G H I J K L M N O P
R  R S T U V W X Y Z A B C D E F G H I J K L M N O P Q
S  S T U V W X Y Z A B C D E F G H I J K L M N O P Q R
T  T U V W X Y Z A B C D E F G H I J K L M N O P Q R S
U  U V W X Y Z A B C D E F G H I J K L M N O P Q R S T
V  V W X Y Z A B C D E F G H I J K L M N O P Q R S T U
W  W X Y Z A B C D E F G H I J K L M N O P Q R S T U V
X  X Y Z A B C D E F G H I J K L M N O P Q R S T U V W
Y  Y Z A B C D E F G H I J K L M N O P Q R S T U V W X
Z  Z A B C D E F G H I J K L M N O P Q R S T U V W X Y
</pre>
</div>

Alternatively, we could imagine all letters as numbers:

$$E_i = (P_i + K_i) \bmod 26$$
$$D_i = (C_i - K_i) \bmod 26$$

where $P_i$ = letter of plaintext, $K_i$ = key letter, $C_i$ = letter of ciphertext.

Though Vigenère can still be cracked. The only hard part is to find out the length of the key. There're different ways to do it. On my GitHub I explained how to crack Vigenère cipher using [Kasiski examination](https://github.com/0xkrt26/math_behind_security/blob/main/implementations/ciphers/kasiski_vig.md) and wrote an implementation for both [Caesar and Vigenère ciphers](https://github.com/0xkrt26/math_behind_security/blob/main/implementations/ciphers/encryption%26decryption.py).

<br>
### DES

Another type of cipher is a block cipher. In 1970s, one of the most famous block ciphers, DES (Data Encryption Standard), was created by IBM. For many years DES was used as a default protection of bank cards, financial transactions via ATMs, and SWIFT (Society for Worldwide Interbank Financial Telecommunication).

It's a block cipher, so to encrypt the text, you need to first divide it into 64-bit blocks (if needed, pad the last block by adding the required amount of zeroes). Each block is then encrypted according to this scheme:

<div class="scheme-container">
<svg viewBox="100 0 700 1120" xmlns="http://www.w3.org/2000/svg">

    <!-- Data Start: Plaintext & IP -->
    <rect x="200" y="30" width="120" height="30" rx="2" class="box" />
    <text x="260" y="46" class="text">Plaintext</text>
    <path d="M260 60 L260 85" class="line" />
    <circle cx="260" cy="100" r="15" class="box" />
    <text x="260" y="101" class="small-text">IP</text>
    <path d="M260 115 L260 135 L200 135 L200 150" class="line" />
    <path d="M260 115 L260 135 L320 135 L320 150" class="line" />
    <rect x="180" y="150" width="40" height="30" rx="2" class="box" />
    <text x="200" y="166" class="small-text">L0</text>
    <rect x="300" y="150" width="40" height="30" rx="2" class="box" />
    <text x="320" y="166" class="small-text">R0</text>

    <!-- Key Start & PC-1 -->
    <rect x="580" y="30" width="120" height="30" rx="2" class="box" />
    <text x="640" y="46" class="text">Key</text>
    <path d="M640 60 L640 85" class="line" />
    <circle cx="640" cy="100" r="15" class="box" />
    <text x="640" y="101" class="small-text">PC-1</text>
    <path d="M640 115 L640 135 L580 135 L580 150" class="line" />
    <path d="M640 115 L640 135 L700 135 L700 150" class="line" />
    <rect x="560" y="150" width="40" height="30" rx="2" class="box" />
    <text x="580" y="166" class="small-text">C0</text>
    <rect x="680" y="150" width="40" height="30" rx="2" class="box" />
    <text x="700" y="166" class="small-text">D0</text>

    <!-- Key Round 1: Left Shifts -->
    <path d="M580 180 L580 205" class="line" />
    <path d="M700 180 L700 205" class="line" />
    <ellipse cx="580" cy="220" rx="35" ry="15" class="box" />
    <text x="580" y="221" class="small-text">Left shift</text>
    <ellipse cx="700" cy="220" rx="35" ry="15" class="box" />
    <text x="700" y="221" class="small-text">Left shift</text>

    <path d="M580 235 L580 250" class="line" />
    <path d="M700 235 L700 250" class="line" />
    <rect x="560" y="250" width="40" height="30" rx="2" class="box" />
    <text x="580" y="266" class="small-text">C1</text>
    <rect x="680" y="250" width="40" height="30" rx="2" class="box" />
    <text x="700" y="266" class="small-text">D1</text>

    <!-- Data Round 1 -->
    <path d="M200 180 L200 425" class="line" />
    <circle cx="200" cy="440" r="15" class="box" />
    <text x="200" y="441" class="text">+</text>

    <path d="M320 240 L380 240 L380 265" class="line" />
    <circle cx="380" cy="280" r="15" class="box" />
    <text x="380" y="281" class="text">E</text>
    <path d="M380 295 L380 320 L405 320" class="line" />
    <circle cx="420" cy="320" r="15" class="box" />
    <text x="420" y="321" class="text">+</text>

    <path d="M580 280 L580 320 L500 320" class="line" />
    <path d="M700 280 L700 320 L500 320" class="line" />
    <circle cx="485" cy="320" r="15" class="box" />
    <text x="485" y="321" class="small-text">PC-2</text>
    <path d="M470 320 L435 320" class="line" />

    <path d="M580 320 L580 365" class="line" />
    <path d="M700 320 L700 365" class="line" />
    <ellipse cx="580" cy="380" rx="35" ry="15" class="box" />
    <text x="580" y="381" class="small-text">Left shift</text>
    <ellipse cx="700" cy="380" rx="35" ry="15" class="box" />
    <text x="700" y="381" class="small-text">Left shift</text>
    <path d="M580 395 L580 420" class="line" />
    <path d="M700 395 L700 420" class="line" />
    <rect x="560" y="420" width="40" height="30" rx="2" class="box" />
    <text x="580" y="436" class="small-text">Cn</text>
    <rect x="680" y="420" width="40" height="30" rx="2" class="box" />
    <text x="700" y="436" class="small-text">Dn</text>

    <!-- S-boxes S1..S8 -->
    <path d="M420 335 L420 355" class="line" />
    <rect x="293" y="360" width="254" height="40" rx="4" class="s-box" />
    <!-- S1 -->
    <line x1="295.4" y1="355" x2="295.4" y2="360" class="pin" /><line x1="300.6" y1="355" x2="300.6" y2="360" class="pin" /><line x1="305.8" y1="355" x2="305.8" y2="360" class="pin" /><line x1="311" y1="355" x2="311" y2="360" class="pin" /><line x1="316.2" y1="355" x2="316.2" y2="360" class="pin" /><line x1="321.4" y1="355" x2="321.4" y2="360" class="pin" />
    <line x1="299" y1="400" x2="299" y2="405" class="pin" /><line x1="305" y1="400" x2="305" y2="405" class="pin" /><line x1="311" y1="400" x2="311" y2="405" class="pin" /><line x1="317" y1="400" x2="317" y2="405" class="pin" />
    <circle cx="308" cy="380" r="11" fill="#e2e8f0" /><text x="308" y="381" class="small-text">S1</text>
    <!-- S2 -->
    <line x1="327.4" y1="355" x2="327.4" y2="360" class="pin" /><line x1="332.6" y1="355" x2="332.6" y2="360" class="pin" /><line x1="337.8" y1="355" x2="337.8" y2="360" class="pin" /><line x1="343" y1="355" x2="343" y2="360" class="pin" /><line x1="348.2" y1="355" x2="348.2" y2="360" class="pin" /><line x1="353.4" y1="355" x2="353.4" y2="360" class="pin" />
    <line x1="331" y1="400" x2="331" y2="405" class="pin" /><line x1="337" y1="400" x2="337" y2="405" class="pin" /><line x1="343" y1="400" x2="343" y2="405" class="pin" /><line x1="349" y1="400" x2="349" y2="405" class="pin" />
    <circle cx="340" cy="380" r="11" fill="#e2e8f0" /><text x="340" y="381" class="small-text">S2</text>
    <!-- S3 -->
    <line x1="359.4" y1="355" x2="359.4" y2="360" class="pin" /><line x1="364.6" y1="355" x2="364.6" y2="360" class="pin" /><line x1="369.8" y1="355" x2="369.8" y2="360" class="pin" /><line x1="375" y1="355" x2="375" y2="360" class="pin" /><line x1="380.2" y1="355" x2="380.2" y2="360" class="pin" /><line x1="385.4" y1="355" x2="385.4" y2="360" class="pin" />
    <line x1="363" y1="400" x2="363" y2="405" class="pin" /><line x1="369" y1="400" x2="369" y2="405" class="pin" /><line x1="375" y1="400" x2="375" y2="405" class="pin" /><line x1="381" y1="400" x2="381" y2="405" class="pin" />
    <circle cx="372" cy="380" r="11" fill="#e2e8f0" /><text x="372" y="381" class="small-text">S3</text>
    <!-- S4 -->
    <line x1="391.4" y1="355" x2="391.4" y2="360" class="pin" /><line x1="396.6" y1="355" x2="396.6" y2="360" class="pin" /><line x1="401.8" y1="355" x2="401.8" y2="360" class="pin" /><line x1="407" y1="355" x2="407" y2="360" class="pin" /><line x1="412.2" y1="355" x2="412.2" y2="360" class="pin" /><line x1="417.4" y1="355" x2="417.4" y2="360" class="pin" />
    <line x1="395" y1="400" x2="395" y2="405" class="pin" /><line x1="401" y1="400" x2="401" y2="405" class="pin" /><line x1="407" y1="400" x2="407" y2="405" class="pin" /><line x1="413" y1="400" x2="413" y2="405" class="pin" />
    <circle cx="404" cy="380" r="11" fill="#e2e8f0" /><text x="404" y="381" class="small-text">S4</text>
    <!-- S5 -->
    <line x1="423.4" y1="355" x2="423.4" y2="360" class="pin" /><line x1="428.6" y1="355" x2="428.6" y2="360" class="pin" /><line x1="433.8" y1="355" x2="433.8" y2="360" class="pin" /><line x1="439" y1="355" x2="439" y2="360" class="pin" /><line x1="444.2" y1="355" x2="444.2" y2="360" class="pin" /><line x1="449.4" y1="355" x2="449.4" y2="360" class="pin" />
    <line x1="427" y1="400" x2="427" y2="405" class="pin" /><line x1="433" y1="400" x2="433" y2="405" class="pin" /><line x1="439" y1="400" x2="439" y2="405" class="pin" /><line x1="445" y1="400" x2="445" y2="405" class="pin" />
    <circle cx="436" cy="380" r="11" fill="#e2e8f0" /><text x="436" y="381" class="small-text">S5</text>
    <!-- S6 -->
    <line x1="455.4" y1="355" x2="455.4" y2="360" class="pin" /><line x1="460.6" y1="355" x2="460.6" y2="360" class="pin" /><line x1="465.8" y1="355" x2="465.8" y2="360" class="pin" /><line x1="471" y1="355" x2="471" y2="360" class="pin" /><line x1="476.2" y1="355" x2="476.2" y2="360" class="pin" /><line x1="481.4" y1="355" x2="481.4" y2="360" class="pin" />
    <line x1="459" y1="400" x2="459" y2="405" class="pin" /><line x1="465" y1="400" x2="465" y2="405" class="pin" /><line x1="471" y1="400" x2="471" y2="405" class="pin" /><line x1="477" y1="400" x2="477" y2="405" class="pin" />
    <circle cx="468" cy="380" r="11" fill="#e2e8f0" /><text x="468" y="381" class="small-text">S6</text>
    <!-- S7 -->
    <line x1="487.4" y1="355" x2="487.4" y2="360" class="pin" /><line x1="492.6" y1="355" x2="492.6" y2="360" class="pin" /><line x1="497.8" y1="355" x2="497.8" y2="360" class="pin" /><line x1="503" y1="355" x2="503" y2="360" class="pin" /><line x1="508.2" y1="355" x2="508.2" y2="360" class="pin" /><line x1="513.4" y1="355" x2="513.4" y2="360" class="pin" />
    <line x1="491" y1="400" x2="491" y2="405" class="pin" /><line x1="497" y1="400" x2="497" y2="405" class="pin" /><line x1="503" y1="400" x2="503" y2="405" class="pin" /><line x1="509" y1="400" x2="509" y2="405" class="pin" />
    <circle cx="500" cy="380" r="11" fill="#e2e8f0" /><text x="500" y="381" class="small-text">S7</text>
    <!-- S8 -->
    <line x1="519.4" y1="355" x2="519.4" y2="360" class="pin" /><line x1="524.6" y1="355" x2="524.6" y2="360" class="pin" /><line x1="529.8" y1="355" x2="529.8" y2="360" class="pin" /><line x1="535" y1="355" x2="535" y2="360" class="pin" /><line x1="540.2" y1="355" x2="540.2" y2="360" class="pin" /><line x1="545.4" y1="355" x2="545.4" y2="360" class="pin" />
    <line x1="523" y1="400" x2="523" y2="405" class="pin" /><line x1="529" y1="400" x2="529" y2="405" class="pin" /><line x1="535" y1="400" x2="535" y2="405" class="pin" /><line x1="541" y1="400" x2="541" y2="405" class="pin" />
    <circle cx="532" cy="380" r="11" fill="#e2e8f0" /><text x="532" y="381" class="small-text">S8</text>

    <!-- P Permutation -->
    <path d="M420 405 L420 425" class="line" />
    <circle cx="420" cy="440" r="15" class="box" />
    <text x="420" y="441" class="text">P</text>
    <path d="M405 440 L215 440" class="line" />

    <!-- Crossover round 1 -->
    <path d="M200 455 L200 460 L320 490 L320 500" class="line" />
    <path d="M320 180 L320 460 L200 490 L200 500" class="line" />

    <rect x="180" y="500" width="40" height="30" rx="2" class="box" />
    <text x="200" y="516" class="small-text">L1</text>
    <rect x="300" y="500" width="40" height="30" rx="2" class="box" />
    <text x="320" y="516" class="small-text">R1</text>

    <!-- DASHED ROUNDS -->
    <path d="M580 450 L580 570" class="dashed-line" />
    <path d="M700 450 L700 570" class="dashed-line" />
    <path d="M200 530 L200 550" class="line" />
    <path d="M320 530 L320 550" class="line" />
    <path d="M200 550 L200 695" class="dashed-line" />
    <circle cx="200" cy="710" r="15" class="box" />
    <text x="200" y="711" class="text">+</text>
    <path d="M320 570 L380 570 L380 585" class="dashed-line" />
    <circle cx="380" cy="600" r="15" class="box" />
    <text x="380" y="601" class="text">E</text>
    <path d="M380 615 L380 630 L405 630" class="dashed-line" />
    <circle cx="420" cy="630" r="15" class="box" />
    <text x="420" y="631" class="text">+</text>
    <path d="M580 570 L580 630 L500 630" class="dashed-line" />
    <path d="M700 570 L700 630 L500 630" class="dashed-line" />
    <circle cx="485" cy="630" r="15" class="box" />
    <text x="485" y="631" class="small-text">PC-2</text>
    <path d="M470 630 L435 630" class="dashed-line" />
    <path d="M420 645 L420 655" class="dashed-line" />
    <rect x="370" y="655" width="100" height="30" rx="3" class="box" />
    <text x="420" y="671" class="small-text">S-boxes</text>
    <path d="M420 685 L420 695" class="dashed-line" />
    <circle cx="420" cy="710" r="15" class="box" />
    <text x="420" y="711" class="text">P</text>
    <path d="M405 710 L215 710" class="dashed-line" />
    <path d="M200 725 L200 735 L320 750 L320 760" class="dashed-line" />
    <path d="M320 550 L320 735 L200 750 L200 760" class="dashed-line" />
    <path d="M580 630 L580 700" class="dashed-line" />
    <path d="M700 630 L700 700" class="dashed-line" />
    <path d="M580 700 L580 710" class="line" />
    <path d="M700 700 L700 710" class="line" />
    <ellipse cx="580" cy="725" rx="35" ry="15" class="box" />
    <text x="580" y="726" class="small-text">Left shift</text>
    <ellipse cx="700" cy="725" rx="35" ry="15" class="box" />
    <text x="700" y="726" class="small-text">Left shift</text>
    <path d="M580 740 L580 760" class="line" />
    <path d="M700 740 L700 760" class="line" />
    <rect x="560" y="760" width="40" height="30" rx="2" class="box" />
    <text x="580" y="776" class="small-text">C16</text>
    <rect x="680" y="760" width="40" height="30" rx="2" class="box" />
    <text x="700" y="776" class="small-text">D16</text>
    <rect x="180" y="760" width="40" height="30" rx="2" class="box" />
    <text x="200" y="776" class="small-text">L15</text>
    <rect x="300" y="760" width="40" height="30" rx="2" class="box" />
    <text x="320" y="776" class="small-text">R15</text>

    <!-- FINAL ROUND 16 -->
    <path d="M200 790 L200 965" class="line" />
    <circle cx="200" cy="980" r="15" class="box" />
    <text x="200" y="981" class="text">+</text>
    <path d="M320 830 L380 830 L380 845" class="line" />
    <circle cx="380" cy="860" r="15" class="box" />
    <text x="380" y="861" class="text">E</text>
    <path d="M380 875 L380 890 L405 890" class="line" />
    <circle cx="420" cy="890" r="15" class="box" />
    <text x="420" y="891" class="text">+</text>
    <path d="M580 790 L580 890 L500 890" class="line" />
    <path d="M700 790 L700 890 L500 890" class="line" />
    <circle cx="485" cy="890" r="15" class="box" />
    <text x="485" y="891" class="small-text">PC-2</text>
    <path d="M470 890 L435 890" class="line" />
    <path d="M420 905 L420 925" class="line" />
    <rect x="370" y="925" width="100" height="30" rx="3" class="box" />
    <text x="420" y="941" class="small-text">S-boxes</text>
    <path d="M420 955 L420 965" class="line" />
    <circle cx="420" cy="980" r="15" class="box" />
    <text x="420" y="981" class="text">P</text>
    <path d="M405 980 L215 980" class="line" />
    <path d="M200 995 L200 1005 L320 1025 L320 1040" class="line" />
    <path d="M320 790 L320 1005 L200 1025 L200 1040" class="line" />
    <rect x="180" y="1040" width="40" height="30" rx="2" class="box" />
    <text x="200" y="1056" class="small-text">L16</text>
    <rect x="300" y="1040" width="40" height="30" rx="2" class="box" />
    <text x="320" y="1056" class="small-text">R16</text>

</svg>
</div>

Now about each step in details.

<br>
### Initial and final permutations

Before the beginning of the encryption, plaintext undergoes a small transformation called Initial Permutation. It just changes the position of each bit of plaintext in a predetermined pattern:

```
IP
58 50 42 34 26 18 10  2
60 52 44 36 28 20 12  4
62 54 46 38 30 22 14  6
64 56 48 40 32 24 16  8
57 49 41 33 25 17  9  1
59 51 43 35 27 19 11  3
61 53 45 37 29 21 13  5
63 55 47 39 31 23 15  7
```

This IP is reversed after the encryption process is completed. An inverse pattern is applied:

```
IP⁻¹
40  8 48 16 56 24 64 32
39  7 47 15 55 23 63 31
38  6 46 14 54 22 62 30
37  5 45 13 53 21 61 29
36  4 44 12 52 20 60 28
35  3 43 11 51 19 59 27
34  2 42 10 50 18 58 26
33  1 41  9 49 17 57 25
```

<div style="font-style: italic; color: #734f96;">

A lot of sources claim IP to be an additional security measurement, which is completely wrong. It is a deterministic, invertible, publicly known operation. Its only purpose was to ease hardware implementation in the 1970s. Now we would have zero need for it. So IP and IP⁻¹ solve rather an electrical engineering problem than a cryptographic one.

</div>

<br>
### Feistel network

In 1973 German-born cryptographer Horst Feistel came up with a symmetric block cipher construction that became a crucial part of DES. The encryption pattern that you've already seen in the scheme can also be represented as an equation:

$$L_r = R_{r-1}$$
$$R_r = L_{r-1} \oplus f(R_{r-1},\, K_r)$$

<div style="font-style: italic; color: #734f96;">

$\oplus$ here stands for a bitwise addition modulo 2 (= in a binary system) called XOR.

</div>

The Feistel cipher uses a round function for encryption, which means that the same transformation is applied multiple times. Usually a Feistel network consists of more than 3 rounds. DES performs 16 rounds of encryption for additional security.

<br>
### Key and subkeys

Each round $r$ needs a 48-bit subkey $K_r$. Subkeys are generated from a 64 bit key, that consists out of a 56 random bits sequence (actual key) plus 8 parity check bits (for detecting possible errors). Creation of these subkeys starts with a permutation PC-1 (yes, there'll be a lot of permutations today so get ready). It doesn't only switch the positions of the bits but also divides the key in two parts, C and D:

```
C
57 49 41 33 25 17  9
 1 58 50 42 34 26 18
10  2 59 51 43 35 27
19 11  3 60 52 44 36

D
63 55 47 39 31 23 15
 7 62 54 46 38 30 22
14  6 61 53 45 37 29
21 13  5 28 20 12  4
```

Then to both parts we apply a circular shift left operation, which basically moves all the bits to the left by n positions. The bits that have "fallen out" are attached on the right. For example, if n is 2:

```
10 1111  <<2
1111 10
```

How big n is depends on the round r:

| Round | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|-------|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|----|
| n     | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2  | 2  | 2  | 2  | 2  | 2  | 1  |

After each round a subkey is produced by permutating C and D again, this time using PC-2:

```
PC-2
14 17 11 24  1  5
 3 28 15  6 21 10
23 19 12  4 26  8
16  7 27 20 13  2
41 52 31 37 47 55
30 40 51 45 33 48
44 49 39 56 34 53
46 42 50 36 29 32
```

<br>
### E-Function

Now the right 32-bit-long block R0 has to be transformed into a 48-bit-long one to match a subkey. During this process, certain bits are doubled and moved. This expansion E is just like IP, a publicly known one, and is defined through this table:

```
E
32  1  2  3  4  5
 4  5  6  7  8  9
 8  9 10 11 12 13
12 13 14 15 16 17
16 17 18 19 20 21
20 21 22 23 24 25
24 25 26 27 28 29
28 29 30 31 32  1
```

Now when both the right block and subkey have the same length, we just XOR them and feed the result into the S-boxes.

<div style="font-style: italic; color: #734f96;">

Well, why not just generate a 32-bit subkey in the first place and save these extra steps?

As we've already said, an S-box is a 6-to-4-bit transformation, which means the number of bits has to be divisible by six. 48 bits were found to be the best number of bits since it gives enough s-boxes for security without affecting the efficiency. Moreover, such transformation contributes to diffusion and therefore provides additional security.

</div>

<br>
### S-boxes

The function used inside the Feistel network of DES is called a substitution box, or S-box. It is a 6-to-4-bit substitution mapping that makes encryption nonlinear and therefore secure as it deletes 2 bits of information each time. Now in simple language: What is this substitution box?

Imagine it as an actual box with a tiny person inside of it. We put in a small piece of paper with six bits on it, for example:

```
101110
```

A person inside an S-box splits the input in two parts:

```
Outer bits (1st and last):  1 _ _ _ _ 0  →  10
Inner bits (middle four):   _ 0 1 1 1 _  →  0111
```

Then a little worker looks at the table on the wall and finds a field that corresponds to the outer and inner bits of the input:

<div style="overflow-x: auto; margin: 1rem 0;">
<table style="font-family: monospace; font-size: 12px; border-collapse: collapse; min-width: 600px;">
<thead>
<tr>
  <th style="padding:4px 6px;border:1px solid #ccc;"></th>
  <th style="padding:4px 6px;border:1px solid #ccc;">0000</th><th style="padding:4px 6px;border:1px solid #ccc;">0001</th><th style="padding:4px 6px;border:1px solid #ccc;">0010</th><th style="padding:4px 6px;border:1px solid #ccc;">0011</th><th style="padding:4px 6px;border:1px solid #ccc;">0100</th><th style="padding:4px 6px;border:1px solid #ccc;">0101</th><th style="padding:4px 6px;border:1px solid #ccc;">0110</th><th style="padding:4px 6px;border:1px solid #ccc;"><strong>0111</strong></th><th style="padding:4px 6px;border:1px solid #ccc;">1000</th><th style="padding:4px 6px;border:1px solid #ccc;">1001</th><th style="padding:4px 6px;border:1px solid #ccc;">1010</th><th style="padding:4px 6px;border:1px solid #ccc;">1011</th><th style="padding:4px 6px;border:1px solid #ccc;">1100</th><th style="padding:4px 6px;border:1px solid #ccc;">1101</th><th style="padding:4px 6px;border:1px solid #ccc;">1110</th><th style="padding:4px 6px;border:1px solid #ccc;">1111</th>
</tr>
</thead>
<tbody>
<tr><td style="padding:4px 6px;border:1px solid #ccc;">00</td><td style="padding:4px 6px;border:1px solid #ccc;">0010</td><td style="padding:4px 6px;border:1px solid #ccc;">1100</td><td style="padding:4px 6px;border:1px solid #ccc;">0100</td><td style="padding:4px 6px;border:1px solid #ccc;">0001</td><td style="padding:4px 6px;border:1px solid #ccc;">0111</td><td style="padding:4px 6px;border:1px solid #ccc;">1010</td><td style="padding:4px 6px;border:1px solid #ccc;">1011</td><td style="padding:4px 6px;border:1px solid #ccc;">0110</td><td style="padding:4px 6px;border:1px solid #ccc;">1000</td><td style="padding:4px 6px;border:1px solid #ccc;">0101</td><td style="padding:4px 6px;border:1px solid #ccc;">0011</td><td style="padding:4px 6px;border:1px solid #ccc;">1111</td><td style="padding:4px 6px;border:1px solid #ccc;">1101</td><td style="padding:4px 6px;border:1px solid #ccc;">0000</td><td style="padding:4px 6px;border:1px solid #ccc;">1110</td><td style="padding:4px 6px;border:1px solid #ccc;">1001</td></tr>
<tr><td style="padding:4px 6px;border:1px solid #ccc;">01</td><td style="padding:4px 6px;border:1px solid #ccc;">1110</td><td style="padding:4px 6px;border:1px solid #ccc;">1011</td><td style="padding:4px 6px;border:1px solid #ccc;">0010</td><td style="padding:4px 6px;border:1px solid #ccc;">1100</td><td style="padding:4px 6px;border:1px solid #ccc;">0100</td><td style="padding:4px 6px;border:1px solid #ccc;">0111</td><td style="padding:4px 6px;border:1px solid #ccc;">1101</td><td style="padding:4px 6px;border:1px solid #ccc;">0001</td><td style="padding:4px 6px;border:1px solid #ccc;">0101</td><td style="padding:4px 6px;border:1px solid #ccc;">0000</td><td style="padding:4px 6px;border:1px solid #ccc;">1111</td><td style="padding:4px 6px;border:1px solid #ccc;">1010</td><td style="padding:4px 6px;border:1px solid #ccc;">0011</td><td style="padding:4px 6px;border:1px solid #ccc;">1001</td><td style="padding:4px 6px;border:1px solid #ccc;">1000</td><td style="padding:4px 6px;border:1px solid #ccc;">0110</td></tr>
<tr><td style="padding:4px 6px;border:1px solid #ccc;"><strong>10</strong></td><td style="padding:4px 6px;border:1px solid #ccc;">0100</td><td style="padding:4px 6px;border:1px solid #ccc;">0010</td><td style="padding:4px 6px;border:1px solid #ccc;">0001</td><td style="padding:4px 6px;border:1px solid #ccc;">1011</td><td style="padding:4px 6px;border:1px solid #ccc;">1010</td><td style="padding:4px 6px;border:1px solid #ccc;">1101</td><td style="padding:4px 6px;border:1px solid #ccc;">0111</td><td style="padding:4px 6px;border:1px solid #ccc;background:#e8f4e8;"><strong>1000</strong></td><td style="padding:4px 6px;border:1px solid #ccc;">1111</td><td style="padding:4px 6px;border:1px solid #ccc;">1001</td><td style="padding:4px 6px;border:1px solid #ccc;">1100</td><td style="padding:4px 6px;border:1px solid #ccc;">0101</td><td style="padding:4px 6px;border:1px solid #ccc;">0110</td><td style="padding:4px 6px;border:1px solid #ccc;">0011</td><td style="padding:4px 6px;border:1px solid #ccc;">0000</td><td style="padding:4px 6px;border:1px solid #ccc;">1110</td></tr>
<tr><td style="padding:4px 6px;border:1px solid #ccc;">11</td><td style="padding:4px 6px;border:1px solid #ccc;">1011</td><td style="padding:4px 6px;border:1px solid #ccc;">1000</td><td style="padding:4px 6px;border:1px solid #ccc;">1100</td><td style="padding:4px 6px;border:1px solid #ccc;">0111</td><td style="padding:4px 6px;border:1px solid #ccc;">0001</td><td style="padding:4px 6px;border:1px solid #ccc;">1110</td><td style="padding:4px 6px;border:1px solid #ccc;">0010</td><td style="padding:4px 6px;border:1px solid #ccc;">1101</td><td style="padding:4px 6px;border:1px solid #ccc;">0110</td><td style="padding:4px 6px;border:1px solid #ccc;">1111</td><td style="padding:4px 6px;border:1px solid #ccc;">0000</td><td style="padding:4px 6px;border:1px solid #ccc;">1001</td><td style="padding:4px 6px;border:1px solid #ccc;">1010</td><td style="padding:4px 6px;border:1px solid #ccc;">0100</td><td style="padding:4px 6px;border:1px solid #ccc;">0101</td><td style="padding:4px 6px;border:1px solid #ccc;">0011</td></tr>
</tbody>
</table>
</div>

He takes a new piece of paper and writes there:

```
1000
```

and hands it out back to us. This way we got the following transformation:

```
101110 → 1000
```

It's crucial that each out of eight S-boxes has its own table for 6-to-4 bit substitution. This ensures that each bit undergoes as many transformations as possible.

<br>
### Additional permutation

The result that was handed out to us from the s-boxes needs to be permuted. Even though this permutation P is predefined and publicly known, it will still serve as an extra protection from an attacker, as it ensures that in the next round a bit goes into another S-box.

```
P
16  7 20 21
29 12 28 17
 1 15 23 26
 5 18 31 10
 2  8 24 14
32 27  3  9
19 13 30  6
22 11  4 25
```

Now that we've covered each step in detail, look at the scheme in the beginning again. It should look much less scary now.

<br>
### Decryption of DES

To decrypt DES, use the same scheme as we used for encryption: just pretend that ciphertext is now your plaintext and repeat the whole "encryption". The only difference between encryption and decryption is that the subkeys need to be applied in reverse order: start with $K_{16}$, finish with $K_1$.

<br>
### If all the permutations and steps are publicly known, can't we just trace back the plaintext?

No. The main security mechanisms are S-boxes: they take in 6 bits but give out only 4, which means some information gets lost. If we wanted to trace it back, we would have multiple candidates for each four bits we got on the exit. And even if we decided to just trace each candidate back, not only it would've been too many candidates after 16 rounds of Feistel network, but also we would've had to crack a XOR operation between text and an unknown subkey that comes right before the S-boxes. The combination of an unknown input and information loss is exactly the reason why DES has never been broken mathematically.

However, the algorithm was still retired on 19.05.2005 simply because hardware became capable enough to crack an encryption by brute-forcing all possible $2^{56}$ keys. Now the Advanced Encryption Standard (AES) is used instead, but this is a topic for another time.

<br>
### Are encryption and hash functions the same thing?

No. Even though both hash and encryption functions provide certain security, each of them has distinct properties and therefore different areas of application.

Hash functions are irreversible, which makes them perfect for authentication (a detailed explanation with an example can be found in my previous [post](https://0xkrt26.github.io/math_behind_security/2026/08/03/merkle-tree.html) about digital signatures).

Encryption has, in turn, a reverse process called decryption, which reveals the original plaintext to anyone who has a key. This makes the cipher a perfect tool for chatting in privacy. For example, each time you start a new chat in WhatsApp, you see something like "Messages and calls are end-to-end encrypted."

<br>
### Then how are ciphers connected to the history of hashes we have been talking about in all the previous posts?

You see, I was about to cover the next step in the history of hashes, but that construction was based on DES, so I thought a separate post that introduces the concept of ciphers properly might be a good idea. Small spoiler for the future post: a compression function combined with a symmetric block cipher (such as DES) gives you a cryptographically secure hash function. Exactly our goal!

<br>
### My sources and further readings:
[Official DES description by NIST](https://csrc.nist.gov/files/pubs/fips/46-3/final/docs/fips46-3.pdf)
<br>
[Chapter 7 from the Handbook of Applied Cryptography, by A. Menezes, P. van Oorschot, and S. Vanstone](https://cacr.uwaterloo.ca/hac/about/chap7.pdf)
<br>
[Short history of DES](https://www.cryptomuseum.com/crypto/algo/des/index.htm)

<script>
MathJax = { tex: { inlineMath: [["$","$"],["\\(","\\)"]] } };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
