import PySimpleGUIWeb as sg
from tkinter import *
from tkinter import messagebox
from threading import Thread
import socket
import time
import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 ) # Auto-minimize console

# Launch the following command to build the .exe version, without icon:
# pyinstaller --clean --onefile .\WebMessenger.py
# With icon:
# pyinstaller --clean --onefile --icon frog.ico .\WebMessenger.py


addr = socket.getaddrinfo(socket.gethostname(), None) #local IP address 
addr=addr[::-1] # swap

print("LiveMessenger by Paolo Ros")
print("INSTRUCTIONS:")
print("1-Connect this PC to wi-fi (or ethernet).")
print("2-Connect another device to the same network, wi-fi or ethernet (i.e. Smartphone).")
print('3-Open this link on your external device\'s browser: ' + str(addr[0][4][0]) + ':2222')

messaggio = str(addr[0][4][0]) + ':2222'

# Web interface:
layout = [  [sg.Text('Live Messenger by Paolo Ros', size=(25,2))],
            [sg.Text('Insert text:'), sg.Button('Clear', size=(9, 1))],
            [sg.Multiline(size=(35,4), key='-in-')],
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
    ws.geometry('+%d+%d' % (0, 0)) # Window position top left

    ws.title("LiveMessenger by Paolo Ros") # Title 
    ws.attributes('-topmost', True) # Always on top
    ws.configure(bg='black') # Background black

    global msg
    msg = Message(ws, 
            text=messaggio,
            fg = "black",
            bg = "yellow",
            width = screen_width, # full width
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