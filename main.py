import sys
import os
import time
import wave
import pyaudio
from PyQt5 import QtWidgets, QtCore


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class AudioRecorder(QtCore.QThread):
    """
    A QThread that records audio from the specified input device.
    """
    def __init__(self, device_index, parent=None):
        super(AudioRecorder, self).__init__(parent)
        self.device_index = device_index
        self._running = True
        self.frames = []

    def run(self):
        pa = pyaudio.PyAudio()
        try:
            stream = pa.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK,
                             input_device_index=self.device_index)
        except Exception as e:
            print("Error opening audio stream:", e)
            return

        while self._running:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
            except Exception as e:
                print("Error during recording:", e)
                break
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        pa.terminate()

    def stop(self):
        self._running = False

class MainWindow(QtWidgets.QMainWindow):
    """
    Main application window for the Voice Recorder.
    """
    def __init__(self, device_index):
        super(MainWindow, self).__init__()
        self.device_index = device_index

        self.setWindowTitle("Voice Recorder")
        self.resize(400, 200)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.instruction_label = QtWidgets.QLabel(
            "Instructions:\n"
            "- Press the Space Key to start recording.\n"
            "- The timer shows elapsed time.\n"
            "- Press Space again to stop recording.\n"
            "- Press Delete while recording to discard.\n"
            "- Press Delete after stopping to delete the last recording."
        )
        self.instruction_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.instruction_label)

        self.timer_label = QtWidgets.QLabel("")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.timer_label)

        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)  
        self.timer.timeout.connect(self.update_timer)

        
        self.recording = False
        self.recorder = None
        self.recording_start_time = None
        self.recording_count = self.get_initial_recording_count()

        
        if not os.path.exists("recordings"):
            os.makedirs("recordings")

        
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def get_initial_recording_count(self):
        """
        Checks the 'recordings' folder for existing files to continue numbering.
        """
        count = 0
        if os.path.exists("recordings"):
            for filename in os.listdir("recordings"):
                if filename.startswith("recording_") and filename.endswith(".wav"):
                    try:
                        num = int(filename[len("recording_"):-len(".wav")])
                        if num > count:
                            count = num
                    except:
                        continue
        return count

    def keyPressEvent(self, event):
        """
        Handle Space and Delete key presses:
          - Space: start/stop recording.
          - Delete: discard current recording (if recording) or delete last saved recording.
        """
        key = event.key()
        if key == QtCore.Qt.Key_Space:
            if not self.recording:
                self.start_recording()
            else:
                self.stop_recording(save=True)
        elif key == QtCore.Qt.Key_Delete:
            if self.recording:
                self.stop_recording(save=False)
            else:
                self.delete_last_recording()
        else:
            super(MainWindow, self).keyPressEvent(event)

    def start_recording(self):
        """Starts a new recording session using the selected input device."""
        self.recorder = AudioRecorder(self.device_index)
        self.recorder.start()
        self.recording_start_time = time.time()
        self.timer.start()
        self.recording = True
        self.instruction_label.setText("Recording... Press Space to stop, Delete to discard.")

    def stop_recording(self, save=True):
        """
        Stops the current recording. If 'save' is True, the recording is saved;
        otherwise, it is discarded.
        """
        if self.recorder is not None:
            self.recorder.stop()
            self.recorder.wait()  
            self.timer.stop()

            if save:
                self.recording_count += 1
                filename = os.path.join("recordings", f"recording_{self.recording_count}.wav")
                try:
                    wf = wave.open(filename, 'wb')
                    wf.setnchannels(CHANNELS)
                    pa = pyaudio.PyAudio()
                    wf.setsampwidth(pa.get_sample_size(FORMAT))
                    pa.terminate()
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(self.recorder.frames))
                    wf.close()
                    self.instruction_label.setText(
                        f"Recording saved:\n{filename}\n\nPress Space to record again,\nor Delete to remove the last recording."
                    )
                except Exception as e:
                    self.instruction_label.setText(f"Error saving recording:\n{str(e)}")
            else:
                self.instruction_label.setText("Recording discarded.\nPress Space to record again.")

            self.recorder = None
            self.recording = False
            self.timer_label.setText("")

    def delete_last_recording(self):
        """Deletes the last saved recording file (if any)."""
        if self.recording_count > 0:
            filename = os.path.join("recordings", f"recording_{self.recording_count}.wav")
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    self.instruction_label.setText(f"Deleted last recording:\n{filename}\nPress Space to record again.")
                    self.recording_count -= 1
                except Exception as e:
                    self.instruction_label.setText(f"Error deleting file:\n{filename}\n{str(e)}")
            else:
                self.instruction_label.setText("No recording file found to delete.")
        else:
            self.instruction_label.setText("No recordings to delete.")

    def update_timer(self):
        """Updates the timer label with the elapsed recording time."""
        elapsed = time.time() - self.recording_start_time
        mins, secs = divmod(int(elapsed), 60)
        millis = int((elapsed - int(elapsed)) * 1000)
        self.timer_label.setText(f"Elapsed Time: {mins:02d}:{secs:02d}.{millis:03d}")

class DeviceSelectionDialog(QtWidgets.QDialog):
    """
    A dialog that lists available input devices so the user can select one.
    """
    def __init__(self, parent=None):
        super(DeviceSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Input Device")
        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(QtWidgets.QLabel("Select Audio Input Device:"))
        self.device_combo = QtWidgets.QComboBox(self)
        self.populate_devices()
        self.layout.addWidget(self.device_combo)

        
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(buttonBox)

    def populate_devices(self):
        """
        Populates the combo box with all available input devices.
        """
        self.pa = pyaudio.PyAudio()
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            if info.get('maxInputChannels', 0) > 0:
                display_text = f"{info['name']} (Index {i})"
                self.device_combo.addItem(display_text, i)

    def get_selected_device_index(self):
        """Returns the device index of the currently selected input device."""
        return self.device_combo.currentData()

def main():
    app = QtWidgets.QApplication(sys.argv)

    
    deviceDialog = DeviceSelectionDialog()
    if deviceDialog.exec_() == QtWidgets.QDialog.Accepted:
        device_index = deviceDialog.get_selected_device_index()
    else:
        sys.exit(0)  

    
    window = MainWindow(device_index)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()