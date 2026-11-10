# youtube_ciscraper

Fetch the transcript of a YouTube video and ask Claude questions about it from your terminal.

The main script is **`ask_claude.py`**. Give it a YouTube link and it fetches the transcript itself, then lets you send it to Claude with your own prompts, one after another. Answers are saved to an Obsidian note. You don't need to download or save the transcript yourself.

A second, optional script, **`transcription.py`**, only downloads a transcript to a text file. `ask_claude.py` uses its fetching code, but you never have to run it.

`ask_claude.py` calls the [Claude Code](https://claude.com/claude-code) CLI (`claude -p`), so it runs on your Claude subscription. You **don't need an API key or API credits**.

## Requirements

- Python 3.9 or later
- [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/)
- The Claude Code CLI, installed and logged in (needed only for `ask_claude.py`)

## Installation

```bash
git clone <repository-url>
cd youtube_ciscraper

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install youtube-transcript-api
```

Install Claude Code and run `claude` once so it can log you in.

## Usage

### Ask Claude about a video

`ask_claude.py` accepts three kinds of input:

```bash
# 1. A YouTube link: the transcript is fetched for you
python ask_claude.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"

# 2. Any text file
python ask_claude.py notes.txt

# 3. Nothing: paste text, then type END on its own line
python ask_claude.py
```

It looks for a Portuguese transcript first and falls back to English. To change that order, edit the `languages` default in `transcription()` in `transcription.py`.

Supported link formats:

- `https://www.youtube.com/watch?v=<id>`
- `https://youtu.be/<id>`
- `https://www.youtube.com/shorts/<id>`
- `https://www.youtube.com/embed/<id>`

When the text has loaded, the script asks for a prompt. Type a question or instruction (for example, *"Summarise this in five bullet points"*) and Claude replies. You can keep asking about the same transcript. Press Enter on an empty prompt to quit.

Claude answers in the language you write the prompt in.

To ask a single question and exit, pass the prompt as a second argument:

```bash
python ask_claude.py "https://www.youtube.com/watch?v=XXXXXXXXXXX" "Summarise this in five bullet points"
```

### Answers in Obsidian

Every answer is also saved to an [Obsidian](https://obsidian.md) note, which opens in Obsidian after the first answer:

- The note is created at `<vault>/YouTube/<video title>.md`. It has the video link in its properties, the transcript in a folded callout, and one section per prompt with Claude's answer.
- Asking about the same video again adds to the existing note.
- When you start `ask_claude.py` without an argument (or double-click `ask_claude.bat`), it lists your 10 most recent videos. Pick a number to keep asking about that video: the transcript is read back from its note, so YouTube isn't contacted again. You can also pass a note's path, or drag the note onto `ask_claude.bat`.
- The default vault is `Documents/Obsidian Vault` in your home folder. To use another vault, set the `OBSIDIAN_VAULT` environment variable to its folder, for example `setx OBSIDIAN_VAULT "C:\Users\me\Documents\Vault Tese"` on Windows. To change the folder inside the vault, edit `OBSIDIAN_FOLDER` in `ask_claude.py`.
- If the vault folder doesn't exist, answers are only printed.

### Only download a transcript (optional)

If you just want the transcript as a text file, without Claude:

```bash
python transcription.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"
```

It prints the transcript and writes it to `transcription.txt` in the current folder. `ask_claude.py` does not use or create this file.

### Windows launcher

On Windows, double-click `ask_claude.bat` to start `ask_claude.py` in a console window with the project's virtual environment. You can also drag a `.txt` file onto it to load that file. To launch it from the Desktop, right-click `ask_claude.bat` → *Show more options* → *Send to* → *Desktop (create shortcut)*.

## How it works

- `transcription.py` takes the 11-character video ID from the link and uses `youtube-transcript-api` to download the captions. It then joins them into one block of text.
- `ask_claude.py` wraps the transcript in `<transcript>` tags and adds a short instruction telling Claude to treat it as material to analyse, not as instructions. Your prompt goes after it.
- The message reaches `claude -p` through stdin, which avoids the Windows command-line length limit on long transcripts.
- `ANTHROPIC_API_KEY` is removed from the environment before Claude Code is called, so the request uses your subscription login and is not billed to the API.
- The video title for the note's name comes from YouTube's public oEmbed endpoint. If that lookup fails, the note is named after the video ID.
- The note is opened with an `obsidian://open?path=...` link. Obsidian reloads it by itself when more answers are added.

## Limitations

- A transcript can only be fetched if the video has captions, either uploaded or auto-generated, in one of the requested languages.
- YouTube may block or rate-limit transcript requests, especially from cloud servers or after many requests in a row.
- Each prompt sends the full transcript again, so very long videos use more of your Claude usage.

## Project structure

```
youtube_ciscraper/
├── ask_claude.bat     # Windows double-click launcher for ask_claude.py
├── ask_claude.py      # Interactive Q&A over a transcript using Claude Code
└── transcription.py   # Fetches a YouTube transcript (used by ask_claude.py; can also save it to a file)
```
