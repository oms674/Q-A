import openai
import io

class TranscriptionAgent:
    def __init__(self):
        self.client = openai.Client()  # Ensure this is correctly instantiated

    async def transcribe_audio(self, audio_data):
        try:
            # Using 'io.BytesIO' to handle the received audio data correctly
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"  # Required for OpenAI API format detection

            # Transcription API (Updated for `openai>=1.0.0`)
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",  # Whisper model for transcription
                file=audio_file,
                response_format="text"
            )
            return transcript.strip()

        except openai.APIError as e:
            return f"❌ Transcription API Error: {e}"
        except Exception as e:
            return f"❌ Transcription Error: {e}"
