import os
import assemblyai as aai
import click

@click.command()
def transcribe():
    """Transcribe an audio file using AssemblyAI API."""
    api_key = os.environ['ASSEMBLYAI_API_KEY']
    
    aai.settings.api_key = api_key # type: str

    file_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3" # type: str

    transcriber = aai.Transcriber() # type: aai.Transcriber
    
    transcript = transcriber.transcribe(file_url) # type: aai.Transcript

    print(transcript.text) # type: str

if __name__ == '__main__':
    transcribe()
