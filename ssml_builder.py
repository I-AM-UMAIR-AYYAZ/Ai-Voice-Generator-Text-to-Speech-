def build_ssml(text, emotion, pause, speed):
    # Pure, default Google voice
    return f"""
<speak>
    {text}
</speak>
"""
