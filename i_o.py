#!/usr/bin/python

"""
The IO module it's a layer between the two user-interface classes (GUI and CLI), which
in turn are used by the main module, and the rest of the system, allowing sending
and receiving data both from local (e.g. using python executable on a target platform)
and remote (e.g. playing the game on the web site built with Django)
"""

__author__ =  'Andrea Orlandi'
__version__=  '1.0'

import time, sys #all?

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
    def stdIn_cli__loading(interval): #percentual loading with ANSI escape codes
        print ("Loading...")
        for i in range(0, 100):
            time.sleep(interval)
            sys.stdout.write(u"\u001b[1000D" + str(i + 1) + "%")
            sys.stdout.flush()
        print()
    def write(self,string):
        switch = {
            'stdCLI' : self.stdOut_cli, # stdOut is a fun
            'stdGUI' : self.stdOut_tkinter,
            'socket' : self.writeSocket, 
            'django' : self.djangoSend}
        switch[self.outType](string)
    def read(self):
        switch = {
            'stdCLI' : self.stdIn_cli,
            'stdGUI' : self.stdIn_tkinter,
            'socket' : self.readSocket, 
            'django' : self.djangoRcv}
        return switch[self.inType]()
    def stdOut_cli(self,string):
        print(string)
    def stdOut_tkinter(self, data):
        pass
    def stdIn_cli(self):
        line = input() #former raw_input
        return line
    def stdIn_tkinter(self):
        pass
    def writeSocket(self, data):
        pass
    def readSocket(self):
        pass
    def djangoSend(self, data):
        pass
    def djangoRcv(self):
        pass
