import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os

# Initialize speech recognition and translator
rec = sr.Recognizer()
translator = Translator()

# Initialize pygame for audio playback
pygame.mixer.init()

# Create a list of supported languages
supported_languages = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'rw', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']

# Create the main Tkinter window
window = tk.Tk()
window.title("Speech Translator")
window.geometry("400x200")

# Language selection
input_language_label = tk.Label(window, text="Select Input Language:")
input_language_label.pack()

input_language_var = tk.StringVar()
input_language_var.set("en")  # Set a default language
input_language_menu = ttk.Combobox(window, textvariable=input_language_var, values=supported_languages)
input_language_menu.pack()

output_language_label = tk.Label(window, text="Select Output Language:")
output_language_label.pack()

output_language_var = tk.StringVar()
output_language_var.set("en")  # Set a default language
output_language_menu = ttk.Combobox(window, textvariable=output_language_var, values=supported_languages)
output_language_menu.pack()

# Start/Stop button
is_recording = False
update_button = tk.Button(window, text="Start Recording", command=lambda: toggle_recording())
update_button.pack()

# Function to start and stop recording
def toggle_recording():
    global is_recording
    if not is_recording:
        is_recording = True
        update_button.config(text="Stop Recording")
        start_recording()
    else:
        is_recording = False
        update_button.config(text="Start Recording")

# Function to handle speech recognition
def start_recording():
    with sr.Microphone() as source:
        print("Speak something...")
        audio = rec.listen(source)

    try:
        recognized_text = rec.recognize_google(audio, language=input_language_var.get())
        translated_text = translate_text(recognized_text)
        play_translated_audio(translated_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Function to translate text
def translate_text(text):
    translated = translator.translate(text, src=input_language_var.get(), dest=output_language_var.get())
    return translated.text

# Function to play the translated audio
def play_translated_audio(text):
    tts = gTTS(text, lang=output_language_var.get())
    tts.save("translated.mp3")
    pygame.mixer.music.load("translated.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set an event when playback ends

# Function to delete the audio file after playback
def delete_audio_file():
    os.remove("translated.mp3")

# Bind the delete_audio_file function to the playback end event
window.bind(pygame.USEREVENT, lambda: delete_audio_file())

window.mainloop()
