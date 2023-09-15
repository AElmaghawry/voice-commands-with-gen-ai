#!/usr/bin/env python3

import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json
import tkinter as tk
from threading import Thread  # Import the Thread class

'''This script processes audio input from the microphone and displays the transcribed text.'''

# Create a flag to track recording status
recording = False

# Create a variable to store the recording duration (in seconds)
# recording_duration = 5

# list all audio devices known to your system
print("Display input/output devices")
print(sd.query_devices())

# get the samplerate - this is needed by the Kaldi recognizer
device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])

# display the default input device
print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], device_info))

# setup queue and callback function
q = queue.Queue()

def recordCallback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    if recording:
        q.put(bytes(indata))

# build the model and recognizer objects.
print("===> Build the model and recognizer objects.  This will take a few minutes.")
model = Model(model_name='vosk-model-en-us-0.22')
recognizer = KaldiRecognizer(model, samplerate)
recognizer.SetWords(False)

def start_recording():
    global recording 
    recording = True 
    record_button.config(bg="red",activebackground="red",text="Recording")

def stop_recording(event):
    global recording 
    recording = False 
    record_button.config(bg="green",text="Recording")

# Function to toggle recognition
"""
IF you want to use the button with a duration 
time un comment the following function 
"""
# def toggle_recognition():
#     global recording
#     if not recording:
#         recording = True
#         record_button.config(bg="green", text="Recording")  # Change button color and text when recording
#         record_button.after(recording_duration * 1000, toggle_recognition)  # Schedule the toggle after the specified duration
    
#     else:
#         recording = False
#         record_button.config(bg="yellow", text="Recording")  # Change button color and text back to original state


# Function to start the GUI in a separate thread
def start_gui():
    # Create the GUI window
    window = tk.Tk()
    window.title("STT")
    # Create a single button for toggling recognition
    global record_button
    record_button = tk.Button(window, text="Recording", bg="green", width=20, height=3)
    record_button.pack(pady=10)

    record_button.bind("<ButtonPress-1>", lambda event: start_recording())
    record_button.bind("<ButtonRelease-1>", lambda event: stop_recording(event))

    # Start the GUI main loop
    window.mainloop()

# Create a thread for the GUI
gui_thread = Thread(target=start_gui)

print("===> Begin recording. Press Ctrl+C to stop the recording ")
try:
    with sd.RawInputStream(dtype='int16',
                            channels=1,
                            callback=recordCallback):
        # Start the GUI thread
        gui_thread.start()

        while True:
            data = q.get()
            if recording and recognizer.AcceptWaveform(data):
                recognizerResult = recognizer.Result()
                # convert the recognizerResult string into a dictionary
                resultDict = json.loads(recognizerResult)
                if not resultDict.get("text", "") == "":
                    print(recognizerResult)
                else:
                    print("no input sound")

except KeyboardInterrupt:
    print('===> Finished Recording')
except Exception as e:
    print(str(e))
print('===> Finished Recording')
