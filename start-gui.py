from Tkinter import *
from subprocess import *
class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Run SMS Deamon", command=self.run_sms)
        self.hi_there.pack(side=LEFT)

        self.hi_there = Button(frame, text="Run Twitter Deamon", command=self.run_twitter)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print "hi there, everyone!"

    def run_sms(self):
        p1 = Popen(['python sms/console.py'],shell=True)
        
    def run_twitter(self):
        p2 = Popen(['python twitter/console.py'],shell=True)

root = Tk()

app = App(root)

root.mainloop()
