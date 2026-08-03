import random
import hashlib

#Imagine you are Alice.
#This program helps you to compute a Merkle tree with 4 leaves. It also tels you which values to send to Bob and imitates the verification process.

#Note: the messages are not protected (the count of 0s is NOT appended to the original message to avoid confusion)

def main():
    seedkey = gen_seed()
    
    print("\nPrior arrangements:")
    
    print("\nThese are your private keys:")
    priv_keys1 = gen_priv_keys(seedkey, 1)
    priv_keys2 = gen_priv_keys(seedkey, 5)
    priv_keys3 = gen_priv_keys(seedkey, 9)
    priv_keys4 = gen_priv_keys(seedkey, 1)
    all_priv_keys = [priv_keys1, priv_keys2, priv_keys3, priv_keys4]
    
    print("\nThese are your public keys:")
    pub_keys1 = comp_pub_keys(priv_keys1, 1)
    pub_keys2 = comp_pub_keys(priv_keys2, 2)
    pub_keys3 = comp_pub_keys(priv_keys3, 3)
    pub_keys4 = comp_pub_keys(priv_keys4, 4)
    pub_keys = [pub_keys1, pub_keys2, pub_keys3, pub_keys4]
    
    lvl1, lvl2, root = comp_tree(pub_keys)

    for k in range(4):
        m = input("\nPlease enter your message (only 3 bits): ")
        if len(m) != 3 or not all(c in '01' for c in m):
            print("Message must be exactly 3 bits (e.g. 101). Skipping this signature slot.")
            continue
        print_path(k, pub_keys, lvl1, lvl2, root, all_priv_keys[k], m)

    print("\nYou ran out of signatures. Please start from the beginning to generate a new tree.")


def gen_seed():
    seedkey = random.getrandbits(200)
    bin_seedkey = format(seedkey, f"0{200}b")
    print(f"Your seedkey: {bin_seedkey}")
    return bin_seedkey

#This example uses the same hash function both for F and for H.
def gen_priv_keys(seedkey, n):
    priv_keys = []
    for j in range(4):
        print(f"\nFor m{j+n}:")
        for i in range(3):
            data = f"{seedkey}_{i}_{j+n}".encode()
            x_ij = hashlib.sha256(data).hexdigest()
            print(f"x_{i+1},{j+n} = {x_ij}")
            priv_keys.append(x_ij)
    return priv_keys


def comp_pub_keys(priv_keys, n):
    pub_keys = []
    for var in priv_keys:
        y_ij = hashlib.sha256(var.encode()).hexdigest()
        pub_keys.append(y_ij)
    print(f"Y_{n} = {pub_keys}")
    return pub_keys


def comp_tree(pub_keys):
    print("\nLeaf nodes H(i,i):")
    lvl1 = []
    for i in range(4):
        n = leaf_node(i + 1, pub_keys[i])
        lvl1.append(n)

    print("\nInner nodes H(i,j):")
    n1 = inner_node(1, 2, lvl1[0], lvl1[1])
    n2 = inner_node(3, 4, lvl1[2], lvl1[3])
    lvl2 = [n1, n2]

    print("\nRoot (SEND TO BOB):")
    root = inner_node(1, 4, lvl2[0], lvl2[1])
    return lvl1, lvl2, root


def leaf_node(i, Y_i):
    data = f"{i}_{i}_{Y_i}".encode()
    n = hashlib.sha256(data).hexdigest()
    print(f"H({i},{i}) = {n}")
    return n

def inner_node(i, j, left, right):
    data = f"{i}_{j}_{left}_{right}".encode()
    n = hashlib.sha256(data).hexdigest()
    print(f"H({i},{j}) = {n}")
    return n


def print_path(k, pub_keys, lvl1, lvl2, root, priv_keys, m):
    print(f"\n--- Authentication path for message {k + 1} ---")
    h_leaf = lvl1[k]

    if k == 0:
        print(f"Send: Y_1, H(2,2), H(3,4)")
        computed_inner = inner_node(1, 2, h_leaf, lvl1[1])
        computed_root  = inner_node(1, 4, computed_inner, lvl2[1])
    elif k == 1:
        print(f"Send: Y_2, H(1,1), H(3,4)")
        computed_inner = inner_node(1, 2, lvl1[0], h_leaf)
        computed_root  = inner_node(1, 4, computed_inner, lvl2[1])
    elif k == 2:
        print(f"Send: Y_3, H(4,4), H(1,2)")
        computed_inner = inner_node(3, 4, h_leaf, lvl1[3])
        computed_root  = inner_node(1, 4, lvl2[0], computed_inner)
    
    else:
        print(f"Send: Y_4, H(3,3), H(1,2)")
        computed_inner = inner_node(3, 4, lvl1[2], h_leaf)
        computed_root  = inner_node(1, 4, lvl2[0], computed_inner)

    print(f"\n---Bob verifies the root R---")
    if computed_root == root:
        print("Message is authentic")
    else:
        print("Authentication failed")

    # Reveal private keys according to Lamport-Diffie:
    n_offset = k * 3 + 1   
    print(f"\nReveal these private keys for message '{m}' to Bob:")
    if m == '000':
        print("No private keys to reveal.")
    else:
        for j_bit, bit in enumerate(m):
            i = int(bit)
            key_index = j_bit * 2 + i
            j_label = n_offset + j_bit
            if i == 1:
                print(f"  bit {j_bit + 1} = {bit}  →  x_{j_label} = {priv_keys[key_index]}")
        print(f"\n---Bob verifies each revealed x by computing F(x) and checking against y_j---")



if __name__ == "__main__":
    main()
