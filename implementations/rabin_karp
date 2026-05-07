# Constants used across functions
BASE = 256

def main():
    text = input("Please enter the text: ")
    pattern = input("Please enter your search pattern: ")
    
    try:
        prime = int(input("Please enter the prime number: "))
    except ValueError:
        print("Please enter a valid integer for the prime.")
        return

    m = len(text)
    n = len(pattern)

    # Initial hashes using your specific logic
    hash_text = first_hash(text, n, prime)
    hash_pattern = first_hash(pattern, n, prime)

    # We pass the data into the sliding window function
    matches = rolling_hash_search(text, pattern, m, n, hash_text, hash_pattern, prime)

    if matches > 0:
        print(f"Pattern is found a total of {matches} time(s).")
    else:
        print("Pattern is not found.")


def first_hash(string, length, prime):
    current_hash = 0
    for i in range(length):
        c = ord(string[i])
        # Following your formula: c * (256 ** (n-i-1))
        current_hash += c * (BASE ** (length - i - 1))
    return current_hash % prime


def rolling_hash_search(text, pattern, m, n, hash_text, hash_pattern, prime):
    match_count = 0
    # Pre-calculate (256**(n-1)) to use in the rolling formula
    h_multiplier = pow(BASE, n - 1, prime)

    for i in range(m - n + 1):
        # 1. Check for a match
        if hash_text == hash_pattern:
            # The "Check" (handling collisions)
            if text[i : i + n] == pattern:
                match_count += 1
                print(f"Pattern is found at position: {i}")

        # 2. Calculate hash for the next window (if we aren't at the end)
        if i < m - n:
            c_old = ord(text[i])
            c_new = ord(text[i + n])
            
            # Your logic: Remove high-order, shift left, add new low-order
            hash_text = (BASE * (hash_text - c_old * h_multiplier) + c_new) % prime
            
            # Ensure the hash isn't negative
            if hash_text < 0:
                hash_text += prime
                
    return match_count

if __name__ == "__main__":
    main()
