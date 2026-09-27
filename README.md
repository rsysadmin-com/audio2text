# audio2text

A simple command-line tool for transcribing audio files locally using [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

`audio2text` is designed to do one thing and keep it simple:

```bash
audio2text recording.ogg
```

The transcription is performed locally on your computer. Your audio files are not uploaded to an external transcription service.

## Features

* Local audio transcription using faster-whisper
* Automatic language detection
* Optional language selection
* Multiple audio files in a single command
* Optional timestamps
* Optional transcript export to a text file
* Configurable Whisper model
* CPU and CUDA support
* Voice Activity Detection (VAD)
* No cloud transcription service required

## Requirements

You need:

* Linux
* Python 3.10 or newer
* `pipx`

The Whisper model is downloaded automatically the first time it is needed, so an Internet connection is required for the initial model download.

After that, transcription itself is performed locally.

## Installation

### 1. Install pipx

First check whether `pipx` is already installed:

```bash
pipx --version
```

If that prints a version number, you can continue to the next step.

If `pipx` is not installed, install it using your Linux distribution's package manager.

For example, on Arch Linux and Arch-based distributions:

```bash
sudo pacman -S python-pipx
```

On Debian/Ubuntu:

```bash
sudo apt install pipx
```

Then make sure the directory used by `pipx` is in your `PATH`:

```bash
pipx ensurepath
```

After running this command, open a new terminal.

### 2. Clone audio2text

```bash
git clone https://github.com/rsysadmin-com/audio2text.git
cd audio2text
```

### 3. Install audio2text

From inside the repository:

```bash
pipx install .
```

That's it.

You can now run:

```bash
audio2text --version
```

Expected output:

```text
audio2text 0.1.0
```

You can also verify that the command is available:

```bash
which audio2text
```

A typical installation will show something similar to:

```text
/home/your-user/.local/bin/audio2text
```

## Quick start

Transcribe an audio file:

```bash
audio2text recording.ogg
```

Example output:

```text
Loading model 'large-v3' on cpu...

===== recording.ogg =====
[Language: en (99.8%)]
Hello, this is an example audio recording.
```

The detected language and confidence are displayed automatically when language detection is enabled.

## Usage

```text
usage: audio2text [-h] [-V] [-l LANGUAGE] [-m MODEL]
                  [-d {cpu,cuda,auto}]
                  [--compute-type COMPUTE_TYPE]
                  [-t] [-o]
                  files [files ...]
```

### Options

```text
-h, --help
    Show the help message and exit.

-V, --version
    Show the installed audio2text version and exit.

-l, --language LANGUAGE
    Language code such as en, es, de or pt.
    Default: auto

-m, --model MODEL
    Whisper model to use.
    Default: large-v3

-d, --device {cpu,cuda,auto}
    Device used for inference.
    Default: cpu

--compute-type COMPUTE_TYPE
    CTranslate2 compute type, for example:
    int8, float16 or float32

-t, --timestamps
    Include timestamps in the transcript.

-o, --output
    Save the transcript to a text file.
```

## Language detection

By default, `audio2text` lets Whisper detect the language automatically:

```bash
audio2text recording.ogg
```

Example:

```text
===== recording.ogg =====
[Language: pt (99.9%)]
Bom dia, como é que você está?
```

You can force a specific language using `-l` or `--language`:

```bash
audio2text -l pt recording.ogg
```

Other examples:

```bash
audio2text -l en recording.ogg
audio2text -l es recording.ogg
audio2text -l de recording.ogg
```

For very short recordings, specifying the language manually can sometimes improve transcription accuracy.

## Multiple files

You can transcribe several files with one command:

```bash
audio2text recording1.ogg recording2.ogg recording3.ogg
```

Shell wildcards also work:

```bash
audio2text *.ogg
```

Or, for example:

```bash
audio2text -l pt *.ogg
```

The Whisper model is loaded once and reused for all files.

Each transcription is clearly separated:

```text
===== recording1.ogg =====
First transcription...

===== recording2.ogg =====
Second transcription...
```

## Timestamps

Use `-t` or `--timestamps` to include timestamps:

```bash
audio2text -t recording.ogg
```

Example:

```text
===== recording.ogg =====
[Language: pt (99.9%)]
[00:00:00.000 --> 00:00:02.840] Bom dia, como é que você está?
[00:00:03.720 --> 00:00:10.800] Vou falar devagar, e mediante o áudio eu vou aumentando a velocidade.
```

## Saving the transcript

By default, the transcription is printed to the terminal.

Use `-o` or `--output` to also save it to a text file:

```bash
audio2text -o recording.ogg
```

The file is created in the current directory with a name similar to:

```text
transcript_20260927_153045.txt
```

You can combine output files and timestamps:

```bash
audio2text -t -o recording.ogg
```

Multiple input files are stored in the same transcript file:

```bash
audio2text -t -o *.ogg
```

## Whisper models

The default model is:

```text
large-v3
```

You can select another model using `-m` or `--model`:

```bash
audio2text -m medium recording.ogg
```

For example:

```bash
audio2text -m small recording.ogg
audio2text -m medium recording.ogg
audio2text -m large-v3 recording.ogg
```

Smaller models generally require fewer resources and run faster, while larger models generally provide better transcription accuracy.

## CPU

CPU transcription is the default:

```bash
audio2text recording.ogg
```

This is equivalent to:

```bash
audio2text --device cpu recording.ogg
```

When running on CPU and no compute type is specified, `audio2text` uses:

```text
int8
```

You can explicitly select another compute type:

```bash
audio2text --device cpu --compute-type float32 recording.ogg
```

## NVIDIA CUDA

If your system has a compatible NVIDIA GPU and the required CUDA libraries, you can use:

```bash
audio2text --device cuda --compute-type float16 recording.ogg
```

CUDA support depends on your local NVIDIA/CUDA environment and the requirements of CTranslate2/faster-whisper.

If CUDA is not correctly configured, use CPU mode instead:

```bash
audio2text --device cpu recording.ogg
```

## Automatic device selection

You can let the underlying inference engine select the device:

```bash
audio2text --device auto recording.ogg
```

## Supported audio formats

`audio2text` uses faster-whisper and its underlying audio decoding stack.

Common formats such as the following should work:

```text
.ogg
.mp3
.wav
.m4a
.flac
```

Other formats supported by the underlying decoder may also work.

No manual audio conversion is normally required.

## WhatsApp voice messages

One of the original use cases for `audio2text` was transcribing WhatsApp voice messages.

For example:

```bash
audio2text "WhatsApp Ptt 2026-09-25 at 16.37.21.ogg"
```

Or several messages:

```bash
audio2text *.ogg
```

Add timestamps if desired:

```bash
audio2text -t *.ogg
```

## Privacy

Transcription is performed locally on your machine.

Audio files are not uploaded to an external transcription service.

Whisper model files may need to be downloaded when a model is used for the first time. Once the model is available locally, the actual audio transcription is performed locally.

This makes `audio2text` useful when you do not want to send recordings to an online transcription service.

## Updating audio2text

If you installed `audio2text` from a cloned Git repository using `pipx`, update the repository first:

```bash
cd audio2text
git pull
```

Then reinstall it:

```bash
pipx install . --force
```

You can verify the installed version with:

```bash
audio2text -V
```

## Uninstalling

If you installed `audio2text` using `pipx`:

```bash
pipx uninstall audio2text
```

This removes the application and its isolated Python environment.

---

# Development

The following section is only needed if you want to modify or contribute to `audio2text`.

Normal users do **not** need to create a virtual environment manually.

## Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/audio2text.git
cd audio2text
```

## Create a development environment

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Your shell should now be using the Python interpreter inside `.venv`.

You can verify this with:

```bash
which python
```

It should point somewhere inside:

```text
audio2text/.venv/
```

## Install the project in editable mode

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install `audio2text` in editable mode:

```bash
python -m pip install -e .
```

Editable mode means that changes made to the source code are immediately available without reinstalling the package after every edit.

You can test it with:

```bash
audio2text -V
audio2text --help
```

## Using pipx during development

Alternatively, you can expose the development version as a normal user command using `pipx`:

```bash
pipx install -e .
```

This creates an isolated environment managed by `pipx` while keeping the installation linked to your source tree.

The command will normally be available as:

```text
~/.local/bin/audio2text
```

This is useful if you want to run your development version from anywhere on the system.

## Building a release

Install the Python build tool inside the development virtual environment:

```bash
source .venv/bin/activate
python -m pip install build
```

Build the source distribution and wheel:

```bash
python -m build
```

A successful build creates:

```text
dist/
├── audio2text-0.1.0-py3-none-any.whl
└── audio2text-0.1.0.tar.gz
```

The version number comes from `pyproject.toml`.

## Testing the built wheel

Before publishing a release, it is a good idea to test the actual wheel rather than only the development installation.

Leave the development virtual environment:

```bash
deactivate
```

Remove any existing `pipx` installation:

```bash
pipx uninstall audio2text
```

Install the newly built wheel:

```bash
pipx install ./dist/audio2text-0.1.0-py3-none-any.whl
```

Check the installation:

```bash
which audio2text
audio2text -V
audio2text --help
```

Then perform a real transcription:

```bash
audio2text recording.ogg
```

Or test timestamps:

```bash
audio2text -t recording.ogg
```

If that works, you have tested the complete path:

```text
source code
    ↓
source distribution
    ↓
wheel
    ↓
pipx installation
    ↓
audio2text command
    ↓
real transcription
```

## Project structure

```text
audio2text/
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
└── src/
    └── audio2text/
        ├── __init__.py
        └── cli.py
```

The main CLI implementation lives in:

```text
src/audio2text/cli.py
```

Package metadata, dependencies, version information and the command-line entry point are defined in:

```text
pyproject.toml
```

The command-line entry point is:

```toml
[project.scripts]
audio2text = "audio2text.cli:main"
```

## Versioning

The project version is defined in one place:

```toml
[project]
version = "0.1.0"
```

in `pyproject.toml`.

The installed version can be checked with:

```bash
audio2text -V
```

Do not duplicate the version number in the Python source code.

## Design philosophy

`audio2text` is intentionally small.

The basic use case should remain:

```bash
audio2text recording.ogg
```

Additional features should be optional and should not make the simple case complicated.

The goal is not to become an audio editor, translation service or large transcription platform.

It is a small Unix-style command-line tool that turns audio into text.

## License

MIT License.

See [LICENSE](LICENSE) for details.

## Disclaimer

This software is provided on an "AS IS" basis. The author is not to be held responsible for any damage, data loss, or other consequences resulting from its use or misuse.
