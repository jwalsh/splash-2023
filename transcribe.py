import os
import time
import ffmpeg
import assemblyai
import click
import whisper
from dataclasses import dataclass
from typing import List, BinaryIO, ByteString, Dict
from enum import Enum

import subprocess
from pync import Notifier
import sox
import pyaudio


## Usage
# test-transcribe:
# 	poetry run python transcribe.py
# test-transcribe-model:
# 	poetry run python transcribe.py -w -m small
# test-transcribe-duration:
# 	poetry run python transcribe.py --d 60
# test-transcribe-file:
# 	poetry run python transcribe.py --input file transcript.json
# test-transcribe-phrase:
# 	poetry run python transcribe.py --phrase "bingo"
# test-transcribe-output:
# 	poetry run python transcribe.py --output my-transcripts


# TODO: Action to take when phrase is detected
# $ python app.py transcribe -m small  # core scenario 1
# $ python app.py summarize transcript.json # core scenario 2
# $ python app.py listen # core scenario 3


class RecordingSource(Enum):
    PYAUDIO = "pyaudio"
    FFMPEG = "ffmpeg"
    SOX = "sox"
    UNKNOWN = "unknown"

class TranscriberSource(Enum):
    ASSEMBLYAI = 'assemblyai'
    WHISPER = 'whisper'
    UNKNOWN = 'unknown'
    
@dataclass
class Recording:
    """Represents an audio recording."""

    file: BinaryIO
    duration: float
    source: RecordingSource
    date: str
    transcript: str = ""

    def __post_init__(self):
        self.transcribe()

    def transcribe(self):
        # Transcribe audio to text
        self.transcript = "TODO: Transcribe audio to text"

    def to_bytes(self) -> ByteString:
        # return the bytes of the source file
        return self.file.read()

    def to_file(self, filename: str) -> None:
        # save the source file to disk
        with open(filename, "wb") as f:
            f.write(self.file)

    def transcribe(self) -> str:
        transcript_text = "Transcript text..."
        self.transcript = transcript_text
        return transcript_text

    def __str__(self):
        return f"Recording({self.source}, {self.duration}s)"

    def __repr__(self):
        return str(self)


@dataclass
class Segment:
    id: int
    seek: int
    start: float
    end: float
    text: str
    tokens: List[int]
    temperature: float
    avg_logprob: float
    compression_ratio: float
    no_caption_prob: float


@dataclass
class Transcript:
    text: str
    segments: List[Segment]
    language: str


def load_transcript(data: Dict) -> Transcript:
    return Transcript(
        text=data["text"],
        segments=[Segment(**s) for s in data["segments"]],
        language=data["language"],
    )


def take_action(transcript):
    click.echo(f"Taking action for: {transcript}")
    click.echo("\a")  # Terminal bell
    # e.g. send to a chatbot, or a home automation system
    Notifier.notify(
        f'Action taken for "{transcript}"', title="Transcribe", sound="default"
    )


def check_transcript(transcript, phrase):
    click.echo(f"Checking transcript for {phrase}")
    if phrase in transcript:
        click.echo("\a")  # Terminal bell
        take_action(transcript)

def transcribe_audio():
    pass

def record_audio(use_sox: bool, use_pyaudio: bool) -> ByteString:
    """Capture audio from microphone."""
    if use_sox:
        return record_with_sox()

    elif use_pyaudio:
        return record_with_pyaudio()

    else:
        return record_with_ffmpeg()


def record_with_sox() -> ByteString:
    """Record audio using SoX."""
    pass


def record_with_pyaudio() -> ByteString:
    """Record audio using PyAudio."""
    # WIP
    return (
        pyaudio.PyAudio()
        .open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024,
        )
        .read(1024)
    )


def record_with_ffmpeg() -> ByteString:
    """Record audio using FFmpeg."""
    # WIP

    pass


# def transcribe(audio: ByteString) -> str:
#     """Transcribe audio using selected service."""
#     pass


@dataclass
class Phrase:
    text: str
    compliance: int


# Distinctive - Easily distinguished from normal speech to avoid false positives.
# Concise - Shorter phrases are easier for speech recognition.
# Literal - Avoid figurative language that could be misinterpreted.
# Upbeat - Positive phrases sound more natural as exclamations.
# Clear intent - Obvious meaning and purpose.
# Unambiguous - No room for misinterpretation.
PHRASES = [
    Phrase("Begin action", 9),
    Phrase("Let's get started", 8),
    Phrase("Commence plan", 7),
    Phrase("Initiate sequence", 6),
    Phrase("Launch operations", 5),
    Phrase("bingo", 7),
    Phrase("eureka", 8),
    Phrase("shiny", 6),
    Phrase("hallelujah", 6),
    Phrase("kablam", 5),
    Phrase("kaboom", 4),
    Phrase("squee", 4),
    Phrase("totes", 2),
    Phrase("test", 1),
]


