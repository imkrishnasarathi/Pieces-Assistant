import tkinter as tk
import speech_recognition as sr
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pyttsx3

engine = pyttsx3.init()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pieces Assistant")
        self.root.geometry("600x400")

        self.style = ttk.Style()
        self.style.theme_use("cosmo")

        self.label = ttk.Label(root, text="Speak something...", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.button = ttk.Button(root, text="Start Listening", command=self.listen)
        self.button.pack(pady=10)

        self.output_label = ttk.Label(root, text="", font=("Helvetica", 14))
        self.output_label.pack(pady=20)

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.config(text="Listening...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                self.output_label.config(text=f"You said: {text}")
                self.speak(f"You said: {text}")
            except sr.UnknownValueError:
                self.output_label.config(text="Sorry, I didn't catch that.")
            except sr.RequestError:
                self.output_label.config(text="Sorry, there was an error with the speech service.")

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()