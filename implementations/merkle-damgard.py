from Crypto.Cipher import DES

#Reserve bits for length block
len_bits = 64
#New bits added each round
chunk_size = 106
IV = 0

def main():
  message = input("Please, enter the message: ")
  message_bytes = message.encode('utf-8')

  msg_int = bytes_to_int(message_bytes)
  msg_length = len(message_bytes) * 8

  #Calculate padding
  remainder = (msg_length + len_bits) % chunk_size
  padding_bits = (chunk_size - remainder) % chunk_size

  # Create message | zero_padding | original_length
  padded_msg_len = msg_length + padding_bits + len_bits
  padded_msg = (msg_int << (padding_bits + len_bits)) | msg_length

  n = padded_msg_len // chunk_size

  result = IV   #First chaining value (128 bits)

  for i in range(n):
        #Extract the 106-bit chunk from the message:
        shift = padded_msg_len - (i + 1) * chunk_size
        chunk = (padded_msg >> shift) & ((1 << chunk_size) - 1)

        #Concatenate running result with new bits
        block_input = (result << chunk_size) | chunk
        result = F(block_input)

  print("Hash function:", result)

def encrypt(plaintext, key):
  cipher = DES.new(key, DES.MODE_ECB)
  return cipher.encrypt(plaintext)

#Bit extraction:
def first_117_of(x):
  return x >> 117

def last_117_of(x):
  return x & ((1 << 117) - 1)

def first_59_of(x):
  return x >> 5

#For encryption int needs to be converted into bytes
def int_to_bytes(i, length):
  return i.to_bytes(length, byteorder='big')

#Convert back to int for math operations
def bytes_to_int(b):
  return int.from_bytes(b, byteorder='big')

#DES in Python ignores the lowest bit of every key byte
#Put 7 real key bits into each byte
def make_des_key(key_56_bits):
  key = 0
  for i in range(8):
    seven_bits = (key_56_bits >> (49 - 7 * i)) & 0x7F
    key = (key << 8) | (seven_bits << 1)
  return int_to_bytes(key, 8)

def f(padding, user_input):
  payload_len = 120 - len(padding)
  #padding | input
  block = (int(padding, 2) << payload_len) | user_input

  plaintext = block >> 56
  key = block & ((1 << 56) - 1)

  encrypted = encrypt(int_to_bytes(plaintext, 8), make_des_key(key))
  #Davies-Meyer:
  return bytes_to_int(encrypted) ^ plaintext

#Our F_3 function:
def F(user_input):
  x1 = first_117_of(user_input)
  x2 = last_117_of(user_input)

  a = f("100", x1)
  a = first_59_of(a)
  b = f("101", x2)
  b = first_59_of(b)
  ab = (a << 59) | b
  p1 = f("00", ab)

  c = f("110", x1)
  c = first_59_of(c)
  d = f("111", x2)
  d = first_59_of(d)
  cd = (c << 59) | d
  p2 = f("01", cd)

  return (p1 << 64) | p2

if __name__ == "__main__":
    main()