from misc.custom_exceptions import *

class Frame:
    """"""
    def __init__(self, frame_bstr:str, debug:bool=False): #TODO This should be a bytestring not str
        options_major, options_minor, payload, checksum = split_frame(frame_bstr)

        if not checksum_validation(): raise InvalidFrameError #TODO do we need exit logic here?

    def split_frame(self, frame_bstr:str):
        print(frame_bstr)

        starting_position = frame_bstr.find('\xDE\xAD\xBE\xEF')
        ending_position = frame_bstr.find('\xBE\xEF\xDE\xAD')

        if (starting_position == -1) or (ending_position == -1): #couldnt locate
            #raise InvalidFrameError
            return #TODO do we need this return?

        """ TODO
        probably need to modify start position to kill start indicator
        probably need to modify the end position to kill end indicator

        (1B) bytestr::options_major = starting_position
        (3B) bytestr::options_minor = starting_position + 1
        (1012B) bytestr::payload = starting_position + 4
        (1B) bytestr::checksum = ending_position - 1
        maybe do this in two phases?
        """

        #TODO input validation for 0x1-0x3 major option

        return options_major, options_minor, payload, checksum

    def checksum_validation(self, frame_bstr:str, chksum:int):
        """TODO add bytes in sequence mod \xFF and validate, return true if valid"""
        return True

    def execute_request(self, options_major:int, options_minor:int):
        """this is where we do action selection and such"""
        if options_major == 1:
            selecton_key_manipulation(options_minor)
        elif options_major == 2:
            selection_data_exchange(options_minor)
        elif options_major == 3:
            selection_firmware_validation(options_minor)

    def selecton_key_manipulation(self, options_minor:int):
        pass
        #from here we make a selection based on minor options and execute the action located in the actions folder

    def selection_data_exchange(self, options_minor:int, payload:str):
        pass

    def selection_firmware_validation(self, options_minor:int):
        pass
