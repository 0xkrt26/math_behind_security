import collections

def main():
    while True:
        print("Please, choose how you want to crack the Caesar ciphre:")
        print("1. Brute force")
        print("2. Language analyse")
        choice = input("Please, enter the number: ")
        if choice=="1":
            caesar1()
            break
        elif choice=="2":
            caesar2()
            break
        else:
            print("Invalid choice, please try again.\n")

def caesar1():
    text = ciphertxt()
    plaintext =[]

    for i in range(26):
        for j in range (len(text)):
            c = (ord(text[j].lower()) - 97 - i) % 26
            plaintext.append(chr(ord('A') + c))
        print(f"Key: {i+1}, plaintext: {''.join(plaintext)}")
        plaintext =[]
        
def caesar2():
    text = ciphertxt()
    
    common = collections.Counter(c.lower() for c in text).most_common(5)
    
    for i in range (5):
        if i >= len(common): 
            print ("The text is too short. Please, try brute force.")
            break 
        else:
            letter = common[i][0]
            #[0] twice to return just the letter
            key = ord(letter.lower()) - 97 - 4
            #if a=0, then e=4

            plaintext = []
            for j in range (len(text)):
                p = (ord(text[j].lower()) - 97 - key) % 26
                plaintext.append(chr(ord('A') + p))
    
            ans = input (f"Is this a plaintext: {''.join(plaintext)}, y/n?") 
            if ans == "y":
                print (f"Plaintext: {''.join(plaintext)}")
                break  
            if ans == "n" and i==4:
                print ("Sorry, the language analysis didn't work. Please, try using brute force.")

def ciphertxt():
    text = input("Please, enter your ciphertext: ")

    clean_text = []
    for char in text:
        # Only adds letters to the clean text
        if char.isalpha():
            clean_text.append(char)
   
    return clean_text




if __name__ == "__main__":
    main()
