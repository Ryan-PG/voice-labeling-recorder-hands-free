# Voice Recorder App (Hands Free)

## Overview

This is a simple **hands-free voice recording app** built with **Python** and **Streamlit**. It allows users to **start, stop, and delete recordings** using their keyboard. The application records audio, saves files sequentially, and provides real-time feedback on the recording duration.

## Features

- 🎙 **Start Recording**: Press `Space` to begin recording.
- ⏱ **Real-time Timer**: Displays elapsed recording time.
- ⏹ **Stop Recording**: Press `Space` again to stop recording.
- 🗑 **Discard Recording**: Press `Delete` while recording to discard it.
- 🧹 **Delete Last Recording**: Press `Delete` after stopping to remove the last saved recording.
- 📁 **Automatic File Management**: Saves recordings sequentially in the `recordings` folder.
- ⚡ **Keyboard-Controlled**: No mouse needed—just use `Space` and `Delete` keys!

## Installation

### Prerequisites

Ensure you have **Python 3.7+** installed on your system. Then install dependencies:

```sh
pip install streamlit sounddevice numpy keyboard
```

## Usage

Run the application using:

```sh
streamlit run your_script.py
```

Once running, use the following controls:

- **Press `Space`** → Start Recording
- **Press `Space` again** → Stop and Save Recording
- **Press `Delete` while recording** → Discard recording
- **Press `Delete` after stopping** → Delete last saved recording

## File Storage

- Recordings are stored in the `recordings/` directory.
- Files are named sequentially: `recording_1.wav`, `recording_2.wav`, etc.
- Deleting the last recording removes the most recent file.

## License

This project is open-source under the **MIT License**.

## Contributions

Feel free to submit **issues, suggestions, or pull requests**!

---

🚀 Happy Recording! 🎙
