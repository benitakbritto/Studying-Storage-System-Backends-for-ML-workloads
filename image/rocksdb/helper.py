'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7), 'big')
    
def bytes_to_int(xbytes):
    return int.from_bytes(xbytes, 'big')