
def data_send(payload_len:int, payload:str):
    """
    """
    payload_len = int.from_bytes(payload_len, byteorder='big', signed=False)
    payload = payload[:payload_len].decode()

    print(f"Recieved data send, Payload size: {payload_len}, Payload: {payload}")

    payload_segments = [payload[i:i+32] for i in range(31)]
    #31 segments of 32byte(256bit) payload segments, allows us to use 1012 bytes
