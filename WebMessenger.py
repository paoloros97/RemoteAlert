import PySimpleGUIWeb as sg
from tkinter import *
from tkinter import messagebox
from threading import Thread
import socket
import time

# Launch the following command to build the .exe version:
# pyinstaller --clean --onefile .\WebMessenger.py


addr = socket.getaddrinfo(socket.gethostname(), None) #local IP address 
addr=addr[::-1] # swap

print("LiveMessenger by Paolo Ros")
print("INSTRUCTIONS:")
print("1-Connect this PC to wi-fi (or ethernet).")
print("2-Connect another device to the same network, wi-fi or ethernet (i.e. Smartphone).")
print('3-Open this link on your external device\'s browser: ' + str(addr[0][4][0]) + ':2222')

messaggio = 'Connect to:\n ' + str(addr[0][4][0]) + ':2222'

# Web interface:
layout = [  [sg.Text('Live Messenger by Paolo Ros', size=(25,2))],
            [sg.Text('Insert text:'), sg.Button('Clear', size=(9, 1))],
            [sg.Multiline(size=(35,8), key='-in-')],
            [sg.Button('Show', size=(9, 2)), sg.Button('Hide', size=(9, 2))],
            [sg.Text(' ', key='ore')],
            [sg.Text('The message will be auto-closed after 40s.')],
         ] 



def disable_event(): # Make x button useless
    messagebox.showwarning('No No No', 'Chiudere la finestra del terminale, non questa.')
    pass

def AlertWindow():
    global ws # needed for the following def WebInterface function
    ws = Tk()

    screen_width = ws.winfo_screenwidth() # Screen width
    screen_height = ws.winfo_screenheight() # Screen height
    ws_width = (screen_width / 2) # half screen and x position
    #ws_height = screen_height 
    ws.geometry(f'{int(ws_width)}x{int(screen_height)}+{int(ws_width)}+{0}') # width \x height \+ x position \+ y position
    ws.title("LiveMessenger by Paolo Ros") # Title 
    ws.attributes('-topmost', True) # Always on top
    ws.configure(bg='black') # Background black

    global msg
    msg = Message(ws, 
            text=messaggio,
            fg = "black",
            bg = "yellow",
            width = ws_width-8, #half screen
            font = "Arial 43 bold")
    msg.pack()

    ws.protocol("WM_DELETE_WINDOW", disable_event) # Disable window closing button

    ws.mainloop()

def WebInterface():
    window = sg.Window('LiveMessenger by Paolo Ros', layout, web_port=2222, web_start_browser=False, disable_close=True)

    while True:
        event, values = window.read()
        local_time = time.ctime() # Timestamp

        if event == 'Show': 
            if values['-in-'] != '': # Se il testo non è vuoto
                msg.configure(text=values['-in-']) # Write received text
                ws.state(newstate='normal') # Maximize
                window['ore'].update('Showed @ ' + str(local_time))

                if 'autoclose' in locals(): # Check if autoclose exists
                    ws.after_cancel(autoclose) # Stop to restart AutoClosing

                autoclose = ws.after(40000, lambda:(ws.state(newstate='iconic'), window['ore'].update('AutoHidden @ ' + str(local_time))))

        elif event == 'Hide':
            ws.state(newstate='iconic') # Minimize
            window['ore'].update('Hidden @ ' + str(local_time))
            if 'autoclose' in locals(): # Check if autoclose exists
                ws.after_cancel(autoclose) # Stop AutoClosing
            
        elif event == 'Clear':
            window['-in-'].update('')

        if event is None:
            break

    window.close()

thread_1 = Thread(target = AlertWindow)
thread_2 = Thread(target = WebInterface)

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()