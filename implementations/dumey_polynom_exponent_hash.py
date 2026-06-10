#For this example let's use a Mersenne Prime M61:
prime = (2**61)-1

def main():
    message = input ("Please enter a string: ")
    #First convert string into x (ascii multiplied by powers of 256)
    x = int.from_bytes(message.encode(), byteorder='big')
    
    dumey(x)
    polynom(x)
    exponent(x)
    
def dumey(x):
    num = x%97
    
    print(f"Memory location out of 100 accessible memory locations(Arnold Dumey method): {num}")
    
def polynom(x):
    #Let's use a 5th degree polynom
    coeff = [989720, 89252, 539728, 802160, 135298, 44930]
    
    #Instead of calculating powers from standard polynomial form use Horner's method for a shortcut:
    #f(x)= (((((a5*x + a4)*x + a3)*x + a2)*x + a1)*x + a0)
    result = 0
    for c in coeff:
        #And don't forget to perform modulo operation every time to keep numbers small
        result = (result*x +c)%prime
        
    print(f"Hash value using a high-degree polynomial: {result}")
    
def exponent(x):
    a = 7
    result = pow(a, x, prime)
    
    print(f"Hash value using discrete exponentiation: {result}")
    
if __name__ == "__main__":
    main()
