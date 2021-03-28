
def assemble_payload(payload_str:str):
    payload_len = len(payload_str) #can be up to two bytes (16 bits)
    payload_str = payload_str.encode()

    #this is where we may need to generate random data to avoid padding issues
    if len(payload_str) < 992: payload_str = payload_str + (b'\xFF' * (992 - len(payload_str)))

    payload_segments = [payload_str[i:i+32] for i in range(31)]
    #31 segments of 32byte(256bit) payload segments, allows us to use 1012 bytes

    return payload_str, payload_len.to_bytes(2, byteorder='big')
