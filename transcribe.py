import os
import time
import ffmpeg
import assemblyai
import click
import whisper
from dataclasses import dataclass
from typing import List, Dict
import subprocess
from pync import Notifier

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
    Notifier.notify(f'Action taken for "{transcript}"', title='Transcribe', sound='default')

def check_transcript(transcript, phrase):
    click.echo(f"Checking transcript for {phrase}")
    if phrase in transcript: 
        click.echo('\a') # Terminal bell
        take_action(transcript)

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
PHRASES_SCORED = [
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


PHRASES = [p.text for p in PHRASES_SCORED]

ACTIONS_MIDDLEWARE = []

@click.command()
@click.argument('filename', default='output.mp4')
@click.option('-d', '--chunk-duration', default=10, type=int, help='Recording duration in seconds')
@click.option('-k', '--api-key', envvar='ASSEMBLYAI_API_KEY', help='AssemblyAI API key')
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
        # Error if we're using AssemblyAI but don't have an API key
        if not api_key:
            raise click.UsageError("API key required for AssemblyAI")
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

        check_transcript(transcript_text, phrase)

if __name__ == '__main__':
    transcribe()
