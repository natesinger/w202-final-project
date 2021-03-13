
class SimulatedMemory:
    def __init__(self):
        with open('.tmp/tmp_nvram.bin','a+') as io:
            pass

        #this is going to be a config file as a raw binary file so we can demonstrate exactly how small this memory requirement is

    #    self.keyspace = []
    #    for i in range(10): #setup keyspace
            #gen a key
    #        pass

    def read_key():
        pass

    def write_key():
        pass


if __name__ == "__main__":
    emulated_ram = SimulatedMemory()


#we can do this as a class maybe?

#I want to use a YAML config file to store the keys, and settings simulating NVRAM and operating memory




#256/32 = 8
#so for 10 keys we need 32*10 bytes
