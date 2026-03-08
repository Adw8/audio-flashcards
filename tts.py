import hashlib
import os
import urllib.request
import wave
from pathlib import Path

import numpy as np
from piper.voice import PiperVoice
from pydub import AudioSegment

VOICES_DIR = "./voices"
DEFAULT_VOICE = "en_US-lessac-medium"
_HF_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0"

_loaded: dict[str, PiperVoice] = {}


def _normalize_voice_name(voice_name: str) -> str:
    """Normalise locale country code to uppercase: en_gb-... → en_GB-..."""
    parts = voice_name.split("-", 2)
    if len(parts) == 3:
        loc_parts = parts[0].split("_", 1)
        if len(loc_parts) == 2:
            parts[0] = f"{loc_parts[0]}_{loc_parts[1].upper()}"
    return "-".join(parts)


def _voice_url(voice_name: str, ext: str) -> str:
    # voice_name format: {locale}-{name}-{quality}  e.g. en_US-lessac-medium
    parts = voice_name.split("-", 2)
    locale, name, quality = parts[0], parts[1], parts[2]
    lang = locale.split("_")[0]
    return f"{_HF_BASE}/{lang}/{locale}/{name}/{quality}/{voice_name}.onnx{ext}"


def _ensure_voice(voice_name: str, voices_dir: str) -> Path:
    os.makedirs(voices_dir, exist_ok=True)
    onnx = Path(voices_dir) / f"{voice_name}.onnx"
    cfg = Path(voices_dir) / f"{voice_name}.onnx.json"
    for path, url in [(onnx, _voice_url(voice_name, "")), (cfg, _voice_url(voice_name, ".json"))]:
        if not path.exists():
            print(f"Downloading {path.name}...")
            urllib.request.urlretrieve(url, path)
    return onnx


def _get_voice(voice_name: str, voices_dir: str) -> PiperVoice:
    if voice_name not in _loaded:
        onnx_path = _ensure_voice(voice_name, voices_dir)
        _loaded[voice_name] = PiperVoice.load(str(onnx_path))
    return _loaded[voice_name]


def speak(text: str, voice: str | None, cache_dir: str) -> AudioSegment:
    voice_name = _normalize_voice_name(voice or DEFAULT_VOICE)
    key = hashlib.sha256(f"{text}{voice_name}".encode()).hexdigest()[:16]
    cache_path = os.path.join(cache_dir, f"{key}.wav")

    if not os.path.exists(cache_path):
        piper_voice = _get_voice(voice_name, VOICES_DIR)
        chunks = list(piper_voice.synthesize(text))
        audio = np.concatenate([c.audio_int16_array for c in chunks])
        sample_rate = chunks[0].sample_rate

        with wave.open(cache_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(audio.tobytes())

    return AudioSegment.from_file(cache_path, format="wav")
