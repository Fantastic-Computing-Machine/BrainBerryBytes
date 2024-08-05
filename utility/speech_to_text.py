import tempfile
from groq import Groq
import os

class SpeechToText:
    def __init__(self,api_key ):
        self.client = Groq(api_key=api_key)
        self.model="whisper-large-v3"
        self.prompt = ""
        self.response_format = "json"
        self.language = "en"
        self.temperature = 0.0

    def convert(self, audio_data):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file_path = temp_audio_file.name

        with open(temp_audio_file_path, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(temp_audio_file_path, file.read()),
                model=self.model,
                prompt=self.prompt,
                response_format=self.response_format,
                language=self.language,
                temperature=self.temperature
            )
        os.remove(temp_audio_file_path)
        
        return transcription.text