import sounddevice as sd
import numpy as np

def clap_detected():
    print("Clap Detected")

def listen_for_clap(threshold=0.5, samplerate=44100):
    detected = False

    def audio_callback(indata, frames, time, status):
        nonlocal detected
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > threshold:
            detected = True
            clap_detected()
            raise sd.CallbackStop()  # Stop the stream when clap is detected

    with sd.InputStream(callback=audio_callback, channels=1, samplerate=samplerate):
        while not detected:
            sd.sleep(100)

if __name__ == "__main__":
    print("Listening for clap...")
    listen_for_clap()
