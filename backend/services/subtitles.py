from faster_whisper import WhisperModel
from typing import List, Tuple
import logging

logger = logging.getLogger("subtitle_video_app")

_model: WhisperModel | None = None

def get_model() -> WhisperModel:
    global _model
    if _model is None:
        logger.info("Loading Faster-Whisper model (medium)...")
        _model = WhisperModel(
            "medium",
            device="cpu",
            compute_type="int8"
        )
        logger.info("Faster-Whisper model loaded")
    return _model

def format_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h = ms // 3_600_000
    m = (ms % 3_600_000) // 60_000
    s = (ms % 60_000) // 1000
    ms = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def write_srt(segments: List[Tuple[int, float, float, str]], srt_path: str) -> None:
    lines: list[str] = []
    for idx, start, end, text in segments:
        lines.append(str(idx))
        lines.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
        lines.append(text.strip())
        lines.append("")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def generate_srt(
    audio_path: str,
    srt_path: str,
    language: str = "fr",
) -> None:
    model = get_model()
    logger.info("Transcribing audio for subtitles: %s (lang=%s)", audio_path, language)

    if language == "en":
        task = "translate"
        lang_arg = None
    else:
        task = "transcribe"
        lang_arg = None

    segments_iter, _info = model.transcribe(
        audio_path,
        task=task,
        language=lang_arg,
        beam_size=5,
        word_timestamps=False,
    )

    collected: List[Tuple[int, float, float, str]] = []
    idx = 1
    for segment in segments_iter:
        collected.append((idx, segment.start, segment.end, segment.text))
        idx += 1

    logger.info("Transcription produced %s segments", len(collected))
    write_srt(collected, srt_path)
    logger.info("SRT written: %s", srt_path)
