# recording.py

from dataclasses import dataclass
from typing import BinaryIO

@dataclass
class Recording:

  file: BinaryIO
  duration: float
  source: str
  date: str
  
  def transcribe(self) -> str:
    return "Transcribed text"
