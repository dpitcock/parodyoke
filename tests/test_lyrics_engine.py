import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from lyrics_engine import count_syllables, fetch_lyrics, generate_parody

class TestLyricsEngine(unittest.TestCase):
    
    def test_count_syllables(self):
        self.assertEqual(count_syllables("hello"), 2)
        self.assertEqual(count_syllables("world"), 1)
        self.assertEqual(count_syllables("computer"), 3)

    @patch('lyrics_engine.lyricsgenius.Genius')
    @patch('os.getenv')
    def test_fetch_lyrics(self, mock_getenv, mock_genius_cls):
        mock_getenv.return_value = "fake_token"
        mock_genius_instance = MagicMock()
        mock_genius_cls.return_value = mock_genius_instance
        
        mock_song = MagicMock()
        mock_song.lyrics = "Verse 1\nHello world"
        mock_genius_instance.search_song.return_value = mock_song
        
        lyrics = fetch_lyrics("Song", "Artist")
        self.assertEqual(lyrics, "Verse 1\nHello world")
        mock_genius_instance.search_song.assert_called_with("Song", "Artist")

    @patch('lyrics_engine.OpenAI')
    @patch('os.getenv')
    def test_generate_parody(self, mock_getenv, mock_openai_cls):
        mock_getenv.return_value = "fake_key"
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Parody line 1\nParody line 2"
        mock_client.chat.completions.create.return_value = mock_response
        
        original = ["Line 1", "Line 2"]
        parody = generate_parody(original, "coding")
        
        self.assertEqual(len(parody), 2)
        self.assertEqual(parody[0], "Parody line 1")
        self.assertEqual(parody[1], "Parody line 2")

if __name__ == '__main__':
    unittest.main()
