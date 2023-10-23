import os
import subprocess
import yt_dlp
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def download_captions(url):
    options = {
        'writesubtitles': True,
        'allsubtitles': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def summarize_text(file, sentences=10):
    parser = PlaintextParser.from_file(file, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences)
    return summary

def main():
    url = input("Enter video URL: ")
    download_captions(url)

    file = input('Enter subtitle file path to summarize: ')
    summary = summarize_text(file)
    print("Summary:\n", "\n".join(str(s) for s in summary))

if __name__ == "__main__":
    main()
