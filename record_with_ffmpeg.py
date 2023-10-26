import click
import ffmpeg
import os

from typing import List, BinaryIO, ByteString
from dataclasses import dataclass
from typing import BinaryIO
from enum import Enum

class RecordingSource(Enum):
    PYAUDIO = 'pyaudio' 
    FFMPEG = 'ffmpeg'
    SOX = 'sox'
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
        return "Transcript text..."

    def __str__(self):
        return f"Recording({self.source}, {self.duration}s)"

    def __repr__(self):
        return str(self)


def record_with_pyaudio() -> Recording:
    """Record audio using PyAudio."""
    pass


def record_with_ffmpeg(duration) -> Recording:
    """Record audio using ffmpeg."""
    output_filename = "output.wav"
    stream = ffmpeg.input(":0", f="avfoundation", ac=1, t=duration).output(
        output_filename
    )

    try:
        ffmpeg.run(stream)
    except ffmpeg.Error as e:
        print(e.stderr)

    print("Recording finished")
    record_bytes = open("output.wav", "rb").read()
    os.remove("output.wav")

    return Recording(record_bytes, duration, RecordingSource.FFMPEG, "2020-01-01")


def record_with_sox(duration) -> Recording:
    """Record audio using SoX."""
    pass


def record_audio(duration, use_sox: bool, use_pyaudio: bool) -> ByteString:
    """Capture audio from microphone."""
    # Only one of these will be True
    if use_pyaudio and use_sox:
        raise ValueError("Only one of use_sox or use_pyaudio can be True")

    if use_sox:
        return record_with_sox()

    elif use_pyaudio:
        return record_with_pyaudio()

    else:
        return record_with_ffmpeg(duration)


@click.command()
@click.option(
    "--filename",
    "-f",
    default="output.wav",
    help="Output filename to save recording to.",
)
@click.option("--duration", "-d", default=10, help="Duration of recording in seconds.")
def cli(filename, duration):
    recording = record_audio(duration, False, False)
    recording.to_file(filename)
    print(f"Recorded {duration} seconds to {filename}")


if __name__ == "__main__":
    cli()
