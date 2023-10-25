import os
import ffmpeg
import assemblyai 
import click

@click.command()
@click.option('-k', '--api-key', envvar='ASSEMBLYAI_API_KEY', required=True, help='AssemblyAI API key')
def transcribe(api_key):
    """Transcribe audio file using FFmpeg and AssemblyAI API."""

    assemblyai.api_key = api_key

    stream = ffmpeg.input(":0", f="avfoundation", ac=1, ar="24k")
    stream = ffmpeg.output(stream, "output.wav", ac=1, ar=24000)
    ffmpeg.run(stream)

    with open("output.wav", 'rb') as f:
        audio = f.read()

    transcript = assemblyai.transcript(audio)

    summary = assemblyai.summarize(transcript)
    print(summary)

if __name__ == '__main__':
    transcribe()
