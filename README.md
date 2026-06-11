# 🤖 Joseh — Voice Assistant

> ⚠️ **Alpha Software** — Joseh is in early alpha. Expect rough edges, missing features, and breaking changes between versions. Contributions and bug reports are welcome.

Joseh is a voice-controlled desktop assistant built in Python. It understands natural speech, recognizes intent through a custom spaCy NLP model, and can execute system and Spotify commands — all hands-free.

---

## Features

- 🎙️ **Voice or text input** — toggle between speech recognition and keyboard input
- 🎵 **Spotify control** — play, pause, skip, go back, and check what's currently playing
- 🧠 **NLP intent recognition** — uses a custom-trained spaCy model to handle complex, multi-command phrases like *"pause the music and then tell me the date"*
- 🖥️ **System commands** — run system updates on Fedora and Ubuntu
- 📅 **Date reporting** — ask Joseh what day it is
- 🔊 **Text-to-speech responses** — Joseh talks back via pyttsx3

---

## How It Works

Joseh processes each command through a two-stage pipeline:

1. **Simple command check** — uses `en_core_web_lg` (spaCy base model) to tokenize and lemmatize the input, looking for direct keyword matches against the command map. If a match is found with no named entities, it runs immediately.

2. **Complex command handling** — if the input contains named entities or doesn't match any keyword directly, it's passed to `joseh_model_v1`, Joseh's custom-trained intent classifier. The input is first split on conjunctions (*and*, *then*, *also*, *,*) so multi-intent commands are handled correctly.

---

## Requirements

- Python 3.12 (newer version DOES NOT WORKS)
- Linux (Fedora or Ubuntu recommended) or Windows
- A Spotify Premium account
- A microphone (if using voice input)

### Python dependencies

```
spacy
spotipy
speechrecognition
pyttsx3
distro
```

You'll also need the spaCy models:

```bash
python -m spacy download en_core_web_lg
```

---

## Setup

1. Clone the repository and install dependencies:

```bash
git clone https://github.com/rods-frs/joseh
cd joseh
pip install -r requirements.txt
```

2. Run:

```bash
python mainV4.py
```

---

## Configuration

The parameters below are at the top of `mainV4.py` and are the main knobs for customizing Joseh's behavior:

| Parameter | Default | Description |
|---|---|---|
| `COMMAND_VIA_SPEECH` | `True` | Set to `False` to disable voice input and use keyboard only |
| `SYSTEM_PASSWORD` | `"herocraft"` | Sudo password used for system update commands |
| `SPEECH_WAIT_TIME` | `10` | Max seconds Joseh listens for a phrase before timing out |

Additionally, in `joseh_toolbox.py`:

| Parameter | Location | Description |
|---|---|---|
| `r.pause_threshold` | `speech_recognition_configuration()` | Seconds of silence before a phrase is considered finished. Increase if Joseh cuts you off too early |
| `engine.setProperty('rate', 150)` | `tts_configuration()` | TTS speech rate (words per minute). Default pyttsx3 is 200 |
| `score >= 0.5` | `intent_recognition()` | Confidence threshold for accepting an intent from the NLP model. Lower = more permissive, higher = stricter |

---

## Available Commands

| Command | What it does |
|---|---|
| `resume` | Resumes Spotify playback |
| `pause` | Pauses Spotify playback |
| `next` | Skips to the next track |
| `previous` | Goes back to the previous track |
| `get_music` | Tells you what's currently playing |
| `date` | Tells you today's date |
| `update` | Runs a system package update (Fedora/Ubuntu) |
| `exit` | Ends the session |

Commands can be chained naturally — e.g., *"pause the music and tell me the date"* — and Joseh will execute each in sequence.

---

## Project Structure

```
joseh/
├── mainV4.py          # Entry point, main loop, parameter config
├── joseh_toolbox.py   # All core functions (setup, commands, NLP, TTS)
└── joseh_model_v1/    # Custom spaCy intent classification model
```

---

## Known Limitations (Alpha)

- Speech recognition depends on Google's API (`recognize_google`), requiring an internet connection
- System update commands only support Fedora and Ubuntu
- No wake word detection — each interaction requires a manual Enter press
- ALSA error suppression is hardcoded (Linux-specific); may behave unexpectedly on other setups

---

## Author

Made by [Rodrigo](https://linkedin.com/in/rodrigo-silva) • [rodrigo.etc@proton.me](mailto:rodrigo.etc@proton.me) • [@rods-frs](https://github.com/rods-frs)
