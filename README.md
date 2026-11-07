# youtube_ciscraper

Fetch the transcript of a YouTube video and ask Claude questions about it from your terminal.

The project has two small scripts:

- **`transcription.py`** downloads a video's transcript and saves it to `transcription.txt`.
- **`ask_claude.py`** loads a transcript (from a YouTube link, a text file, or pasted text) and lets you send it to Claude with your own prompts, one after another.

`ask_claude.py` calls the [Claude Code](https://claude.com/claude-code) CLI (`claude -p`), so it runs on your Claude subscription. You don't need an API key or API credits.

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

### Download a transcript

```bash
python transcription.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"
```

The script prints the transcript and writes it to `transcription.txt` in the current folder. If you leave out the link, it asks for one.

It looks for a Portuguese transcript first and falls back to English. To change that order, edit the `languages` default in `transcription()`.

Supported link formats:

- `https://www.youtube.com/watch?v=<id>`
- `https://youtu.be/<id>`
- `https://www.youtube.com/shorts/<id>`
- `https://www.youtube.com/embed/<id>`

### Ask Claude about a video

`ask_claude.py` accepts three kinds of input:

```bash
# 1. A YouTube link: the transcript is fetched for you
python ask_claude.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"

# 2. A text file, such as one saved by transcription.py
python ask_claude.py transcription.txt

# 3. Nothing: paste text, then type END on its own line
python ask_claude.py
```

When the text has loaded, the script asks for a prompt. Type a question or instruction (for example, *"Summarise this in five bullet points"* or *"List every exercise mentioned and how to do it"*) and Claude replies. You can keep asking about the same transcript. Press Enter on an empty prompt to quit.

Claude answers in the language you write the prompt in.

## How it works

- `transcription.py` takes the 11-character video ID from the link and uses `youtube-transcript-api` to download the captions. It then joins them into one block of text.
- `ask_claude.py` wraps the transcript in `<transcript>` tags and adds a short instruction telling Claude to treat it as material to analyse, not as instructions. Your prompt goes after it.
- The message reaches `claude -p` through stdin, which avoids the Windows command-line length limit on long transcripts.
- `ANTHROPIC_API_KEY` is removed from the environment before Claude Code is called, so the request uses your subscription login and is not billed to the API.

## Limitations

- A transcript can only be fetched if the video has captions, either uploaded or auto-generated, in one of the requested languages.
- YouTube may block or rate-limit transcript requests, especially from cloud servers or after many requests in a row.
- Each prompt sends the full transcript again, so very long videos use more of your Claude usage.

## Project structure

```
youtube_ciscraper/
├── ask_claude.py      # Interactive Q&A over a transcript using Claude Code
├── transcription.py   # Fetches a YouTube transcript and saves it to transcription.txt
└── transcription.txt  # Sample output (transcript of the most recent run)
```
