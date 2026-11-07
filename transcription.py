import re
import sys
from youtube_transcript_api import YouTubeTranscriptApi

def video_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", url)
    if not m:
        raise ValueError("Invalid link")
    return m.group(1)

def transcription(url: str, languages=("pt", "en")) -> str:
    t = YouTubeTranscriptApi().fetch(video_id(url), languages=languages)
    return " ".join(s.text for s in t)

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else input("Video link: ")
    text = transcription(url)
    print(text)
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(text)
