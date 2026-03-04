import whisper
import os
import sys
import time
from pathlib import Path

# ─────────────────────────────────────────────
#  Ensure FFmpeg is findable by Whisper
#  (handles cases where it's not on system PATH)
# ─────────────────────────────────────────────
_FFMPEG_DIR = r"C:\Users\joyas\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
if os.path.isdir(_FFMPEG_DIR) and _FFMPEG_DIR not in os.environ.get("PATH", ""):
    os.environ["PATH"] = _FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")

# ─────────────────────────────────────────────
#  Supported audio formats
# ─────────────────────────────────────────────
SUPPORTED_FORMATS = {".mp3", ".wav", ".ogg", ".mp4", ".m4a", ".flac", ".opus", ".webm", ".aac", ".mpeg", ".mpg"}


def load_model(model_size: str = "base"):
    """
    Load a Whisper model.
    Available sizes: tiny, base, small, medium, large
      - tiny   → fastest, least accurate (~1 GB RAM)
      - base   → good balance for most cases (~1 GB RAM)  ← DEFAULT
      - small  → better accuracy (~2 GB RAM)
      - medium → even better (~5 GB RAM)
      - large  → best accuracy (~10 GB RAM)
    """
    print(f"[INFO] Loading Whisper model: '{model_size}' ...")
    model = whisper.load_model(model_size)
    print(f"[INFO] Model '{model_size}' loaded successfully.\n")
    return model


def transcribe_audio(file_path: str, model, language: str = "en") -> dict:
    """
    Transcribe an audio file to English text.

    Args:
        file_path : Path to the audio file.
        model     : Loaded Whisper model.
        language  : Source language hint (default 'en').
                    Set to None to let Whisper auto-detect the language.

    Returns:
        dict with keys:
            - 'text'     : Full transcribed text
            - 'language' : Detected language
            - 'segments' : List of timed segments (for subtitles)
    """
    path = Path(file_path)

    # ── Validate file ──────────────────────────────────────────────────────
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{path.suffix}'. "
            f"Supported: {', '.join(SUPPORTED_FORMATS)}"
        )

    print(f"[INFO] Transcribing: {path.name}")
    start = time.time()

    # ── Transcribe ─────────────────────────────────────────────────────────
    result = model.transcribe(
        str(path),
        language=language,      # set to None for auto-detect
        task="transcribe",      # "transcribe" keeps original lang; "translate" → English
        verbose=False,
    )

    elapsed = time.time() - start
    print(f"[INFO] Done in {elapsed:.1f}s  |  Detected language: {result['language']}\n")

    return result


def save_transcript(result: dict, output_path: str):
    """Save plain-text transcript to a .txt file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"].strip())
    print(f"[SAVED] Transcript -> {output_path}")


def save_srt(result: dict, output_path: str):
    """
    Save an SRT subtitle file from Whisper segments.
    Compatible with YouTube, VLC, and most video players.
    """
    def format_time(seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"], start=1):
            f.write(f"{i}\n")
            f.write(f"{format_time(seg['start'])} --> {format_time(seg['end'])}\n")
            f.write(f"{seg['text'].strip()}\n\n")

    print(f"[SAVED] SRT subtitles -> {output_path}")


def transcribe_file(audio_path: str, model_size: str = "base", save_txt: bool = True, save_srt_file: bool = True):
    """
    Full pipeline: load model → transcribe → save outputs.

    Args:
        audio_path   : Path to the audio file.
        model_size   : Whisper model size ('tiny','base','small','medium','large').
        save_txt     : Whether to save a .txt transcript.
        save_srt_file: Whether to save an .srt subtitle file.

    Returns:
        Transcribed text (str)
    """
    # Load model
    model = load_model(model_size)

    # Transcribe
    result = transcribe_audio(audio_path, model)

    # Determine output base name
    base = str(Path(audio_path).with_suffix(""))

    # Save outputs
    if save_txt:
        save_transcript(result, base + "_transcript.txt")

    if save_srt_file:
        save_srt(result, base + "_subtitles.srt")

    # Print to console
    print("-" * 60)
    print("TRANSCRIPTION RESULT:")
    print("-" * 60)
    print(result["text"].strip())
    print("-" * 60)

    return result["text"].strip()


# ─────────────────────────────────────────────────────────────────
#  Run from command line:
#    python audio_to_text.py <audio_file> [model_size]
#
#  Examples:
#    python audio_to_text.py voice_note.ogg
#    python audio_to_text.py lecture.mp3 small
#    python audio_to_text.py interview.wav medium
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audio_to_text.py <audio_file> [model_size]")
        print("       model_size options: tiny | base | small | medium | large")
        print("       (default: base)")
        sys.exit(1)

    audio_file = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"

    transcribe_file(audio_file, model_size=model_size)
