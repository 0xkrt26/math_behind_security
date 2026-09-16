def main():
    while True:
        print("Please, choose one from the following:")
        print("1. Caesar encryption")
        print("2. Caesar decryption")
        print("3. Vigenère encryption")
        print("4. Vigenère decryption")
        choice = input ("Please, enter the number: ")
        if (choice == "1"):
            caesar_en()
            break
        elif (choice == "2"):
            caesar_de()
            break
        elif (choice == "3"):
            vig_en()
            break
        elif (choice == "4"):
            vig_de()
            break
        else:
            print("Invalid choice, please try again.\n")

def caesar_en():
    text = plaintext("en")
    k = input("Please, enter the key: ")
    try:
        k = int(k)
    except ValueError:
        print("Key must be a number. If you want to use a letter, please, start again and choose Option 3.")
        caesar_en()
        return

    else:
        
        new_text = []

        for i in range (len(text)):
            c = (ord(text[i].lower()) - 97 + k) % 26
            #97 so that a=0
            new_text.append(chr(ord('A') + c))

        print(f"Ciphertext: {''.join(new_text)}")

def caesar_de():
    text = plaintext("de")
    k = input("Please, enter the key: ")
    try:
        k = int(k)
    except ValueError:
        print("Key must be a number. If you want to use a letter, please, start again and choose Option 4.")
        caesar_de()
        return

    else:
        new_text = []

        for i in range (len(text)):
            c = (ord(text[i].lower()) - 97 - k) % 26
            new_text.append(chr(ord('A') + c))

        print(f"Plaintext: {''.join(new_text)}")

def vig_en():
    text = plaintext("en")

    k = input("Please, enter the key: ")
    if not k.isalpha():
        print("Key must contain letters only.")
        vig_en()
        return
    k = list(k)

    n = 0
    new_text = []
    for i in range (len(text)):
        c = (ord(text[i].lower()) - 97 + ord(k[n].lower()) - 97) % 26
        new_text.append(chr(ord('A') + c))
        n = (n+1) % len(k)   

    print(f"Ciphertext: {''.join(new_text)}")

def vig_de():
    text = plaintext("de")

    k = input("Please, enter the key: ")
    if not k.isalpha():
        print("Key must contain letters only.")
        vig_de()
        return
    k = list(k)

    n = 0
    new_text = []

    for i in range (len(text)):
        c = (ord(text[i].lower()) - 97 - (ord(k[n].lower()) - 97)) % 26
        new_text.append(chr(ord('A') + c))
        n = (n+1) % len(k)   

    print(f"Plaintext: {''.join(new_text)}")


def plaintext(type):
    if type == "en":
        text = input("Please, enter your plaintext: ")
    elif type == "de":
        text = input("Please, enter your ciphertext: ")

    clean_text = []
    for char in text:
        # Only adds letters to the clean text
        if char.isalpha():
            clean_text.append(char)
   
    return clean_text


if __name__ == "__main__":
    main()
