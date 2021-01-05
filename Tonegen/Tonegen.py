import pyaudio
import numpy as np
import threading
import time
import tkinter
from tkinter import *
from tkinter import font

root = tkinter.Tk()
root.title("Sine Tone Generator")
root.geometry("560x200")

####### Our wave settings, before the classwork ######
######################################################

sample_rate = 128000  # sampling rate, or bitrate
duration = 0.1        # wave duration
pitch_hertz = 440.0   # sine frequency or pitch or tone or note :)

### Only solution on using strings I found :) ###
#################################################

class freq_hz:
    def __init__(self, freq_hz_val):
        self.value = freq_hz_val    

pitch_str = freq_hz(pitch_hertz)

################ Amplitude thread ####################
######################################################

class amplitude(threading.Thread):
    def __init__(self, pitch, rate=44100, period=0.1):
        super().__init__()

        self._stop_event = threading.Event()
        self.pitch = pitch
        self.sample_rate = rate
        self.duration = period
        self.stopped = False
        self.py_audio = pyaudio.PyAudio()
        self.stream = self.py_audio.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)
        self.direction = 0
        self.rate = 50

    def set_pitch(self, hz):
        self.pitch.value = hz

    def mute(self):
        self.stopped = True

    def unmute(self):
        self.stopped = False

    def stop(self):
        self.direction = 0

    def grow(self):
        self.direction = 1

    def fall(self):
        self.direction = -1

    def run(self):
        while True:
            if self.stopped:
                time.sleep(duration)
            else:
                sample = sin_wav(self.sample_rate, self.duration, self.pitch.value)
                self.stream.write(sample)
            self.pitch.value = self.pitch.value + self.direction * self.rate
            if self.pitch.value > 25000.0:
                self.pitch.value = 25000.0
            if self.pitch.value < 0.0:
                self.pitch.value = 0.0

def sin_wav(rate, wav_dur, hz):
    return (np.sin(2 * np.pi * np.arange(rate * wav_dur) * hz / rate)).astype(np.float32).tobytes()

amplitude = amplitude(pitch_str, sample_rate, duration)
amplitude.daemon = True
amplitude.start()

####### Buttons functions ##########
####################################

def mute_callback():
    amplitude.mute()

def unmute_callback():
    amplitude.unmute()
    
def set_callback():
    global pitch_str
    pitch_str.value = float(set_str.get())

def slide(n):
    global pitch_str
    pitch_str.value = float(freq_scale.get())

def fall_callback():
    amplitude.fall()

def stop_callback():
    amplitude.stop()

def grow_callback():
    amplitude.grow()


hz_str = tkinter.StringVar()
hz_str.set(str(pitch_str.value))

set_str = tkinter.StringVar()
set_str.set(str(pitch_str.value))

freq_scale = Scale(root, from_=0, to=1000, orient=HORIZONTAL, command=slide, length=400)

#Button's settings
mute_btn = tkinter.Button(root, text="Mute", command=mute_callback)
unmute_btn = tkinter.Button(root, text="Unmute", command=unmute_callback)
hz_entry = tkinter.Entry(root, textvariable=hz_str)
hz_entry.config(state='disabled')
set_entry = tkinter.Entry(root, textvariable=set_str)
set_btn = tkinter.Button(root, text="Set", command=set_callback, padx=10, pady=10)
hz_label = tkinter.Label(root, text="Hz", padx=10, pady=10)
fall_btn = tkinter.Button(root, text="Fall", command=fall_callback, padx=10, pady=10)
stop_btn = tkinter.Button(root, text="Stop", command=stop_callback, padx=10, pady=10)
grow_btn = tkinter.Button(root, text="Grow", command=grow_callback, padx=10, pady=10)

#GUI coordinates
mute_btn.grid(row=3, column=0)
unmute_btn.grid(row=3, column=1)
hz_entry.grid(row=0, column=0)
set_entry.grid(row=1, column=0)
set_btn.grid(row=1, column=1)
hz_label.grid(row=0, column=1)
freq_scale.grid(row=2, column=0)
fall_btn.grid(row=2, column=2)
stop_btn.grid(row=1, column=2)
grow_btn.grid(row=0, column=2)


while True:
    hz_str.set(str(pitch_str.value))
    root.update_idletasks()
    root.update()
