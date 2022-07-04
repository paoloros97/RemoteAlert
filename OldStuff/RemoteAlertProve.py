from tkinter import *

ws = Tk()
ws.title("Message")
ws.configure(bg="yellow")
#ws.geometry("1400x700")

messaggio = "Questo è un messaggio di prova, mentra questo è un altro messaggio di prova. Scriviamo un altro messaggio dai"
                

msg = Message(ws, 
            text=messaggio,
            fg = "black",
            bg = "yellow",
            width = 1400,
            font = "Helvetica 50 bold italic")

msg.pack() 

input("Invio")
msg.configure(text="s")

input("Minimize")
#ws.state(newstate='iconic')
ws.iconify()

input("Nuovo testo")
msg.configure(text="altro scritto")

input("Maximize")
ws.state("zoomed")
#ws.deiconify()
#ws.lift(aboveThis=None)

input("Minimize")
ws.state(newstate='iconic')
	
ws.mainloop()
