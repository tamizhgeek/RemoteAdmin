from Tkinter import *
from subprocess import *
class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.run_sms = Button(frame, text="Run SMS Deamon", command=self.run_sms)
        self.run_sms.pack(side=LEFT)

        self.run_twitter = Button(frame, text="Run Twitter Deamon", command=self.run_twitter)
        self.run_twitter.pack(side=LEFT)

          
    def run_sms(self):
        p1 = Popen(['python sms/console.py'],shell=True)
        
    def run_twitter(self):
        p2 = Popen(['python twitter/console.py'],shell=True)


root = Tk()

app = App(root)

root.mainloop()
