'''
    @brief: Integer to Bytes and vice versa
    @authors: Benita, Hemal, Reetuparna
'''

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7), 'big')
    
def bytes_to_int(xbytes):
    return int.from_bytes(xbytes, 'big')