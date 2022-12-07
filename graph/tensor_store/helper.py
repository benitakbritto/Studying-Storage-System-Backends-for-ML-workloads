def int_to_bytes(num):
    str_val = str(num)
    return str_val.encode()

def convert_tensor_to_bytes(tensor_data):
    return tensor_data.encode()