# C47SpeechExtractor

A powerful yet simple tool to extract, rebuild, and manage WAV audio files from the **Hitman: Codename 47** `.bin` archives.

## Features

- Extract WAV files directly from a .bin file
- Rebuild a .bin archive from a folder of WAV files
- Generate .idx-style name lists compatible with the original game format
- Cross-platform (Windows / Linux / macOS)
- No dependencies – pure Python 3

## Usage

### Extract WAV files

Extracts all WAV chunks from a `.bin` file using a `.idx` names file:

```bash
python c47extractor.py -e input.bin names.idx
```

### Create a BIN file

Combines all .wav files from a folder into a single .bin file:

```bash
python c47extractor.py -m output.bin wavs_folder/ names.idx
```

This will also automatically regenerate the names file (names.idx) to match your WAV folder.

### Generate a Names File

Generates a .idx-style file from an existing folder of WAVs:

```bash
python c47extractor.py -n wavs_folder/ names.idx
```

Each entry is formatted similarly to the Unix ls -l output.
Example output line:

```bash
-rw-rw-r--   1 zope       13284 Oct 17 15:01 speech_001.wav
```

## Notes

- The .idx file must contain valid .wav filenames in its text (one per line or formatted like ls -l).
- If there are more WAV chunks than names, the script will warn you and skip the extra ones.
- Likewise, if there are more names than WAVs, unused names will be ignored.

## Requirements

Just Python 3.7 or higher
