'''

File: sha256.py
Author: Brandon Chua, Brandon Greenaway, Nicholas Harris
Purpose:  Program recreating Secure Hashing Algorithm 256-bit (SHA-256), a hashing algorithm that creates
          a message digest for the purposes of data encryption and integrity.
Version:  1.0 - Nov 16, 2024
Resources: Wikipedia SHA2 page, W3 schools for python function documentation, ChatGPT for some bug checking and small parts like the list splicing and stuct.pack/struct.unpack usage.

'''

import struct, os

# Initialize hash values
h0 = 0x6a09e667
h1 = 0xbb67ae85
h2 = 0x3c6ef372
h3 = 0xa54ff53a
h4 = 0x510e527f
h5 = 0x9b05688c
h6 = 0x1f83d9ab
h7 = 0x5be0cd19

# Initialize round constants
k = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def rotr(x, n): return (x >> n | x << (32-n))

def sha256(message):
    # SHA-256 Hashing Algorithm
    global h0, h1, h2, h3, h4, h5, h6, h7, k
    
    # Pre-processing: padding the message
    lenpadding = struct.pack(">Q", (len(message) * 8))
    message += b'\x80'
    message += b'\x00' * ((56 - (len(message)) % 64) % 64)
    message += lenpadding

    # Process the message in 512-bit chunks
    for i in range(0, len(message), 64):
        subchunk = []
        for num in range(64):
            subchunk.append(message[i+num])
        chunk = struct.pack("64B", *subchunk)
        # Create message schedule array
        w = [0] * 64
        for j in range(16):
            w[j] = struct.unpack(">I", chunk[j*4:j*4+4])[0]
        for j in range(16, 64):
            s0 = rotr(w[j-15], 7) ^ rotr(w[j-15], 18) ^ (w[j-15] >> 3)
            s1 = rotr(w[j-2], 17) ^ rotr(w[j-2], 19) ^ (w[j-2] >> 10)
            w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xffffffff

        # Initialize working variables
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        # Compression function main loop
        for j in range(64):
            S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + k[j] + w[j]) & 0xffffffff
            S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffff
            
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff

        # Add the compressed chunk to the current hash value
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        h5 = (h5 + f) & 0xffffffff
        h6 = (h6 + g) & 0xffffffff
        h7 = (h7 + h) & 0xffffffff

    # Produce the final hash value
    hash_value = struct.pack(">8I", h0, h1, h2, h3, h4, h5, h6, h7)
    return hash_value.hex().upper()

def readFile(file_path):
    f = open(file_path, 'rb')
    return f.read()

def get_input(): 
    choice = input("Would you like to enter in 'text' or a 'file': ")
    while choice not in ("text", "Text", "file", "File"):
        print("You typed something wrong. Please pick either 'text' or 'file'.")
        choice = input("Would you like to enter in 'text' or a 'file': ")
    if choice == 'text':
        str = input("Enter your text: ")
        message = str.encode('utf-8') 
    else: 
        file = input("Enter your filename with its full path: ")
        while (not os.path.isfile(file)): 
            print("You typed something wrong. Please enter a valid filename.")
            file = input("Enter your filename with its full path: ")
        message = readFile(file)
    return message

# Example usage
hash_value = sha256(get_input())
print(hash_value)
