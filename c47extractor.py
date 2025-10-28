import os
import re
import sys
import time
from datetime import datetime

def extract_wavs(input_filename, names_file):
    """
    Searches a binary file for RIFF/WAVE headers and extracts the chunks 
    as separate .wav files, naming them according to a provided list.
    """
    try:
        with open(input_filename, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_filename}")
        return

    riff_header = b'RIFF'
    wave_signature = b'WAVE'

    indices = []
    i = 0
    while True:
        i = data.find(riff_header, i)
        if i == -1:
            break
        if data[i+8:i+12] == wave_signature:
            indices.append(i)
        i += 1

    if not indices:
        print("Error: No WAV headers found.")
        return

    indices.append(len(data))

    try:
        with open(names_file, 'r', encoding='utf-8', errors='ignore') as nf:
            lines = nf.readlines()
    except FileNotFoundError:
        print(f"Error: Names file not found: {names_file}")
        return

    wav_names = [re.search(r'([A-Za-z0-9_\-]+\.wav)', line) for line in lines]
    wav_names = [m.group(1) for m in wav_names if m]

    output_dir = "extracted"
    os.makedirs(output_dir, exist_ok=True)

    count = min(len(indices) - 1, len(wav_names))

    for n in range(count):
        start = indices[n]
        end = indices[n + 1]
        chunk = data[start:end]
        output_filename = f"{output_dir}/{wav_names[n]}"

        with open(output_filename, "wb") as out:
            out.write(chunk)

        print(f"Extracted: {output_filename} ({len(chunk)} bytes)")

    total_wav_chunks = len(indices) - 1
    total_names = len(wav_names)

    if total_names < total_wav_chunks:
        print(f"\nWarning: Found more WAV chunks ({total_wav_chunks}) than names ({total_names}). "
              f"The remaining chunks will be ignored.")
    elif total_names > total_wav_chunks:
        print(f"\nWarning: Found more names ({total_names}) than WAV chunks ({total_wav_chunks}). "
              f"The remaining names will not be used.")

    print(f"\nTotal WAV files extracted: {count}")

def make_names_file(wavs_path, names_file):
    """
    Generates a file list with permissions, user, size, date, and name
    formatted like a Unix-style `ls -l` output.
    """
    user = os.getenv("USER", "zope")  # default to 'zope' if not found
    with open(names_file, "w", encoding="utf-8") as f:
        for filename in sorted(os.listdir(wavs_path)):
            if not filename.lower().endswith(".wav"):
                continue

            path = os.path.join(wavs_path, filename)
            stats = os.stat(path)
            size = stats.st_size

            # Formatta la data in stile "Oct 17 15:01"
            t = time.localtime(stats.st_mtime)
            date_str = time.strftime("%b %d %H:%M", t)

            # Scrivi la riga tipo ls -l
            f.write(f"-rw-rw-r--   1 {user:<10} {size:8d} {date_str} {filename}\n")

    print(f"Generated names file: {names_file}")

def make_bin(bin_filename, wavs_path, names_file):
    """
    Combines all WAV files from a folder into a single .bin file.
    """
    with open(bin_filename, 'wb') as bin_file:
        for filename in sorted(os.listdir(wavs_path)):
            if filename.lower().endswith('.wav'):
                wav_path = os.path.join(wavs_path, filename)
                with open(wav_path, 'rb') as wav_file:
                    data = wav_file.read()
                    bin_file.write(data)
    print(f"Created BIN file: {bin_filename}")

    # Automatically regenerate names file
    make_names_file(wavs_path, names_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Extract WAVs: python c47extractor.py -e input.bin names.idx")
        print("  Make BIN:     python c47extractor.py -m output.bin wavs_folder/ names.idx")
        print("  Make Names:   python c47extractor.py -n wavs_folder/ names.idx")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "-e":
        bin_file = sys.argv[2].strip()
        names_file = sys.argv[3].strip()
        extract_wavs(bin_file, names_file)

    elif cmd == "-m":
        bin_file = sys.argv[2].strip()
        wavs_folder = sys.argv[3].strip()
        names_file = sys.argv[4].strip()
        make_bin(bin_file, wavs_folder, names_file)

    elif cmd == "-n":
        wavs_folder = sys.argv[2].strip()
        names_file = sys.argv[3].strip()
        make_names_file(wavs_folder, names_file)