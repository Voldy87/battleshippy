from tkinter import Tk, Label, Button, Frame, N,S,E,W,SE, StringVar #LEFT, RIGHT
from common.interface.i_o import I_O

class GUI:
    LABEL_TEXT = [
        "This is our first GUI!",
        "Actually, this is our second GUI.",
        "We made it more interesting...",
        "...by making this label interactive.",
        "Go on, click on it again.",
    ]    
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label_index = 0
        self.label_text = StringVar()
        self.label_text.set(self.LABEL_TEXT[self.label_index])
        self.label = Label(master, textvariable=self.label_text)
        self.label.bind("<Button-1>", self.cycle_label_text)
        self.label.grid()
        
# default: row = 1st available empty row, col = 0
        self.label2 = Label(master, text="This is our first GUI!")
        self.label2.grid(row=3, columnspan=1  , sticky=W)
##        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.grid(row=1, sticky=W+E) 
##        self.greet_button.pack(side=LEFT)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.grid(row=2, column=1, sticky=SE)
##        self.close_button.pack(side=RIGHT)
        self.container = Frame(master)
        self.container.grid(row=4)
        self.button1 = Button(self.container)
        self.button1["text"] = "hello world"
        self.button1["background"] = "green"
        self.button1.pack()
        self.button1.bind("<Button-1>",self.info)
        self.button2 = Button(self.container)
        self.button2.configure(text = "wunderbar")
        self.button2.configure(background = "red")
        self.button2.pack()
        self.button2.bind("<Button-1>", self.ciao) #in case of "bind" the fun must take self AND event as args, while with "command" only self
        self.button2.bind("<Return>", self.ciao)
        self.button2.focus_force() #!
        self.button3 = Button(self.container)
        self.button3.configure(text = "giannighezi", background = "yellow")
        self.button3.pack()
        self.container2 = Frame(master)
        self.container3 = Frame(master)
        self.container4 = Frame(master)
        self.container2.grid(row=5, column=0)
        self.container3.grid(row=5, column=1)
        self.container4.grid(row=5, column=2)
        self.label3 = Label(self.container2, text="AAAAAAAAAA", background = "blue")
        self.label4 = Label(self.container3, text="bbbbbbbbbbbbb", background = "grey")
        self.label5 = Label(self.container4, text="CCCCCCCCCC", background = "orange")
        self.label3.pack()
        self.label4.pack()
        self.label5.pack()
    def ciao(self,event):
        print(str(event.time))
        print(str(event.type))
        print(str(event.widget))
        print(str(event.keysym)) #only for keyboardpress!!
    def greet(self):
        print("Greetings!")
    def info(self,event):
        print(event)
    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.LABEL_TEXT) # wrap around
        self.label_text.set(self.LABEL_TEXT[self.label_index])



    def renderGrid(self, grid, enemyView, lastshotView):
        pass  #gui first time draw, others update
##root = Tk()
##my_gui = GUI(root)
##root.mainloop()
