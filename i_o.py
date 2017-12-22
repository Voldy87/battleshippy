#!/usr/bin/python

"""
The IO module it's a layer between the two user-interface classes (GUI and CLI), which
in turn are used by the main module, and the rest of the system, allowing sending
and receiving data both from local (e.g. using python executable on a target platform)
and remote (e.g. playing the game on the web site built with Django)
"""

__author__ =  'Andrea Orlandi'
__version__=  '1.0'

class I_O:
    def __init__(self,inpuType="stdin", outpuType="stdout"):
        """

        Set default attribute values 
 
        Keyword arguments:
        inpuType -- type of input
        outpuType -- type of input
        
        """
        self.inType = inpuType
        self.outType = outpuType
    def write(self,string):
        switch = {
            'stdCLI' : stdOut_cli, # stdOut is a fun
            'stdGUI' : stdOut_tkinter,
            'socket' : writeSocket, 
            'django' : djangoSend}
        switch[self.outType](string)
    def read(self):
        switch = {
            'stdCLI' : stdIn_cli,
            'stdGUI' : stdIn_tkinter,
            'socket' : readSocket, 
            'django' : djangoRcv}
        return switch[self.inType]
    def stdOut_cli(self,string):
        print(string)
    def stdOut_tkinter():
        pass
    def stdIn_cli():
        line = input()
        return line
    def stdIn_tkinter():
        pass
    def writeSocket():
        pass
    def readSocket():
        pass
    def djangoSend():
        pass
    def djangoRcv():
        pass
