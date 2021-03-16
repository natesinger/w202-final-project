
def keymgmt_write(key_number:int, payload:str):
    print(f"Recieved: Key Managemnet Write, Key Index: {key_number}, Payload {payload[0:32]}")
