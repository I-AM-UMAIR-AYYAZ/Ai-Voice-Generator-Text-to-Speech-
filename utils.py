def normalize_hinglish(text):
    replacements = {
        "hai": "है",
        "kya": "क्या",
        "kyun": "क्यों",
        "samajh": "समझ",
        "zindagi": "ज़िंदगी",
        "waqt": "वक़्त"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text
