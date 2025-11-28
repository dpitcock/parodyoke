import os
import yt_dlp
import re
from typing import List, Tuple, Optional

def download_video(url: str, output_dir: str = "temp") -> Tuple[Optional[str], Optional[str]]:
    """
    Downloads video and subtitles from YouTube.
    Returns a tuple of (video_path, subtitle_path).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'srt',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_title = info.get('title', 'video')
        video_ext = info.get('ext', 'mp4')
        
        # Construct expected filenames
        # yt-dlp sanitizes filenames, so we might need to find the file
        # This is a simplification; robust implementation would check the actual output filename
        filename = ydl.prepare_filename(info)
        
        # Subtitle filename usually appends .en.srt
        subtitle_path = filename.rsplit('.', 1)[0] + '.en.srt'
        
        if not os.path.exists(subtitle_path):
             # Try checking for other subtitle formats or langs if 'en' failed specifically
             # For now, return None if not found
             subtitle_path = None

        return filename, subtitle_path

def parse_srt(srt_path: str) -> List[Tuple[float, float, str]]:
    """
    Parses an SRT file into a list of (start_time, end_time, text).
    Time is in seconds.
    """
    if not srt_path or not os.path.exists(srt_path):
        return []

    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match SRT blocks
    # Index
    # Start --> End
    # Text
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n((?:(?!\n\n).)*)', re.DOTALL)
    
    matches = pattern.findall(content)
    parsed_subs = []

    for _, start_str, end_str, text in matches:
        start = _time_to_seconds(start_str)
        end = _time_to_seconds(end_str)
        clean_text = text.strip().replace('\n', ' ')
        parsed_subs.append((start, end, clean_text))

    return parsed_subs

def _time_to_seconds(time_str: str) -> float:
    """Converts HH:MM:SS,mmm to seconds."""
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split(',')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000.0
