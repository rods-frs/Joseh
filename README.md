# 🤖 Joseh — Intelligent Voice Assistant

Joseh is a lightweight Python-based voice-controlled desktop assistant that understands natural language commands, manages Spotify playback, executes system operations, and responds with text-to-speech. Built with a custom spaCy NLP model, it processes complex multi-command phrases and adapts to user workflows across Linux and Windows.

---

## ✨ Features

- **🎙️ Voice & Text Input** — Switch between speech recognition and keyboard input modes
- **🎵 Spotify Control** — Play, pause, skip, rewind, and check currently playing tracks
- **🧠 Natural Language Processing** — Custom-trained spaCy model handles complex phrases like *"pause the music and tell me the date"*
- **🖥️ System Commands** — Run package updates on Fedora/Ubuntu, install programs via package managers
- **📅 Utility Commands** — Get current date, check system info
- **🔊 Text-to-Speech** — Joseh responds audibly using pyttsx3
- **⚙️ Extensible** — Add custom commands easily through `custom_commands.py`
- **🛡️ Credential Management** — Secure password storage via system keyring

---

## 📋 Requirements

- **Python 3.12** (required; newer versions not supported)
- **OS**: Linux (Fedora/Ubuntu recommended) or Windows
- **Spotify Premium account** (for music control)
- **Microphone** (optional, for voice input)
- **System dependencies**: 
  - Linux: `python3-dev` and `portaudio` libraries (for PyAudio)
  - Windows: Visual C++ build tools (for PyAudio compilation)

### Python Dependencies

All required packages are in `requirements.txt`. Key libraries:

- **spacy** — NLP pipeline and intent recognition
- **spotipy** — Spotify Web API client
- **SpeechRecognition** — Google Speech-to-Text integration
- **pyttsx3** — Cross-platform text-to-speech
- **vosk** — Offline speech recognition (experimental)
- **keyring** — Secure credential storage

---

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/rods-frs/Joseh.git
cd Joseh
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

### 2. Configure Credentials

Run the assistant in direct command mode to set up Spotify and system credentials:

```bash
python mainV5.py
```

Then type `direct command mode` and:
- **Option 1**: Create system credentials (sudo password for updates)
- **Option 3**: Link your Spotify account via OAuth

### 3. Run

```bash
python mainV5.py
```

By default, Joseh runs in **keyboard mode**. Type a command and press Enter:

```
What's your command?
>> pause the music and tell me the date
```

---

## 🎯 Commands

### Built-in Commands

| Command | What it does |
|---------|-------------|
| `resume` | Start Spotify playback |
| `pause` | Stop Spotify playback |
| `next` | Skip to next track |
| `previous` | Go back to previous track |
| `get_music` / `what's playing` | Announce current track |
| `play [artist/song]` | Search and play from Spotify |
| `date` / `what day is it` | Say today's date |
| `update` | Run system package manager update |
| `install [program]` | Install a program (Flatpak or system PM) |
| `exit` | End the session |

### Special Modes

| Mode | Command | Function |
|------|---------|----------|
| Custom Commands | `custom command mode` | Add and execute your own functions |
| Direct Commands | `direct command mode` | Manage credentials, execute system tasks |

### Multi-Command Phrases

Joseh's NLP model handles complex chained commands:

```
"pause the music and tell me the date"
→ executes: pause, then date

"play despacito and skip to the next song"
→ executes: play_music (with entity "despacito"), then next
```

---

## ⚙️ Configuration

### Runtime Flags (mainV5.py)

```python
command_via_speech = False          # Set True for voice input
SKIP_NOUN_WARNING = True            # Suppress NLP debug messages
DEBUG_MODE = False                  # Enable verbose logging
```

### Advanced Settings

Find these in tool modules and adjust as needed:

- **Speech Recognition Timeout**: `SPEECH_WAIT_TIME` (seconds before timeout)
- **Pause Threshold**: `r.pause_threshold` in `tools/toolbox/toolboxv2.py` (silence detection)
- **TTS Speed**: `engine.setProperty('rate', 150)` (words per minute; default 200)
- **Intent Confidence**: `score >= 0.5` in model detection (lower = more permissive)

### Adding Custom Commands

Edit `custom_commands.py`:

```python
def my_command():
    print("My custom action!")
    # Add your logic here

commands_map = {
    1: exampleCommand,
    2: my_command  # Add your command here
}
```

Then in a session, type `custom command mode` and select option `2`.

---

## 📁 Project Structure

