import pysrt
from config import OUTPUT_SUBS

def generate_subtitles(english_text):
    subs = pysrt.SubRipFile()
    lines = english_text.split(".")

    start = 0
    for i, line in enumerate(lines):
        if line.strip():
            subs.append(
                pysrt.SubRipItem(
                    index=i + 1,
                    start=pysrt.SubRipTime(seconds=start),
                    end=pysrt.SubRipTime(seconds=start + 3),
                    text=line.strip()
                )
            )
            start += 3

    subs.save(OUTPUT_SUBS)
