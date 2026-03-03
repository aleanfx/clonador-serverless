import runpod
from config import get_model_id
from tts_engine import engine

def handler(event):
    input_data = event.get("input", {})
    if not input_data:
        return {"error": "No input provided"}

    text = input_data.get("text")
    if not text:
        return {"error": "Missing 'text' parameter"}

    language = input_data.get("language", "Auto")
    mode = input_data.get("mode", "custom_voice")
    quality = input_data.get("quality", "fast")
    speaker = input_data.get("speaker", "Vivian")
    instruct = input_data.get("instruct")
    ref_audio_base64 = input_data.get("ref_audio_base64")
    ref_text = input_data.get("ref_text")

    if mode == "voice_clone" and not ref_audio_base64:
        return {"error": "Missing 'ref_audio_base64' for voice_clone mode"}

    try:
        model_id = get_model_id(quality, mode)
        audio_b64, sr, dur = engine.generate(
            model_id=model_id,
            mode=mode,
            text=text,
            language=language,
            speaker=speaker,
            instruct=instruct,
            ref_audio_base64=ref_audio_base64,
            ref_text=ref_text
        )
        
        return {
            "success": True,
            "audio_base64": audio_b64,
            "sample_rate": sr,
            "duration_seconds": dur,
            "model_used": model_id
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
