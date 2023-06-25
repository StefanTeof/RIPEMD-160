"""
Implementation of RIPEMD-160
"""

# Initialize functions
def round_one(x, y, z):
    return x ^ y ^ z

def round_two(x, y, z):
    return (x & y) | ((~x) & z)

def round_three(x, y, z):
    return (x | (~y)) ^ z

def round_four(x, y, z):
    return (x & z) | (y & (~z))

def round_five(x, y, z):
    return x ^ (y | (~z))


# Initialize shifts
SHIFTS = [
    # Shifts for round 1
    [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8],
    
    # Shifts for round 2
    [12, 13, 11, 15, 6, 9, 9, 7, 12, 15, 11, 13, 7, 8, 7, 7],
    
    # Shifts for round 3
    [13, 15, 14, 11, 7, 7, 6, 8, 13, 14, 13, 12, 5, 5, 6, 9],
    
    # Shifts for round 4
    [14, 11, 12, 14, 8, 6, 5, 5, 15, 12, 15, 14, 9, 9, 8, 6],
    
    # Shifts for round 5
    [15, 12, 13, 13, 9, 5, 8, 6, 14, 11, 12, 11, 8, 6, 5, 5]
]


# Initialize constants
K = [
    # Round 1
    [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E],
    
    # Round 2
    [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000],
    
    # Round 3
    [0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E, 0x50A28BE6],
    
    # Round 4
    [0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E, 0x50A28BE6, 0x5C4DD124],
    
    # Round 5
    [0x8F1BBCDC, 0xA953FD4E, 0x50A28BE6, 0x5C4DD124, 0x6D703EF3]
]


# Initialize the rho and pi permutations
# Permutation rho
rho_permutation = [7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8]

# Permutation pi
def pi_permutation(i):
    return (9 * i + 5) % 16


# Message padding
def message_padding(message):
    bits = ''.join(format(byte, '08b') for byte in message)

    size = len(bits)
    
    if len(bits) % 512 != 448:
        bits += '1'

        while len(bits) % 512 != 448:
            bits += '0'
    
    bits += format(size, '064b')

    return bits


def ripemd_160(message):
    
    # Initialize word buffer
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    E = 0xC3D2E1F0

    padded_message = message_padding(message)

    # Devide the message in 512bit blocks
    blocks = [padded_message[i:i+512] for i in range(0, len(padded_message), 512)]
    
    for block in blocks:
        words = [block[i:i+32] for i in range(0, len(block), 32)] # Devide the block into 16 32-bit words
        for i in range(len(words)):
            words[i] = words[rho_permutation[i]] # Do rho permutation for each word
        a, b, c, d, e = A, B, C, D, E

        # 80 operations for each 512-bit block (16 words times 5 rounds)
        for i in range(0, 80):
            r=-1
            # Define the round function for each word
            if i<=16:
                fn = round_one(b,c,d)
                r = 0
            elif i<=32:
                fn = round_two(b,c,d)
                r = 1
            elif i<48:
                fn = round_three(b,c,d)
                r = 2
            elif i<64:
                fn = round_four(b, c, d)
                r = 3
            else:
                fn = round_five(b, c, d)
                r = 4

            # Update the words
            tmp_e = e
            e = d
            d = (c<<10) & 0xFFFFFFFF
            c = b
            b = ((a + fn + int(words[pi_permutation(i)],16) + K[r][i%5])<<SHIFTS[r][i%15] + tmp_e) & 0xFFFFFFFF        
            a = tmp_e

        # Update the word buffer
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF
        E = (E + e) & 0xFFFFFFFF

    hash_value = format(A, '08x') + format(B, '08x') + format(C, '08x') + format(D, '08x') + format(E, '08x')

    return hash_value



if __name__ == '__main__':
    msg = b'Hello World!'
    print(ripemd_160(msg))
