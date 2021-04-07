
def keymgmt_regenerate():
    print(f"Recieved: Key Managemnet regenerate")

def exchange_key(io:object, index:int):
    print(f'exchanging key {index}')

    print(f'exchanging key {index}')
    print(io.recv())
    time.sleep(2)
    io.send(b'space 1')
    print(io.recv())
    time.sleep(2)
    io.send(b'space 2')
    print(io.recv())
    time.sleep(2)
    io.send(b'space 3')

#recieve public knowledge, p and g
#send ack
#recieve public key from ground
#send public key to ground
#recieve symetric key
#send ack to ground
