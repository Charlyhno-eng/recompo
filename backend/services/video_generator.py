from typing import BinaryIO
import io
import zipfile
import os
import tempfile
from fastapi import UploadFile, HTTPException
from .ffmpeg_utils import (
    get_duration,
    extract_audio_segment,
    loop_video_to_duration,
    trim_video,
    mux_audio_video,
    burn_subtitles,
)
from .subtitles import generate_english_srt
import logging

logger = logging.getLogger("subtitle_video_app")

async def generate_segments_zip(
    audio: UploadFile,
    video: UploadFile,
    parts: int,
) -> BinaryIO:
    if parts < 2 or parts > 30:
        raise HTTPException(status_code=400, detail="parts must be between 2 and 30")

    zip_buffer = io.BytesIO()

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, audio.filename or "audio.mp3")
        video_path = os.path.join(tmpdir, video.filename or "video.mp4")

        logger.info("Saving uploaded files to temp dir: %s", tmpdir)
        with open(audio_path, "wb") as f:
            f.write(await audio.read())
        with open(video_path, "wb") as f:
            f.write(await video.read())

        try:
            total_duration = get_duration(audio_path)
            logger.info("Audio duration: %.3f s", total_duration)
        except Exception as e:
            logger.exception("Failed to probe audio duration")
            raise HTTPException(status_code=400, detail="Invalid audio file") from e

        if total_duration <= 0:
            logger.error("Audio has invalid duration: %.3f", total_duration)
            raise HTTPException(status_code=400, detail="Audio has invalid duration")

        try:
            video_duration = get_duration(video_path)
            logger.info("Video duration: %.3f s", video_duration)
        except Exception as e:
            logger.exception("Failed to probe video duration")
            raise HTTPException(status_code=400, detail="Invalid video file") from e

        if video_duration <= 0:
            logger.error("Video has invalid duration: %.3f", video_duration)
            raise HTTPException(status_code=400, detail="Video has invalid duration")

        segment_duration = total_duration / parts
        logger.info("Segment duration: %.3f s", segment_duration)

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i in range(parts):
                start = segment_duration * i
                end = min(segment_duration * (i + 1), total_duration)
                seg_dur = end - start

                if seg_dur <= 0:
                    logger.warning(
                        "Skipping empty segment %s (start=%.3f, end=%.3f)",
                        i + 1,
                        start,
                        end,
                    )
                    continue

                logger.info(
                    "Processing segment %s/%s: start=%.3f, end=%.3f, dur=%.3f",
                    i + 1,
                    parts,
                    start,
                    end,
                    seg_dur,
                )

                segment_audio_path = os.path.join(tmpdir, f"audio_{i+1:02d}.mp3")
                extract_audio_segment(
                    input_audio=audio_path,
                    output_audio=segment_audio_path,
                    start=start,
                    duration=seg_dur,
                )
                logger.info("Audio segment written: %s", segment_audio_path)

                looped_video_path = os.path.join(tmpdir, f"video_loop_{i+1:02d}.mp4")
                loop_video_to_duration(
                    input_video=video_path,
                    output_video=looped_video_path,
                    target_duration=seg_dur,
                    video_duration=video_duration,
                )
                logger.info("Looped video written: %s", looped_video_path)

                trimmed_video_path = os.path.join(tmpdir, f"video_trim_{i+1:02d}.mp4")
                trim_video(
                    input_video=looped_video_path,
                    output_video=trimmed_video_path,
                    duration=seg_dur,
                )
                logger.info("Trimmed video written: %s", trimmed_video_path)

                # Mux audio + vidéo
                base_output_path = os.path.join(tmpdir, f"segment_{i+1:02d}_nosubs.mp4")
                logger.info("Muxing segment %s -> %s", i + 1, base_output_path)
                mux_audio_video(
                    input_video=trimmed_video_path,
                    input_audio=segment_audio_path,
                    output_path=base_output_path,
                )
                logger.info("Muxed segment ready: %s", base_output_path)

                srt_path = os.path.join(tmpdir, f"segment_{i+1:02d}.srt")
                logger.info("Generating English subtitles for segment %s", i + 1)
                generate_english_srt(
                    audio_path=segment_audio_path,
                    srt_path=srt_path,
                )
                logger.info("SRT ready: %s", srt_path)

                final_output_path = os.path.join(tmpdir, f"segment_{i+1:02d}.mp4")
                logger.info("Burning subtitles into video: %s -> %s", base_output_path, final_output_path)
                burn_subtitles(
                    input_video=base_output_path,
                    srt_path=srt_path,
                    output_path=final_output_path,
                )
                logger.info("Final subtitled segment ready: %s", final_output_path)

                with open(final_output_path, "rb") as f:
                    zip_file.writestr(f"segment_{i+1:02d}.mp4", f.read())

        logger.info("All segments packed into zip")

    zip_buffer.seek(0)
    return zip_buffer
