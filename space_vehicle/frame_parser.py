from misc.custom_exceptions import *
from space_vehicle.actions.keymgmt_select import *
from space_vehicle.actions.keymgmt_wipe import *
from space_vehicle.actions.keymgmt_write import *
from space_vehicle.actions.keymgmt_regenerate import *
from space_vehicle.actions.signature_validation import *
from space_vehicle.actions.data_send import *

class Frame:
    """"""
    def __init__(self, frame_bstr:str, debug:bool=False): #TODO This should be a bytestring not str
        selection, options, payload, checksum = self.split_frame(frame_bstr)

        if not self.checksum_validation(frame_bstr, checksum): raise InvalidFrameError #TODO do we need exit logic here?

        self.execute_request(int.from_bytes(selection, byteorder='little', signed=False), options, payload)

    def split_frame(self, frame_bstr:str) -> [str, str]:
        starting_position = frame_bstr.find(b'\xDE\xAD\xBE\xEF') + 4 #compensate for tag itself
        ending_position = frame_bstr.find(b'\xBE\xEF\xDE\xAD')

        ## TODO vaidate that the payload is 1012 bytes so we recieeved the full frame

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

        ## TODO

        return True

    def execute_request(self, selection:int, options:str, payload:str):
        """this is where we do action selection and such

        TODO"""

        if selection == 1:
            self.selecton_key_manipulation(options, payload)
            #selecton_key_manipulation(options)
        elif selection == 2:
            self.selection_data_exchange(options, payload)
            #selection_data_exchange(options)
        elif selection == 3:
            self.selection_firmware_validation()
            #selection_firmware_validation(options)

    def selecton_key_manipulation(self, options:str, payload:str):
        """This will interface with the memory class to select the active key,
        replace existing keys in the schedule, or lookup what key is active. The
        number of the active key can be transmitted in plaintext. This is also where
        we will perform the asymetric key exchange. Generally these functions
        use the second byte of the options segment for indexing

        param::str::options
        param::str::payload where relevant this allows for key exchange"""

        ## TODO When we strip a single byte from a byte string, do we automatically
        ## get type conversion to an int? Curious about this, seems odd

        if options[0] == 1: keymgmt_wipe()
        elif options[0] == 2: keymgmt_select(options[1])
        elif options[0] == 3: keymgmt_write(options[1], payload)
        elif options[0] == 4: keymgmt_regenerate()
        else: raise InvalidFrameError

    def selection_data_exchange(self, options:str, payload:str):
        """This is where our symmetric exchange will happen, basically just need
        to determine how we want to chunk out the payload block, assuming AES256
        and then work it onto a bytestring return for transmission

        param::str::options two byte options field
        param::str::payload data to exchange, key is already selected in memory"""

        data_send(options, payload)

    def selection_firmware_validation(self):
        """I think we will want to simulate this, something like creating a file
        with a bunch of random junk in it, and then passing the hash back and
        forth. If we had this compiled (C something) we could run it against the
        binaries, but since its python bytecode, its dynamic so that wont work

        param::str::options two byte options field"""

        signature_validation()
