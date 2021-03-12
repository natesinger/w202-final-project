from misc.custom_exceptions import *

class Frame:
    """"""
    def __init__(self, frame_bstr:str, debug:bool=False): #TODO This should be a bytestring not str
        selection, options, payload, checksum = self.split_frame(frame_bstr)

        print(selection)
        print(options)
        print(len(payload))
        print(checksum)

        if not self.checksum_validation(frame_bstr, checksum): raise InvalidFrameError #TODO do we need exit logic here?

    def split_frame(self, frame_bstr:str) -> [str, str]:
        starting_position = frame_bstr.find(b'\xDE\xAD\xBE\xEF') + 4 #compensate for tag itself
        ending_position = frame_bstr.find(b'\xBE\xEF\xDE\xAD')

        if (starting_position == -1) or (ending_position == -1): #couldnt locate
            #raise InvalidFrameError
            return #TODO do we need this return?

        selection = frame_bstr[starting_position:starting_position+1] #first byte
        options = frame_bstr[starting_position+1:starting_position+3] #next two bytes
        payload = frame_bstr[starting_position+3:ending_position-1] #next 1012 bytes
        checksum = frame_bstr[ending_position-1:ending_position] #last byte

        if not (1 <= int.from_bytes(selection, byteorder='big', signed=False) <= 3):
            raise InvalidFrameError #validate major selection

        return selection, options, payload, checksum

    def checksum_validation(self, frame_bstr:str, chksum:int) -> bool:
        """Takes a frame as a byte string and a single byte checksum and performs
        boolean validation to ensure that the checksum matches the frame. Effectively
        this is just adding the bytes together one at a time and then performing
        modular division around a max byte value to get it down to one byte (\xFF==255).

        Given a frame: \x01\x05\x76\x32\x51, the valid checksum would be \xFF
        Given a frame: \xE3\x51\xBB\x01\x02... the valid checksum would be \xF3

        param::bytestr::frame_bstr this is the frame as recieved on the wire
        param::int::chksum this is the checksum parsed from the frame as an int
        return::bool pass fail condition whether the checksum validated
        """

        ##TODO

        return True

    def execute_request(self, selection:int, options:int):
        """this is where we do action selection and such"""
        if selection == 1:
            selecton_key_manipulation(options)
        elif selection == 2:
            selection_data_exchange(options)
        elif selection == 3:
            selection_firmware_validation(options)

    def selecton_key_manipulation(self, options:int):
        pass
        #from here we make a selection based on minor options and execute the action located in the actions folder

    def selection_data_exchange(self, options:int, payload:str):
        pass

    def selection_firmware_validation(self, options:int):
        pass
