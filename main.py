import sounddevice as sd
import numpy as np
import wave
import time
import streamlit as st
import threading
import keyboard
import os

"""
# Voice Recorder App

## How to Use:
- **Press the Space Key** to start recording.
- The timer on the UI will show the elapsed time.
- **Press the Space Key again** to stop recording.
- **Press the Delete Key while recording** to discard the current recording.
- **Press the Delete Key after stopping** to remove the last saved recording.
- The recorded audio file will be saved automatically in the `recordings` folder.
- Files are saved sequentially as `recording_1.wav`, `recording_2.wav`, etc.

## Features:
- Hands-free recording using the Space key.
- Real-time timer display.
- Automatic file saving with sequential numbering.
- Delete functionality for both active and saved recordings.

"""

samplerate = 44100  # Sample rate
channels = 2  # Number of channels
recording = []
recording_flag = False
start_time = None
elapsed_time = 0
last_saved_filename = None

def callback(indata, frames, time, status):
    global recording_flag, recording
    if recording_flag:
        recording.append(indata.copy())

def record_audio(timer_placeholder):
    global recording_flag, recording, start_time, elapsed_time
    recording = []
    recording_flag = True
    start_time = time.time()
    with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
        while recording_flag:
            elapsed_time = int(time.time() - start_time)
            timer_placeholder.write(f"Recording Time: {elapsed_time} seconds")
            time.sleep(1)

def stop_recording(timer_placeholder):
    global recording_flag, last_saved_filename
    recording_flag = False
    if recording:
        last_saved_filename = save_audio()
    else:
        st.warning("No audio recorded. Recording was stopped before capturing any data.")
    timer_placeholder.write("Recording stopped.")

def get_next_filename():
    save_dir = "recordings"
    os.makedirs(save_dir, exist_ok=True)
    existing_files = [f for f in os.listdir(save_dir) if f.startswith("recording_") and f.endswith(".wav")]
    existing_numbers = [int(f.split("_")[1].split(".")[0]) for f in existing_files if f.split("_")[1].split(".")[0].isdigit()]
    next_number = max(existing_numbers) + 1 if existing_numbers else 1
    return os.path.join(save_dir, f"recording_{next_number}.wav")

def save_audio():
    if not recording:
        st.warning("No audio data to save.")
        return None
    audio_data = np.concatenate(recording, axis=0)
    filename = get_next_filename()
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
    st.success(f"Recording saved as {filename}")
    return filename

def delete_last_recording():
    global last_saved_filename
    if last_saved_filename and os.path.exists(last_saved_filename):
        os.remove(last_saved_filename)
        st.warning(f"Deleted last recording: {last_saved_filename}")
        last_saved_filename = None
    else:
        st.warning("No recording found to delete.")

def keyboard_listener(timer_placeholder):
    global recording_flag, start_time, elapsed_time, recording
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == "down":
            if event.name == "space":
                if not recording_flag:
                    threading.Thread(target=record_audio, args=(timer_placeholder,), daemon=True).start()
                else:
                    stop_recording(timer_placeholder)
            elif event.name == "delete":
                if recording_flag:
                    recording.clear()  # Discard current recording
                    recording_flag = False
                    timer_placeholder.write("Recording discarded.")
                else:
                    delete_last_recording()

def main():
    global elapsed_time, recording_flag
    st.title("Voice Recorder App")
    timer_placeholder = st.empty()
    threading.Thread(target=keyboard_listener, args=(timer_placeholder,), daemon=True).start()

if __name__ == "__main__":
    main()
