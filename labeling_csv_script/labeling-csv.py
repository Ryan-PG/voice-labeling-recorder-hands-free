import os
import re
from docx import Document
from pydub.utils import mediainfo
import pandas as pd

def get_word_lines(docx_file):
    """ Extracts non-empty lines of text from a Word document. """
    doc = Document(docx_file)
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return lines

def natural_sort_key(s):
    """ Sorts file names numerically and alphabetically. """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def get_wav_files(directory):
    """ Gets a sorted list of .wav files from a directory. """
    wav_files = sorted(
        [f for f in os.listdir(directory) if f.endswith(".wav")],
        key=natural_sort_key
    )
    return wav_files

def get_audio_length(file_path):
    """ Gets the length of a .wav file in milliseconds. """
    try:
        info = mediainfo(file_path)
        return int(float(info["duration"]) * 1000)
    except Exception:
        return 0  

def match_lines_to_audio(docx_path, audio_dir, output_csv):
    """ Matches Word document lines to .wav files and saves to a CSV. """
    
    lines = get_word_lines(docx_path)
    wav_files = get_wav_files(audio_dir)

    
    if len(lines) != len(wav_files):
        print(f"Warning: Mismatch! {len(lines)} lines but {len(wav_files)} audio files.")
        if len(lines) > len(wav_files):
            print(f"Extra lines in document: {len(lines) - len(wav_files)}")
        elif len(wav_files) > len(lines):
            print(f"Extra audio files: {len(wav_files) - len(lines)}")

    data = []
    for i, (wav_file, line) in enumerate(zip(wav_files, lines)):
        wav_path = os.path.join(audio_dir, wav_file)
        length = get_audio_length(wav_path)
        data.append([wav_file, length, line])

    
    df = pd.DataFrame(data, columns=["name", "length", "label"])
    df.to_csv(output_csv, index=False)
    print(f"CSV file saved: {output_csv}")


docx_file = "./labeling_csv_script/recordings/Kurdi.Text-Cleaned.docx"
audio_directory = "./labeling_csv_script/recordings"
output_csv_file = "./labeling_csv_script/recordings/segments_info.csv"

match_lines_to_audio(docx_file, audio_directory, output_csv_file)
