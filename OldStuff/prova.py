from tkinter import *
from tkinter import ttk
 
def popup():
    global info
    info = Toplevel()		  # Popup -> Toplevel()

    info.geometry('200x100')
    info.title('Hello')
    
    info.transient(ws) 	    #Popup reduction impossible
    #info.grab_set()	            #Interaction with window impossible game
 
def chiudi():
    info.destroy

ws = Tk()
ws.title('Main window')
Button(ws, text='Open popup', command=popup).pack(padx=10, pady=10)
Button(ws, text='Quit', command=chiudi).pack(padx=10, pady=10)
 
ws.mainloop()	    #Only for the main window