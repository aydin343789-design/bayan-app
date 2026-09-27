#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""بیان — نسخه ساده با Kivy"""

import threading
import requests
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

VOICES = {
    "زن": "fa-IR-DilaraNeural",
    "مرد": "fa-IR-FaridNeural",
}

TONES = {
    "خبری": (0, -10, 0),
    "شاد": (35, 30, 10),
    "غمگین": (-40, -45, -30),
    "آرام": (-45, -8, -35),
}


class BayanApp(App):
    def build(self):
        self.title = "بیان"
        layout = BoxLayout(orientation="vertical", padding=20, spacing=12)

        layout.add_widget(Label(text="بیان استودیو", font_size=28,
                                size_hint_y=None, height=50))

        self.voice_spinner = Spinner(text="زن", values=list(VOICES.keys()),
                                     size_hint_y=None, height=50)
        layout.add_widget(self.voice_spinner)

        self.tone_spinner = Spinner(text="خبری", values=list(TONES.keys()),
                                    size_hint_y=None, height=50)
        layout.add_widget(self.tone_spinner)

        self.text_input = TextInput(
            text="سلام. به استودیوی بیان خوش آمدید.",
            multiline=True, size_hint_y=0.4)
        layout.add_widget(self.text_input)

        self.status = Label(text="آماده", size_hint_y=None, height=40)
        layout.add_widget(self.status)

        btn = Button(text="بخوان و ذخیره", size_hint_y=None, height=60,
                     background_color=(0.88, 0.63, 0.23, 1))
        btn.bind(on_press=self.on_speak)
        layout.add_widget(btn)

        return layout

    def on_speak(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self.status.text = "متنی بنویس"
            return
        self.status.text = "در حال ساخت صدا..."
        threading.Thread(target=self._synth_thread,
                         args=(text,), daemon=True).start()

    def _synth_thread(self, text):
        try:
            out = Path("/sdcard/Download/bayan_output.mp3")
            out.parent.mkdir(parents=True, exist_ok=True)

            voice_name = VOICES.get(self.voice_spinner.text, "fa-IR-DilaraNeural")
            tone = TONES.get(self.tone_spinner.text, TONES["خبری"])

            url = "https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Origin": "chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold",
            }

            # روش ساده: از edge-tts web api استفاده کن
            # یا از یک سرویس جایگزین
            raise RuntimeError("در نسخه بعدی پیاده‌سازی می‌شود")

        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_error(str(e)), 0)

    def _on_error(self, msg):
        self.status.text = f"خطا: {msg}"


if __name__ == "__main__":
    BayanApp().run()
