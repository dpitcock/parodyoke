import os
import lyricsgenius
import pyphen
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

def fetch_lyrics(song_title: str, artist_name: str) -> Optional[str]:
    """
    Fetches lyrics from Genius.
    Requires GENIUS_ACCESS_TOKEN env var.
    """
    token = os.getenv("GENIUS_ACCESS_TOKEN")
    if not token:
        print("Warning: GENIUS_ACCESS_TOKEN not found. Skipping lyrics fetch.")
        return None

    try:
        genius = lyricsgenius.Genius(token, verbose=False)
        song = genius.search_song(song_title, artist_name)
        if song:
            return song.lyrics
        return None
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return None

def count_syllables(text: str) -> int:
    """
    Counts syllables in a text string using Pyphen.
    """
    dic = pyphen.Pyphen(lang='en_US')
    words = text.split()
    count = 0
    for word in words:
        # Remove punctuation for better counting
        clean_word = ''.join(c for c in word if c.isalnum())
        if clean_word:
            count += len(dic.inserted(clean_word).split('-'))
    return count

def generate_parody(original_lyrics_lines: List[str], topic: str) -> List[str]:
    """
    Generates parody lyrics using OpenAI API.
    Requires OPENAI_API_KEY env var.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found. Returning placeholder lyrics.")
        return [f"[Parody] {line}" for line in original_lyrics_lines]

    client = OpenAI(api_key=api_key)
    
    # Construct prompt
    prompt = f"Write a parody of the following song lyrics about the topic: '{topic}'.\n"
    prompt += "Try to match the syllable count and rhythm of each line.\n\n"
    prompt += "Original Lyrics:\n"
    prompt += "\n".join(original_lyrics_lines)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a creative songwriter specializing in parodies."},
                {"role": "user", "content": prompt}
            ]
        )
        parody_text = response.choices[0].message.content
        return parody_text.strip().split('\n')
    except Exception as e:
        print(f"Error generating parody: {e}")
        return [f"[Error] {line}" for line in original_lyrics_lines]
