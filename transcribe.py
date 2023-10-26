import os
import time
import ffmpeg
import assemblyai
import click
import whisper
from dataclasses import dataclass
from typing import List, Dict
import subprocess

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
    text=data['text'],
    segments=[Segment(**s) for s in data['segments']], 
    language=data['language']
  )

def take_action(transcript):
    click.echo(f"Taking action for: {transcript}")
    click.echo('\a') # Terminal bell
    # e.g. send to a chatbot, or a home automation system


def check_transcript(transcript, phrase):
  if phrase in transcript: 
    click.echo('\a') # Terminal bell
    take_action(transcript)

PHRASES = [
    'eureka',
    'bingo',
    'jackpot',
    'breakthrough',
    'hallelujah',
    'shazam',
    'bippity-boppity-boo',
    'hocus-pocus',
    'sim-sala-bim',
    'bamboozled',
]

@click.command()
@click.argument('filename', default='output.mp4')
@click.option('-d', '--chunk-duration', default=10, type=int, help='Recording duration in seconds')
@click.option('-k', '--api-key', envvar='ASSEMBLYAI_API_KEY', required=True, help='AssemblyAI API key')
@click.option('-o', '--output-dir', default='transcripts', help='Output directory for generated files')
@click.option('-w', '--whisper', is_flag=True, help='Use Whisper to transcribe rather than AssemblyAI')
@click.option('-m', '--model', default='base', 
              help='Whisper model name (base, small, medium, large)')
@click.option('-i', '--input', type=click.Choice(['mic', 'file']), default='mic')
@click.option('--phrase', type=click.Choice(PHRASES), default='eureka')
def transcribe(filename: str, chunk_duration: int, api_key: str, output_dir: str, whisper: bool, model: str, input: str, phrase: str):
    """Transcribe audio file using FFmpeg and AssemblyAI API."""

    os.makedirs(output_dir, exist_ok=True)

    if whisper:
        from whisper import Whisper
        # ~/opt/whisper has the models
        whisper = Whisper(model=model)
        transcriber = whisper.transcribe
        click.echo(f"Using Whisper model {model}")
        # audio = ... # load audio

        # p = subprocess.run(['~/opt/whisper.cpp', '--audio=-'], input=audio, capture_output=True)
        # transcript = p.stdout.decode('utf-8')
        # click.echo(transcript)
    else:
        assemblyai.api_key = api_key
        transcriber = assemblyai.Transcriber()
        click.echo("Using AssemblyAI")

    uri = filename # Use filename provided as argument

    if input == 'file':
        transcriber.transcribe(uri)
        return
    
    while True:
        # Show when we're recording
        click.echo()
        click.echo(f"Recording for {chunk_duration} seconds starting at {time.strftime('%H:%M:%S')}")
        click.echo()
        uri = os.path.join(output_dir, f"{int(time.time())}-{filename}")
        # uri = filename
        
        stream = ffmpeg.input(':0', f='avfoundation', ac=2, t=chunk_duration) # type: ffmpeg.nodes.Stream
        stream = ffmpeg.output(stream, uri)
        ffmpeg.run(stream)

        # Emphasize this in the console
        start_time = time.strftime('%H:%M:%S')
        
        click.echo(f"Transcribing {uri} at {start_time}...")
        transcript = transcriber.transcribe(uri)
        click.echo(f"Transcription complete at {time.strftime('%H:%M:%S')}")
        
        transcript_text = transcript.text
        if not transcript_text:
            click.echo("No transcript generated")
            continue

        click.echo("Transcript:")
        click.echo(transcript_text)    

        transcript_file = os.path.join(output_dir, f"{int(time.time())}.txt")
        
        click.echo(f"Writing transcript to {transcript_file}")
        with open(transcript_file, 'w') as f:
            f.write(transcript.text)


if __name__ == '__main__':
    transcribe()
