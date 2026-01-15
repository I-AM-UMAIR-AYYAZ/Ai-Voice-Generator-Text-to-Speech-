from google.cloud import texttospeech  # ✅ THIS LINE WAS MISSING
from config import *

def generate_voice(ssml_text):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(
        ssml=ssml_text
    )

    voice = texttospeech.VoiceSelectionParams(
        language_code=VOICE_LANGUAGE,
        name=VOICE_NAME,
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(OUTPUT_AUDIO, "wb") as out:
        out.write(response.audio_content)
