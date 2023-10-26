"""Records microphone audio using PyAudio."""

import click
from typing import List, BinaryIO, ByteString
import pyaudio 

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

def record_with_pyaudio() -> ByteString:
    """Record audio using PyAudio."""
    
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    audio = stream.read(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return audio

def record_audio(filename: str, duration) -> None:
    """Record microphone audio and save to file using PyAudio.

    Args:
        filename: Output filename to save recording to.
    """
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    frames: List[bytes] = []

    for i in range(0, int(RATE / CHUNK_SIZE * duration)):
        data = stream.read(CHUNK_SIZE)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with open(filename, 'wb') as file: 
        file.write(b''.join(frames))

@click.command()
@click.option('--filename', '-f',
                default='output.mp4',
                help='Output filename to save recording to.'
                )

# duration
@click.option('--duration', '-d',
              default=RECORD_SECONDS,
              help='Duration of recording in seconds.'
              )
def cli(filename, duration):
    """Records microphone audio to filename using PyAudio."""
    record_audio(filename, duration)
    click.echo(f'Recorded {RECORD_SECONDS} seconds of audio to {filename}')

if __name__ == '__main__':
    cli()

