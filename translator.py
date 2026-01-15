from google.cloud import translate_v2 as translate

def translate_to_english(text):
    client = translate.Client()
    result = client.translate(text, target_language="en")
    return result["translatedText"]
