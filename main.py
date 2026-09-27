#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""بیان — اپ موبایل با Kivy و edge-tts"""

import asyncio
import threading
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

try:
    import edge_tts
except ImportError:
    edge_tts = None

VOICES = {
    "زن": "fa-IR-DilaraNeural",
    "مرد": "fa-IR-FaridNeural",
    "کودک": "fa-IR-DilaraNeural",
}

TONES = {
    "خبری": {"pitch": -10, "rate": 0, "volume": 0},
    "شاد": {"pitch": 30, "rate": 35, "volume": 10},
    "غمگین": {"pitch": -45, "rate": -40, "volume": -30},
    "هیجان‌زده": {"pitch": 45, "rate": 45, "volume": 15},
    "آرام": {"pitch": -8, "rate": -45, "volume": -35},
    "جدی": {"pitch": -35, "rate": -25, "volume": -10},
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
        if edge_tts is None:
            self.status.text = "edge-tts نصب نیست"
            return
        text = self.text_input.text.strip()
        if not text:
            self.status.text = "متنی بنویس"
            return
        voice = VOICES.get(self.voice_spinner.text, "fa-IR-DilaraNeural")
        tone = TONES.get(self.tone_spinner.text, TONES["خبری"])
        self.status.text = "در حال ساخت صدا..."
        threading.Thread(target=self._synth_thread,
                         args=(text, voice, tone), daemon=True).start()

    def _synth_thread(self, text, voice, tone):
        try:
            out = Path("/sdcard/Download/bayan_output.mp3")
            out.parent.mkdir(parents=True, exist_ok=True)
            asyncio.run(self._synth_async(text, voice, tone, out))
            Clock.schedule_once(lambda dt: self._on_done(out), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_error(str(e)), 0)

    async def _synth_async(self, text, voice, tone, out_path):
        communicate = edge_tts.Communicate(
            text, voice,
            rate=f"{tone['rate']:+d}%",
            pitch=f"{tone['pitch']:+d}Hz",
            volume=f"{tone['volume']:+d}%")
        await communicate.save(str(out_path))

    def _on_done(self, path):
        self.status.text = f"ذخیره شد: {path}"
        sound = SoundLoader.load(str(path))
        if sound:
            sound.play()

    def _on_error(self, msg):
        self.status.text = f"خطا: {msg}"


if __name__ == "__main__":
    BayanApp().run()
