import os
from typing import List, Tuple
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ColorClip

def render_video(
    original_video_path: str,
    instrumental_audio_path: str,
    lyrics_data: List[Tuple[float, float, str]],
    output_path: str,
    resolution: Tuple[int, int] = (1280, 720)
):
    """
    Renders the final parody video.
    
    Args:
        original_video_path: Path to the downloaded video.
        instrumental_audio_path: Path to the instrumental audio.
        lyrics_data: List of (start, end, text) tuples for the parody lyrics.
        output_path: Path to save the final MP4.
        resolution: Output video resolution (width, height).
    """
    
    # 1. Background
    # Create a black background
    background = ColorClip(size=resolution, color=(0, 0, 0), duration=10) # Duration placeholder, will be updated
    
    # 2. Original Video (PiP)
    # Load original video
    original_clip = VideoFileClip(original_video_path)
    
    # Resize and position in bottom right corner
    pip_width = int(resolution[0] * 0.3)
    pip_clip = original_clip.resized(width=pip_width)
    pip_clip = pip_clip.with_position(("right", "bottom")).with_margin(bottom=20, right=20, opacity=0)
    
    # 3. Audio
    # Load instrumental audio
    audio_clip = AudioFileClip(instrumental_audio_path)
    
    # Set duration based on audio
    final_duration = audio_clip.duration
    background = background.with_duration(final_duration)
    
    # Sync PiP duration (loop or cut?)
    # Usually original video matches audio length, but let's ensure it doesn't exceed
    if pip_clip.duration > final_duration:
        pip_clip = pip_clip.subclipped(0, final_duration)
    
    # 4. Lyrics Overlays
    txt_clips = []
    for start, end, text in lyrics_data:
        # Create TextClip
        # Note: TextClip requires ImageMagick. If not installed, this will fail.
        # We use a default font and white color.
        # stroke_color='black', stroke_width=2 for readability
        txt = (TextClip(text=text, font_size=50, color='white', font='Arial', stroke_color='black', stroke_width=2, size=(resolution[0]-100, None), method='caption')
               .with_position('center')
               .with_start(start)
               .with_end(end))
        txt_clips.append(txt)
        
    # 5. Composite
    final_video = CompositeVideoClip([background, pip_clip] + txt_clips)
    final_video = final_video.with_audio(audio_clip)
    
    # 6. Write File
    final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
