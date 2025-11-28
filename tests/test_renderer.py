import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from renderer import render_video

class TestRenderer(unittest.TestCase):
    
    @patch('renderer.VideoFileClip')
    @patch('renderer.AudioFileClip')
    @patch('renderer.TextClip')
    @patch('renderer.CompositeVideoClip')
    @patch('renderer.ColorClip')
    def test_render_video(self, mock_color, mock_composite, mock_text, mock_audio, mock_video):
        # Setup mocks
        mock_video_instance = MagicMock()
        mock_video.return_value = mock_video_instance
        mock_video_instance.resized.return_value = mock_video_instance
        mock_video_instance.with_position.return_value = mock_video_instance
        mock_video_instance.with_margin.return_value = mock_video_instance
        mock_video_instance.subclipped.return_value = mock_video_instance
        mock_video_instance.duration = 100
        
        mock_audio_instance = MagicMock()
        mock_audio.return_value = mock_audio_instance
        mock_audio_instance.duration = 10
        
        mock_text_instance = MagicMock()
        mock_text.return_value = mock_text_instance
        mock_text_instance.with_position.return_value = mock_text_instance
        mock_text_instance.with_start.return_value = mock_text_instance
        mock_text_instance.with_end.return_value = mock_text_instance
        
        mock_composite_instance = MagicMock()
        mock_composite.return_value = mock_composite_instance
        mock_composite_instance.with_audio.return_value = mock_composite_instance
        
        mock_color_instance = MagicMock()
        mock_color.return_value = mock_color_instance
        mock_color_instance.with_duration.return_value = mock_color_instance
        
        # Run function
        lyrics = [(0, 5, "Line 1"), (5, 10, "Line 2")]
        render_video("video.mp4", "audio.mp3", lyrics, "output.mp4")
        
        # Verify calls
        mock_video.assert_called_with("video.mp4")
        mock_audio.assert_called_with("audio.mp3")
        self.assertEqual(mock_text.call_count, 2)
        mock_composite.assert_called()
        mock_composite_instance.write_videofile.assert_called_with("output.mp4", fps=24, codec='libx264', audio_codec='aac')

if __name__ == '__main__':
    unittest.main()
