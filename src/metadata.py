import re

def clean_youtube_title(title: str) -> str:
    """
    Removes common YouTube 'junk' from video titles.
    """
    # Remove parentheticals/brackets containing specific keywords
    keywords = [
        "official", "video", "audio", "music", "lyrics", "lyric", 
        "hq", "hd", "4k", "karaoke", "instrumental", "remastered", "cover"
    ]
    
    # Regex to find (...) or [...]
    # We'll iterate and check content
    clean_title = title
    
    # Remove specific fixed strings first if needed, but the general approach below covers most.
    # Let's try a regex that matches (...) or [...] and checks if it contains any keyword.
    
    # Simple approach: remove any (...) or [...] that contains a keyword
    def keyword_replacer(match):
        content = match.group(1) or match.group(2)
        if any(k in content.lower() for k in keywords):
            return ""
        return match.group(0) # Keep it if no keyword
        
    clean_title = re.sub(r'\((.*?)\)|\[(.*?)\]', keyword_replacer, clean_title)
    
    # Also remove "ft." or "feat." and everything after? Or just keep it as part of title?
    # User said "strip YouTube junk". Usually ft. is part of the artist/title info.
    # Let's just clean up extra spaces.
    
    clean_title = re.sub(r"\s+", " ", clean_title).strip()
    
    # Remove trailing/leading punctuation
    clean_title = clean_title.strip(" -_[]()")
    
    return clean_title.title() # Convert back to Title Case

def parse_artist_title(title: str) -> tuple[str, str]:
    """
    Attempts to parse Artist and Title from a string.
    Returns (artist, title). Defaults to ('Unknown Artist', title) if split fails.
    """
    # Common separators: " - ", " – ", " : ", " by "
    separators = [" - ", " – ", " : "]
    
    for sep in separators:
        if sep in title:
            parts = title.split(sep, 1)
            return parts[0].strip(), parts[1].strip()
            
    if " by " in title:
        parts = title.split(" by ", 1)
        # "Title by Artist" -> Artist, Title
        return parts[1].strip(), parts[0].strip()
            
    # If no separator found, assume the whole thing is the title, or try to guess
    return "Unknown Artist", title.strip()

def format_output_filename(author: str, parody_title: str, orig_artist: str, orig_title: str) -> str:
    """
    Formats the final filename according to the pattern:
    {{author}} - {{parody-title}} of {{orig_artist}} - {{orig-title}}
    """
    # Sanitize for filesystem
    def sanitize(s):
        return re.sub(r'[<>:"/\\|?*]', '', s).strip()

    return f"{sanitize(author)} - {sanitize(parody_title)} of {sanitize(orig_artist)} - {sanitize(orig_title)}.mp4"
