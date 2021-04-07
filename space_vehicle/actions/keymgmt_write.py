from space_vehicle.actions.keymgmt_regenerate import exchange_key

def keymgmt_write(index:int):
    print(f"Recieved: Key Managemnet Write, Key Index: {index}")

    exchange_key(index)
