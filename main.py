import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import os

# ================= OPTIONAL (PORTABLE EXE SUPPORT) =================
# Uncomment ONLY if you want exe to load key from /keys folder
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
#     os.path.dirname(__file__), "keys", "vertex-voice-key.json"
# )
# ==================================================================

from utils import normalize_hinglish
from ssml_builder import build_ssml
from voice_generator import generate_voice
from translator import translate_to_english
from subtitle_generator import generate_subtitles

# ---------------- UI CONFIG ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- APP ----------------
app = ctk.CTk()
app.title("Hindi AI Voice Generator")
app.geometry("640x680")
app.resizable(False, False)

output_dir = "output"

# ---------------- FUNCTIONS ----------------
def toggle_theme():
    mode = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if mode == "Dark" else "dark")

def choose_output_folder():
    global output_dir
    folder = filedialog.askdirectory()
    if folder:
        output_dir = folder
        status_label.configure(text=f"Output: {output_dir}")

def apply_preset(preset):
    if preset == "mystery":
        emotion_var.set("mysterious")
        pause_var.set("long")
        speed_slider.set(0.9)
    elif preset == "history":
        emotion_var.set("calm")
        pause_var.set("medium")
        speed_slider.set(1.0)
    elif preset == "motivation":
        emotion_var.set("intense")
        pause_var.set("long")
        speed_slider.set(0.85)

def generate_thread():
    try:
        progress.start()
        status_label.configure(text="Generating voice...")

        script = text_box.get("1.0", "end").strip()
        if not script:
            raise ValueError("Please enter a script.")

        script = normalize_hinglish(script)

        ssml = build_ssml(
            script,
            emotion_var.get(),
            pause_var.get(),
            speed_slider.get()
        )

        generate_voice(ssml)

        status_label.configure(text="Generating subtitles...")
        english_text = translate_to_english(script)
        generate_subtitles(english_text)

        progress.stop()
        status_label.configure(text="Done ✔ Files saved in output folder")

        messagebox.showinfo("Success", "Voice and subtitles generated successfully!")

    except Exception as e:
        progress.stop()
        status_label.configure(text="Error ❌")
        messagebox.showerror("Error", str(e))

def generate_all():
    threading.Thread(target=generate_thread, daemon=True).start()

# ---------------- HEADER ----------------
title = ctk.CTkLabel(app, text="🎙 Hindi AI Voice Generator", font=("Segoe UI", 22, "bold"))
title.pack(pady=10)

subtitle = ctk.CTkLabel(
    app,
    text="Male Hindi Voice • Emotion • Presets • Subtitles",
    font=("Segoe UI", 13)
)
subtitle.pack()

# ---------------- SCRIPT ----------------
ctk.CTkLabel(app, text="Script (Hindi / Hinglish)", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=25)

text_box = ctk.CTkTextbox(app, height=160, font=("Segoe UI", 13))
text_box.pack(padx=25, pady=(5, 15), fill="x")

# ---------------- PRESETS ----------------
preset_frame = ctk.CTkFrame(app)
preset_frame.pack(padx=25, pady=10, fill="x")

ctk.CTkLabel(preset_frame, text="Presets", font=("Segoe UI", 14, "bold")).pack(side="left", padx=10)

ctk.CTkButton(preset_frame, text="Mystery", command=lambda: apply_preset("mystery")).pack(side="left", padx=5)
ctk.CTkButton(preset_frame, text="History", command=lambda: apply_preset("history")).pack(side="left", padx=5)
ctk.CTkButton(preset_frame, text="Motivation", command=lambda: apply_preset("motivation")).pack(side="left", padx=5)

# ---------------- CONTROLS ----------------
controls = ctk.CTkFrame(app)
controls.pack(padx=25, pady=10, fill="x")

emotion_var = ctk.StringVar(value="calm")
pause_var = ctk.StringVar(value="medium")

ctk.CTkLabel(controls, text="Emotion").grid(row=0, column=0, padx=15, pady=15)
ctk.CTkOptionMenu(controls, variable=emotion_var,
                  values=["calm", "intense", "mysterious", "sad"]).grid(row=0, column=1)

ctk.CTkLabel(controls, text="Pause").grid(row=0, column=2, padx=15)
ctk.CTkOptionMenu(controls, variable=pause_var,
                  values=["short", "medium", "long"]).grid(row=0, column=3)

# ---------------- SPEED ----------------
ctk.CTkLabel(app, text="Speech Speed", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=25)

speed_slider = ctk.CTkSlider(app, from_=0.7, to=1.3)
speed_slider.set(1.0)
speed_slider.pack(padx=25, pady=(5, 15), fill="x")

# ---------------- ACTIONS ----------------
actions = ctk.CTkFrame(app)
actions.pack(padx=25, pady=10, fill="x")

ctk.CTkButton(actions, text="Choose Output Folder", command=choose_output_folder).pack(side="left", padx=10)
ctk.CTkButton(actions, text="Toggle Theme", command=toggle_theme).pack(side="right", padx=10)

# ---------------- PROGRESS ----------------
progress = ctk.CTkProgressBar(app, mode="indeterminate")
progress.pack(padx=25, pady=(20, 5), fill="x")

status_label = ctk.CTkLabel(app, text="Ready", font=("Segoe UI", 12))
status_label.pack()

# ---------------- GENERATE ----------------
generate_btn = ctk.CTkButton(
    app,
    text="Generate Voice",
    height=50,
    font=("Segoe UI", 16, "bold"),
    command=generate_all
)
generate_btn.pack(pady=25)

# ---------------- FOOTER ----------------
footer = ctk.CTkLabel(app, text="Powered by Google Vertex AI", font=("Segoe UI", 11))
footer.pack(pady=(0, 10))

# ---------------- RUN ----------------
app.mainloop()
