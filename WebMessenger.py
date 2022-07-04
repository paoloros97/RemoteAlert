import PySimpleGUIWeb as sg
from tkinter import *
from threading import Thread
import socket

# Launch the following command to build the .exe version:
# pyinstaller --clean --noconsole --onefile .\WebMessenger.py

# Machine IP address 
addr = socket.getaddrinfo(socket.gethostname(), None)
addr=addr[::-1]
messaggio = 'ISTRUZIONI:\n1-Collegare questo PC al wi-fi.\n2-Collegare il dispositivo esterno alla stessa wi-fi. \n 3-Aprire sul browser del dispositivo esterno il link:\n ' + str(addr[0][4][0]) + ':2222'

# Web interface:
layout = [  [sg.Text('Live Messenger by Paolo Ros', size=(25,2))],
            [sg.Text('Inserisci testo:'), sg.Button('Clear', size=(9, 1))],
            [sg.Multiline(size=(35,8), key='-in-', do_not_clear=False)],
            [sg.Button('Show', size=(9, 1)), sg.Button('Hide', size=(9, 1))]
         ] 

def AlertWindow():
    global ws
    ws = Tk()
    ws.title("Message")
    ws.attributes('-topmost', True)
    ws.configure(bg='black')
    global msg
    msg = Message(ws, 
            text=messaggio,
            fg = "black",
            bg = "yellow",
            width = 1400,
            font = "Helvetica 50 bold italic")

    msg.pack()
    ws.mainloop()


def WebInterface():
    window = sg.Window('LiveMessenger', layout, web_port=2222, web_start_browser=False, disable_close=True)
    while True:
        event, values = window.read()
        
        if event == 'Show': 
            if values['-in-'] != '':
                msg.configure(text='Messaggio:\n' + values['-in-'])
                ws.state("zoomed")
                #print(values['-in-'])
        elif event == 'Hide': 
            ws.state(newstate='iconic')
            #print("Hide")
        elif event == 'Clear':
            window['-in-'].update('')
        if event is None:
            break
    #window.close()


thread_1 = Thread(target=AlertWindow)
thread_2 = Thread(target=WebInterface)
thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()