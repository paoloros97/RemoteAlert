import PySimpleGUIWeb as sg
from tkinter import *
from threading import Thread
import socket

# Launch the following command to build the .exe version:
# pyinstaller --clean --noconsole --onefile .\WebMessenger.py

# Machine IP address 
addr = socket.getaddrinfo(socket.gethostname(), None)
addr=addr[::-1]
print("LiveMessenger by Paolo Ros")
print("ISTRUZIONI:")
print("1-Collegare questo PC al wi-fi.")
print("2-Collegare il dispositivo esterno alla stessa wi-fi.")
print('3-Aprire sul browser del dispositivo esterno il link: ' + str(addr[0][4][0]) + ':2222')

messaggio = 'ISTRUZIONI:\n1-Collegare questo PC al wi-fi.\n2-Collegare il dispositivo esterno alla stessa wi-fi. \n3-Aprire sul browser del dispositivo esterno il link:\n ' + str(addr[0][4][0]) + ':2222'

# Web interface:
layout = [  [sg.Text('Live Messenger by Paolo Ros', size=(25,2))],
            [sg.Text('Inserisci testo:'), sg.Button('Clear', size=(9, 1))],
            [sg.Multiline(size=(35,8), key='-in-')],
            [sg.Button('Show', size=(9, 1)), sg.Button('Hide', size=(9, 1))]
         ] 

def AlertWindow():
    global ws
    ws = Tk()
    ws.title("LiveMessenger by Paolo Ros")
    ws.attributes('-topmost', True)
    ws.configure(bg='black')
    global msg
    msg = Message(ws, 
            text=messaggio,
            fg = "black",
            bg = "yellow",
            width = 1400,
            font = "Helvetica 42 bold")

    msg.pack()
    ws.mainloop()


def WebInterface():
    window = sg.Window('LiveMessenger by Paolo Ros', layout, web_port=2222, web_start_browser=False, disable_close=True)
    while True:
        event, values = window.read()
        
        if event == 'Show': 
            if values['-in-'] != '':
                msg.configure(text=values['-in-']) # Write received text
                ws.state("zoomed") # Maximize
        elif event == 'Hide': 
            ws.state(newstate='iconic') # Minimize

        elif event == 'Clear':
            window['-in-'].update('')
        if event is None:
            break
    window.close()


thread_1 = Thread(target=AlertWindow)
thread_2 = Thread(target=WebInterface)

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()