```
Joseh/
├── mainV5.py                      # Entry point, session loop, configuration flags
├── session.py                     # Session controller, command routing
├── custom_commands.py             # User-defined custom commands
├── requirements.txt               # Python dependencies
│
├── core/                          # System core modules
│   ├── builtin_commands.py        # Direct command mode (credentials, system tasks)
│   ├── credential_checker.py      # Validate stored credentials
│   ├── error_handler.py           # Custom exception classes
│   └── logging_configuration.py   # Logging setup
│
├── tools/                         # Feature modules
│   ├── spotify/
│   │   └── spotipy_commands.py    # Spotify integration (play, pause, skip)
│   │
│   ├── model/
│   │   └── model.py               # NLP pipeline (intent & entity recognition)
│   │
│   ├── toolbox/
│   │   └── toolboxv2.py           # System commands (update, date, install)
│   │
│   ├── tts/
│   │   └── voice.py               # Text-to-speech engine (pyttsx3)
│   │
│   └── stt/
│       └── recognizer.py          # Speech recognition (Google API, Vosk)
│
└── model_training/                # NLP model training scripts & data
    ├── joseh_training.py          # Intent classification trainer
    ├── joseh_ner_training.py      # Named entity recognition trainer
    ├── cat_training_data_v*.csv   # Intent training data
    └── joseh_ner_training*.csv    # Entity training data
```

### Data Flow

1. **Input** → User speaks or types a command
2. **Speech-to-Text** (if enabled) → Convert audio to text via Google Speech API
3. **NLP Pipeline** → 
   - Tokenize & lemmatize with spaCy
   - Check for direct keyword matches
   - If complex, run custom intent classifier (`joseh_model_v1`)
   - Extract entities (artist names, program names) with NER
4. **Command Execution** → Route to Spotify, system tools, or custom functions
5. **Text-to-Speech** → Respond with pyttsx3

---

## 🔧 Troubleshooting

### Speech Recognition Not Working

- Ensure internet connection (Google API required)
- Check microphone permissions: `pulseaudio` running on Linux
- Increase `pause_threshold` if Joseh cuts off mid-phrase

### Spotify Commands Failing

- Run `direct command mode` (option 3) to re-authenticate
- Verify Spotify Premium account (required for API)
- Check internet connection

### NLP Model Errors

- Ensure spaCy model is installed: `python -m spacy download en_core_web_lg`
- Clear any cached models in `.cache/` if model loading fails

### Python 3.12 Requirement

- Some dependencies (PyAudio, cryptography) may fail on Python 3.13+
- Install Python 3.12: `pyenv install 3.12.x`

---

## 🧠 How the NLP Model Works

Joseh uses a **two-stage pipeline** for intent recognition:

### Stage 1: Simple Matching
- Tokenizes input with `en_core_web_lg`
- Lemmatizes words (e.g., "playing" → "play")
- Checks for direct keyword matches in command map
- If match found → execute immediately

### Stage 2: Complex Intent Recognition
- Triggered if Stage 1 fails or input contains named entities
- Uses `joseh_model_v1` (custom-trained classifier)
- Predicts intent with confidence score
- Extracts entities using NER (Named Entity Recognition)
- Returns predicted commands + extracted data

**Example:**
- Input: *"play despacito on spotify"*
- Stage 1: No direct match (contains "despacito")
- Stage 2: Model predicts `play_music`, NER extracts entity `TRACK: despacito`
- Output: `["play_music"]` with entity data

---

## 📦 Training Custom Models

The `model_training/` directory includes scripts to retrain the intent classifier:

```bash
# Train intent classifier
python model_training/joseh_training.py

# Train entity recognition
python model_training/joseh_ner_training.py
```

**Training data format** (CSV):

| text | intent |
|------|--------|
| play music | play_music |
| pause playback | pause |
| what's the date | date |

Add examples to CSV files and re-run training scripts to improve accuracy.

---

## 🚨 Known Limitations (Alpha)

- **No offline speech recognition** — Requires Google Speech API (internet needed)
- **Limited OS support** — System commands only for Fedora/Ubuntu
- **No wake word detection** — Must manually trigger each interaction
- **ALSA noise** — Linux audio warnings are suppressed but not eliminated
- **Python 3.12 only** — Dependency conflicts with newer versions
- **Experimental voice input** — Speech-to-text mode is under development

---

## 🛠️ Development & Contributing

To extend Joseh:

1. **Add a command**: Modify `tools/toolbox/toolboxv2.py` or `custom_commands.py`
2. **Retrain NLP**: Add examples to CSVs in `model_training/`, run training scripts
3. **Fix bugs**: Open an issue with logs (enable `DEBUG_MODE = True`)
4. **Improve docs**: PRs welcome!

---

## 📄 License

This project is released as open-source. Check the repository for license details.

---

## 👤 Author

Built by **Rodrigo Silva**  
📧 [rodrigo.etc@proton.me](mailto:rodrigo.etc@proton.me)  
🔗 [GitHub: @rods-frs](https://github.com/rods-frs)  
💼 [LinkedIn](https://linkedin.com/in/rodrigo-silva)

---

## ❓ FAQ

**Q: Can I use this without Spotify?**  
A: Yes. Skip Spotify setup and use system/custom commands only.

**Q: Does Joseh work offline?**  
A: Partially. Voice input requires internet, but text commands and local operations work offline.

**Q: How do I make Joseh understand my accent better?**  
A: Retrain the model using `model_training/` scripts with examples tailored to your speech patterns.

**Q: Can I run multiple instances?**  
A: Not recommended. Each session accesses the same Spotify API credentials and system resources.

---

**🚀 Ready to try? Start with `Quick Start` above!**
