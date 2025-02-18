# Voice Recorder with PyQt5 and PyAudio

This is a simple voice recording application built using Python, PyQt5 for the GUI, and PyAudio for handling audio input. The application allows users to select an input device and record audio with keyboard controls.

## Features

- **Device Selection**: Choose from available input devices before recording.
- **Simple Controls**:
  - Press `Space` to start/stop recording.
  - Press `Delete` to discard or delete the last saved recording.
- **Real-Time Timer**: Displays elapsed recording time.
- **Automatic File Naming**: Saves recordings in a `recordings/` folder with sequential numbering.
- **Error Handling**: Detects input device issues and file operations safely.

## Installation

### Option 1: Install from Source

Ensure you have Python installed (>=3.7). Install dependencies using:

```bash
pip install -r requirements.txt
```

> **Note:** On some systems, installing PyAudio may require additional system dependencies. Refer to the [official PyAudio documentation](https://people.csail.mit.edu/hubert/pyaudio/) if you encounter issues.

### Option 2: Download Executable

You can download the pre-built application (`labeling-voice-recorder.exe`) from the `dist/` folder and run it directly without needing to install Python or dependencies.

## Usage

### Option 1: Run from Source

Run the application with:

```bash
python main.py
```

Or, if you downloaded the executable:

```bash
./dist/labeling-voice-recorder.exe
```

### Option 2: Download and Use Pre-built Executable
You can download the built version of this application (`labeling-voice-recorder.exe`) from the `dist/` folder or directly from [this link](https://github.com/Ryan-PG/voice-labeling-recorder-hands-free.git/dist/./dist/labeling-voice-recorder.exe). Simply double-click the executable to run the application without needing to install Python or any dependencies.

### Keyboard Shortcuts
- **`Space`**: Start/Stop recording.
- **`Delete` (while recording)**: Discard the current recording.
- **`Delete` (after recording)**: Delete the last saved recording.

## How It Works

1. **Device Selection**
   - On startup, a dialog appears listing available audio input devices.
   - Select a device and click `OK` to proceed.

2. **Recording**
   - Press `Space` to start recording.
   - The app shows the elapsed recording time.
   - Press `Space` again to stop and save the recording.
   - Press `Delete` to discard the current recording.

3. **Saving & Deleting**
   - Saved recordings are stored in a `recordings/` folder as `recording_1.wav`, `recording_2.wav`, etc.
   - Press `Delete` after recording to remove the last saved file.

## Building the Application

If you want to build your own executable version of this application, you can use the following command:

```bash
pyinstaller --onefile --windowed --name labeling-voice-recorder --add-data "recordings;recordings" main.py
```

This will create an executable that includes the necessary dependencies.

## Project Structure

```
voice-recorder/
├── main.py         # Main application script
├── recordings/     # Directory where recorded audio files are saved
├── requirements.txt # Dependencies file
├── dist/           # Folder containing executable
└── README.md       # Documentation
```

## Troubleshooting

- **No input devices detected?**
  - Ensure your microphone is connected and recognized by the system.
  - Try running `python -m pyaudio` to check available devices.

- **PyAudio installation issues?**
  - On Linux, install dependencies first:
    ```bash
    sudo apt-get install portaudio19-dev python3-pyaudio
    ```
  - On Windows, consider using a prebuilt PyAudio wheel.

## License

This project is open-source and available under the MIT License.

---

Feel free to contribute or modify the code as needed!

