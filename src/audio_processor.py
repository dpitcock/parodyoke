import os
import subprocess
from moviepy import VideoFileClip

def extract_audio(video_path: str, output_audio_path: str = None) -> str:
    """
    Extracts audio from a video file.
    If output_audio_path is not provided, it defaults to the video filename with .mp3 extension.
    Returns the path to the extracted audio file.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if output_audio_path is None:
        base, _ = os.path.splitext(video_path)
        output_audio_path = f"{base}.mp3"

    # Use moviepy to extract audio
    # We could use ffmpeg directly for speed, but moviepy is already a dependency
    # and handles codecs well.
    with VideoFileClip(video_path) as video:
        video.audio.write_audiofile(output_audio_path, logger=None)
    
    return output_audio_path

def separate_vocals(audio_path: str, output_dir: str = "temp/separated") -> str:
    """
    Separates vocals from audio using Demucs.
    Returns the path to the instrumental track (no_vocals).
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Run Demucs via CLI
    # demucs -n htdemucs --two-stems=vocals -o <output_dir> <audio_path>
    # --two-stems=vocals forces generation of only 'vocals' and 'no_vocals' (instrumental)
    # -n htdemucs uses the high-quality Hybrid Transformer model (default in v4)
    
    cmd = [
        "demucs",
        "-n", "htdemucs",
        "--two-stems=vocals",
        "-o", output_dir,
        audio_path
    ]
    
    print(f"Running Demucs: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    # Construct expected output path
    # Demucs output structure: <output_dir>/htdemucs/<track_name>/no_vocals.wav
    track_name = os.path.splitext(os.path.basename(audio_path))[0]
    instrumental_path = os.path.join(output_dir, "htdemucs", track_name, "no_vocals.wav")
    
    if not os.path.exists(instrumental_path):
        raise RuntimeError(f"Demucs failed to produce output at {instrumental_path}")
        
    return instrumental_path
