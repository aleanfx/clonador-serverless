from dataclasses import dataclass, field
from typing import Dict, List

MODEL_REGISTRY: Dict[str, Dict[str, str]] = {
    "fast": {
        "custom_voice": "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        "voice_clone":  "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
    },
    "quality": {
        "custom_voice":  "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
        "voice_clone":   "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        "voice_design":  "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    },
}

SUPPORTED_QUALITIES = ["fast", "quality"]
SUPPORTED_MODES = ["custom_voice", "voice_clone", "voice_design"]

def get_model_id(quality: str, mode: str) -> str:
    quality = quality.lower() if quality else "fast"
    mode = mode.lower() if mode else "custom_voice"
    if quality not in SUPPORTED_QUALITIES: quality = "fast"
    if mode not in SUPPORTED_MODES: mode = "custom_voice"
    # voice_design is only available in quality mode
    if mode == "voice_design" and quality == "fast":
        quality = "quality"
    return MODEL_REGISTRY[quality][mode]
