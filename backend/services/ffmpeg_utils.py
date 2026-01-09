import subprocess
import ffmpeg
import math

def get_duration(path: str) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        path,
    ]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)

def extract_audio_segment(
    input_audio: str,
    output_audio: str,
    start: float,
    duration: float,
) -> None:
    (
        ffmpeg
        .input(input_audio, ss=start, t=duration)
        .output(output_audio, acodec="copy")
        .overwrite_output()
        .run(quiet=True)
    )

def loop_video_to_duration(
    input_video: str,
    output_video: str,
    target_duration: float,
    video_duration: float,
) -> None:
    loops = max(1, math.ceil(target_duration / video_duration))
    (
        ffmpeg
        .input(input_video, stream_loop=loops - 1)
        .output(output_video, vcodec="libx264", pix_fmt="yuv420p")
        .overwrite_output()
        .run(quiet=True)
    )

def trim_video(
    input_video: str,
    output_video: str,
    duration: float,
) -> None:
    (
        ffmpeg
        .input(input_video, ss=0, t=duration)
        .output(output_video, vcodec="libx264", pix_fmt="yuv420p")
        .overwrite_output()
        .run(quiet=True)
    )

def mux_audio_video(
    input_video: str,
    input_audio: str,
    output_path: str,
) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_video,
        "-i",
        input_audio,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        output_path,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def burn_subtitles(
    input_video: str,
    srt_path: str,
    output_path: str,
) -> None:
    subtitles_filter = f"subtitles={srt_path}"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_video,
        "-vf",
        subtitles_filter,
        "-c:v",
        "libx264",
        "-c:a",
        "copy",
        "-pix_fmt",
        "yuv420p",
        output_path,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
