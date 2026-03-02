import gc
import io
import base64
import tempfile
import threading
import os
import torch
import soundfile as sf

class TTSEngine:
    def __init__(self):
        self._lock = threading.Lock()
        self._model = None
        self._Qwen3TTSModel = None

    def _ensure_imports(self):
        if self._Qwen3TTSModel is None:
            from qwen_tts import Qwen3TTSModel
            self._Qwen3TTSModel = Qwen3TTSModel

    def _load_model(self, model_id: str):
        self._ensure_imports()
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self._model = self._Qwen3TTSModel.from_pretrained(
            model_id, 
            device_map=device, 
            dtype=torch.bfloat16, 
            attn_implementation="eager"
        )

    def _unload_model(self):
        if self._model is not None:
            del self._model
            self._model = None
        gc.collect()
        if torch.cuda.is_available(): 
            torch.cuda.empty_cache()

    def generate(self, model_id: str, mode: str, text: str, language: str = "Auto", speaker: str = None, instruct: str = None, ref_audio_base64: str = None, ref_text: str = None):
        self._ensure_imports()
        with self._lock:
            try:
                self._load_model(model_id)
                if mode == "custom_voice":
                    k = {"text":text, "language":language, "speaker":speaker}
                    if instruct: k["instruct"] = instruct
                    wavs, sr = self._model.generate_custom_voice(**k)
                elif mode == "voice_clone":
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                        tmp.write(base64.b64decode(ref_audio_base64))
                        tmp_path = tmp.name
                    k = {"text":text, "language":language, "ref_audio":tmp_path}
                    if ref_text: k["ref_text"] = ref_text
                    else: k["x_vector_only_mode"] = True
                    wavs, sr = self._model.generate_voice_clone(**k)
                    os.unlink(tmp_path)
                elif mode == "voice_design":
                    wavs, sr = self._model.generate_voice_design(text=text, language=language, instruct=instruct)
                
                buffer = io.BytesIO()
                sf.write(buffer, wavs[0], sr, format="WAV")
                buffer.seek(0)
                audio_b64 = base64.b64encode(buffer.read()).decode("utf-8")
                dur = len(wavs[0]) / sr
                
                return audio_b64, sr, dur
            except Exception as e:
                raise Exception(f"TTS generation failed: {str(e)}")
            finally:
                self._unload_model()

engine = TTSEngine()
