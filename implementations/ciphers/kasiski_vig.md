## How to break the Vigenère cipher?

The hardest part is to find the length of the key. To do that, we can use the Kasiski examination published by Friedrich Kasiski in 1863.

### Kasiski examination.

To find the key length of a Vigenère key, we can use the Kasiski examination. To demonstrate how it works, I'll be using the encrypted intro of [my post]() about ciphers:

DEFLNFLZUROAJYEGHSIEKLBOPLLRMEPXPWNPRRBLOHZKNPWYRQZBAWAUKVXRZMPUWXCFGPTZQTFPOIJWAVAWVYUWNRAFPLJVKLBRVPGMKPTRXOHRFHAWBDDMMYNILSEEWVOPFISHOXKGVATLPSHVOJVZTRLXGHSCMKASMPNTVZGDFXNSKPBQMLIOBFLBSXDJKFCMWGFSIBSTVARLLENFFEXBGSDPEWAWPREQWHZKTRQSXJSIATLZAXJYRKAMFHXYVWPVTDUSFYBVHUZOGSZXVCFDKIELVBLMOIXAZSMNELWRFMKPHSSHDPEWHZRQGXVBVWGJKOGLTAOWJDFXVIYQWCFHXPSWLKEHLWKHKPXYPUEAXSYTQVMGJWFLXGECTSMIKIPLHLGLFZTLQNVYZTAQBQXYPWKQHLMNWVOPFBUHHITMFVPFAHTZBVPOUWCIAAVBLYOCXZTXVBUHZMFXVVBLROKTBXPWA

1. Find repeating sequences in a text.

The longer the repeating sequence is, the better.

DEFLNFLZUROAJYEGHSIEKLBOPLLRMEPXPWNPRRBLOHZKNPWYRQZBAWAUKVXRZMPUWXCFGPTZQTFPOIJWAVAWVYUWNRAFPLJVKLBRVPGMKPTRXOHRFHAWBDDMMYNILSEE*WVOPF*ISHOXKGVATLPSHVOJVZTRLXGHSCMKASMPNTVZGDFXNSKPBQMLIOBFLBSXDJKFCMWGFSIBSTVARLLENFFEXBGS*DPEW*AWPREQWHZKTRQSXJSIATLZAXJYRKAMFHXYVWPVTDUSFYBVHUZOGSZXVCFDKIELVBLMOIXAZSMNELWRFMKPHSSH*DPEW*HZRQGXVBVWGJKOGLTAOWJDFXVIYQWCFHXPSWLKEHLWKHKPXYPUEAXSYTQVMGJWFLXGECTSMIKIPLHLGLFZTLQNVYZTAQBQXYPWKQHLMN*WVOPF*BUHHITMFVPFAHTZBVPOUWCIAAVBLYOCXZTXVBUHZMFXVVBLROKTBXPWA

2. Calculate the distance between them.

Sequence:	Distance:
WVOPF		288
DPEW		90

3. Find all possible key lengths.

The biggest (distance itself) and the smallest (1) are highly unlikely to be the actual length. Therefore, we're left with these dividers:

288: 144 - 96 - 72 - 48 - 36 - 32 - 24 - 18 - 16 - 12 - 9 - 8 - 6 - 4 - 3 - 2
90: 45 - 30 - 18 - 15 - 10 - 9 - 6 - 5 - 3 - 2

4. Determine the key candidate.

To do that, let's leave only common dividers from the next step:

18 - 9 - 6 - 3 - 2

The key length is most likely 18, but if it's not, we can always repeat the next steps with other dividers.

### Caesar groups analysis.

The key length is 18, so let's make 18 groups:

