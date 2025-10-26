import os
import re
import sys

def extract_wavs(input_filename, names_file):
    """
    Searches a binary file for RIFF/WAVE headers and extracts the chunks 
    as separate .wav files, naming them according to a provided list.

    Args:
        input_filename (str): Path to the binary file containing WAV data.
        names_file (str): Path to the file containing a list of desired WAV names.
    """
    try:
        # Read the entire binary file content
        with open(input_filename, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_filename}")
        return

    # Search for WAV header: RIFF + 4 bytes size + WAVE signature
    riff_header = b'RIFF'
    wave_signature = b'WAVE'

    indices = []
    i = 0
    # Loop through the data to find all occurrences of the RIFF header
    while True:
        i = data.find(riff_header, i)
        if i == -1:
            break
        # Check for the 'WAVE' signature 4 bytes after the size field (i + 8)
        if data[i+8:i+12] == wave_signature:
            indices.append(i)
        i += 1

    if not indices:
        print("Error: No WAV headers found.")
        return

    # Add the end of the file as the last index for chunk slicing
    indices.append(len(data))

    # Read the list of names from the file (line by line)
    try:
        with open(names_file, 'r', encoding='utf-8', errors='ignore') as nf:
            lines = nf.readlines()
    except FileNotFoundError:
        print(f"Error: Names file not found: {names_file}")
        return

    # Extract .wav file names using regex
    # Searches for a string ending in .wav (allowing alphanumeric, underscore, and hyphen)
    wav_names = [re.search(r'([A-Za-z0-9_\-]+\.wav)', line) for line in lines]
    wav_names = [m.group(1) for m in wav_names if m]

    # Create the output directory
    output_dir = "extracted"
    os.makedirs(output_dir, exist_ok=True)

    # Determine the number of files to extract (limited by the smallest list)
    count = min(len(indices) - 1, len(wav_names))

    # Iterate and extract the WAV chunks
    for n in range(count):
        start = indices[n]
        end = indices[n + 1]
        chunk = data[start:end]
        output_filename = f"{output_dir}/{wav_names[n]}"

        with open(output_filename, "wb") as out:
            out.write(chunk)

        print(f"Extracted: {output_filename} ({len(chunk)} bytes)")

    # Handle count mismatch warnings
    total_wav_chunks = len(indices) - 1
    total_names = len(wav_names)

    if total_names < total_wav_chunks:
        print(f"\nWarning: Found more WAV chunks ({total_wav_chunks}) than names ({total_names}). "
              f"The remaining chunks will be ignored.")
    elif total_names > total_wav_chunks:
        print(f"\nWarning: Found more names ({total_names}) than WAV chunks ({total_wav_chunks}). "
              f"The remaining names will not be used.")

    print(f"\nTotal WAV files extracted: {count}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # Corrected usage to require both files
        print("Usage: python c47extractor.py *.bin *.idx")
        print("Please provide the binary file and the names list file.")
    else:
        bin_file = sys.argv[1].strip()
        names_file = sys.argv[2].strip()
        extract_wavs(bin_file, names_file)