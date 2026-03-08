import hashlib
import os
import subprocess

from pydub import AudioSegment


def speak(text: str, voice: str | None, cache_dir: str) -> AudioSegment:
    key = hashlib.sha256(f"{text}{voice or ''}".encode()).hexdigest()[:16]
    cache_path = os.path.join(cache_dir, f"{key}.aiff")

    if not os.path.exists(cache_path):
        cmd = ["say"]
        if voice:
            cmd += ["-v", voice]
        cmd += ["-o", cache_path, text]
        subprocess.run(cmd, check=True)

    return AudioSegment.from_file(cache_path, format="aiff")
