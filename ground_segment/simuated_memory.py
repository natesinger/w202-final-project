#!/usr/bin/python3

class GroundMemoryManager(object):
    """"""
    def __init__(self):
        self.simulated_executablebinary = None
        self.running_memory = None
        self.selectedkey = None
        self.io_stream = None
        self.memory_filename = "ground_segment/nvram.bin" #from project root

    def __enter__(self):
        self.io_stream = open(self.memory_filename,"r+b")
        return self

    def __exit__(self, x,y,z): #junk variables to carry null exit params
        self.io_stream.close()
        return self

    def cycle_stream_mode(self, read:bool=False):
        """because of bugs in python3's binary read/write this is necessary"""
        if read:
            self.io_stream.close()
            self.io_stream = open(self.memory_filename,"r+b")
        else:
            self.io_stream.close()
            self.io_stream = open(self.memory_filename,"w+b")

    def write_patch(self, patch_str:str, offset:int):
        """in python we cannot overwite specific spot in file, so we must read
        the entire file into memory patch in memory, and then write back out"""
        self.cycle_stream_mode(True) #set io as read
        old_file = self.io_stream.read()

        old_file_front = old_file[:offset]
        old_file_back = old_file[offset+len(patch_str):]

        new_file = old_file_front + patch_str + old_file_back
        assert len(new_file) == len(old_file)

        self.cycle_stream_mode(False) #set io as write
        self.io_stream.write(new_file)

    def read_keyselection(self):
        self.cycle_stream_mode(True) #set io to read
        return self.io_stream.read()[15*32:(15*32)+1]

    def write_keyselection(self, selection:int):
        selection = int(selection).to_bytes(1, byteorder='big')
        index = 15*32
        self.write_patch(selection, index)

    def read_key(self):
        index = self.read_keyselection()
        position = 32*int.from_bytes(index,byteorder='big')

        self.cycle_stream_mode(True) #set io to read
        return self.io_stream.read()[position:position+32]

    def write_key(self, key_str:str):
        index = self.read_keyselection()
        position = 32*int.from_bytes(index,byteorder='big')

        self.cycle_stream_mode(True) #set io to read
        self.write_patch(key_str, position)

    def dump(self):
        self.cycle_stream_mode(True) #set io to read
        return self.io_stream.read()

    def clear(self):
        self.io_stream.seek(0,0) #set io head at row 0 col 0
        self.io_stream.truncate() #clear the file
        self.io_stream.write(b'\xFF'*512)

def run():
    with GroundMemoryManager() as m:
        #print(m.read_keyselection())
        m.write_key(b'\x42'*32)
        print(m.dump())
        #m.clear()

if __name__ == "__main__":
    run()