ACTIONS_MIDDLEWARE = []


@click.command()
@click.argument("filename", default="output.mp4")
@click.option(
    "-d", "--chunk-duration", default=10, type=int, help="Recording duration in seconds"
)
@click.option("-k", "--api-key", envvar="ASSEMBLYAI_API_KEY", help="AssemblyAI API key")
@click.option(
    "-o",
    "--output-dir",
    default="transcripts",
    help="Output directory for generated files",
)
@click.option(
    "-w",
    "--whisper",
    is_flag=True,
    help="Use Whisper to transcribe rather than AssemblyAI",
)
@click.option(
    "-m",
    "--model",
    default="base",
    help="Whisper model name (base, small, medium, large)",
)
@click.option("-i", "--input", type=click.Choice(["mic", "file"]), default="mic")
@click.option(
    "--phrase",
    type=click.Choice([p.text for p in PHRASES], case_sensitive=False),
    default="eureka",
)
@click.option("--save", is_flag=True, default=True, help="Save audio and transcripts")
@click.option("--activate", is_flag=True, default=True, help="Activate on a phrase")
def cli(
    filename: str,
    chunk_duration: int,
    api_key: str,
    output_dir: str,
    whisper: bool,
    model: str,
    input: str,
    phrase: str,
    save: bool,
    activate: bool,
):
    """Transcribe audio file using FFmpeg and AssemblyAI API."""

    # WIP: The audio input and transcriptions should use the following: 
    # audio = record_audio(use_sox, use_pyaudio)
    # transcription =  transcribe(audio)

    os.makedirs(output_dir, exist_ok=True)

    # TODO: def transcribe()
    if whisper:
        from whisper import Whisper
        transcriber_source = TranscriberSource.WHISPER

        # ~/opt/whisper has the models
        whisper = Whisper(model=model)

        click.echo(f"Using Whisper model {model}")
        
        # audio = ... # load audio

        # p = subprocess.run(['~/opt/whisper.cpp', '--audio=-'], input=audio, capture_output=True)
        # transcript = p.stdout.decode('utf-8')
        # click.echo(transcript)
    else:
        transcriber_source = TranscriberSource.ASSEMBLYAI
        # Error if we're using AssemblyAI but don't have an API key
        if not api_key:
            raise click.UsageError("API key required for AssemblyAI")
        # Warn if the user has passed the model since that is not used with AssemblyAI
        if model:
            click.echo("Warning: model is not used with AssemblyAI")
        assemblyai.api_key = api_key
        transcriber = assemblyai.Transcriber()

    click.echo(f"Using {transcriber_source} for transcription")


    uri = filename  # Use filename provided as argument

    if input == "file":
        transcriber.transcribe(uri)
        return
    
    while True:
        # Show when we're recording
        click.echo()
        click.echo(
            f"Recording for {chunk_duration} seconds starting at {time.strftime('%H:%M:%S')}"
        )
        click.echo()
        uri = os.path.join(output_dir, f"{int(time.time())}-{filename}")
        # uri = filename

        # WIP: swap out the record_audio function based on the options
        # uri = record_audio(use_sox, use_pyaudio)

        stream = ffmpeg.input(
            ":0", f="avfoundation", ac=2, t=chunk_duration
        )  # type: ffmpeg.nodes.Stream
        stream = ffmpeg.output(stream, uri)
        ffmpeg.run(stream)

        start_time = time.time()

        click.echo(f"Started transcription at {time.strftime('%H:%M:%S')}") 

        if whisper:
            transcript = None
        else:
            transcript = transcriber.transcribe(uri)


        end_time = time.time()

        duration = end_time - start_time 

        click.echo(f"Finished transcription at {time.strftime('%H:%M:%S')}, took {duration:.2f} seconds")


        transcript_text = transcript.text
        if not transcript_text:
            click.echo("No transcript generated")
            continue

        click.echo(
            click.style(
                f"Transcript: {transcript_text}",
                fg='green', bold=True
            )
        )        

        transcript_file = os.path.join(output_dir, f"{int(time.time())}.txt")

        if save:
            click.echo(f"Writing transcript to {transcript_file}")
            with open(transcript_file, "w") as f:
                f.write(transcript.text)
        else:
            click.echo(f"Not saving transcript and removing {uri}")
            os.remove(uri)

        if activate:
            check_transcript(transcript_text, phrase)


if __name__ == "__main__":
    cli()