DIRAQAXEPAMFGQFZOSKFPEQMAOR 		Most common letter is A
EERUTFOESSLSSSHOIHOHUCNNHCO 		Most common letter is S
FKBKFPHWHMIIDXXGXDGXETVWTXK 		Most common letter is X
LLLVPLRVVPOBPJYSAPLPASYVZZT 		Most common letter is L
NBOXOJFOONBSESVZZETSXMZOBTB 		Most common letter is O
FOHRIVHPJTFTWIWXSWAWSITPVXX 		Most common letter is W
LPZZJKAFVVLVAAPVMHOLYKAFPVP 		Most common letter is V
ZLKMWLWIZZBAWTVCNZWKTIQBOBW 		Most common letter is W
ULNPABBSTGSRPLTFERJEQPBUUUA 		Most common letter is U
RRPUVRDHRDXLRZDDLQDHVLQHWH 		Most common letter is R
OMWWAVDOLFDLEAUKWGFLMHXHCZ 		Most common letter is W
AEYXWPMXXXJEQXSIRXXWGLYIIM 		Most common letter is X
JPRCVGMKGNKNWJFEFVVKJGPTAF 		Most common letter is J
YXQFYMYGHSFFHYYLMBIHWLWMAX 		Most common letter is Y
EPZGUKNVSKCFZRBVKVYKFFKFVV 		Most common letter is V
GWBPWPIACPMEKKVBPWQPLZQVBV 		Most common letter is P
HNATNTLTMBWXTAHLHGWXXTHPLY 		Most common letter is T
SPWZRRSLKQGBRMUMSJCYGLLFYL 		Most common letter is L

But how do we determine the key? We could have just assumed that the most common letter in each group must be E, just like it is in the English language, but if we did that, we would have gotten:

A=E => KEY = 0-4 = -4 = 22 = W
S=E => KEY = 18-4 = 14 = O	
X=E => KEY = 23-4 = 19 = T			
L=E => KEY = 11-4 = 7 = H	
O=E => KEY = 14-4 = 10 = K	
W=E => KEY = 22-4 = 18 = S	
V=E => KEY = 21-4 = 17 = R	
W=E => KEY = 22-4 = 18 = S	
U=E => KEY = 20-4 = 16 = Q	
R=E => KEY = 17-4 = 13 = N	
W=E => KEY = 22-4 = 18 = S	
X=E => KEY = 23-4 = 19 = T	
J=E => KEY = 9-4 = 5 = F	
Y=E => KEY = 24-4 = 20 = U	
V=E => KEY = 21-4 = 17 = R	
P=E => KEY = 15-4 = 11 = L	
T=E => KEY = 19-4 = 15 = P	
L=E => KEY = 11-4 = 7 = H	

And as a person who encrypted the original text, I can assure you the key is either a word or a phrase, not just gibberish. 

*This could have worked, though, if our text sample were longer.*

This is why we should take a look not at just one most common letter but preferably 3-4 of them. From here we have two options. 

### Option 1.

We can try assigning the second, third, and so on most common letters *in the group* to E, which would work faster for the first group, for example:

Most frequent letters:	AFQ

For A=*E*:
	F = B
	Q = M
	
For F=*E*:
	A = Z
	Q = P

For Q=*E*:
	A = *O*
	F = *T*		

In bold I marked the first 9 most frequent letters of the English alphabet (frequency is higher than 50%). We can see that Q=E is most probably the right combination, so:

KEY = 16 - 4 = 12 = M

### Option 2.

Or we can try assigning the most common letter of the group to the second, third, and so on most common letters *in the English alphabet*. Let's try it on the second group:

Most frequent letters:	SHO

For S=E:
	H = V
	O = B

For S=T:
	H = *I*
	O = P

For S=A:
	H = Z
	O = F

...

For S=S:
	H = *H*
	O = *O*

*In our example most of the groups are solved faster with the first option*

After we determined the key for each row, we can build the whole key, which, for our example, was:

MATHBEHINDSECURITY

Now we just use this key to decrypt the ciphertext using the [Vigenère decoder]() and get the original text:

REMEMBERHOWWHENYOUWEREAKIDYOUANDYOURFRIENDSCAMEUPWITHYOUROWNSECRETALPHABETMINECONSISTEDOUTOFWEIRDDOODLESTHATLOOKEDTOOALIKEWASUSEDONLYAFEWTIMESANDSOONFORGOTTENBUTMOSTIMPORTANTLYTHISALPHABETFULFILLEDITSPURPOSEITALLOWEDUSKIDSTOCOMMUNICATESECRETLYWITHEACHOTHERUSINGACODEKNOWNONLYTOUSASECRETSOCIETYOFFRIENDSTHOUGHKIDSARENOTTHEONLYONESWHOWANTTOHIDETHEIRSECRETSINTHEADULTWORLDSUCHCODEISCALLEDACIPHERORANENCRYPTIONFUNCTIONANDONLYTHEPERSONWHOHASARIGHTKEYGETSACCESSTOTHEHIDDENINFORMATION
