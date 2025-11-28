import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from audio_processor import extract_audio, separate_vocals

class TestAudioProcessor(unittest.TestCase):
    
    @patch('audio_processor.VideoFileClip')
    def test_extract_audio(self, mock_clip_cls):
        # Setup mock
        mock_clip_instance = MagicMock()
        mock_clip_cls.return_value.__enter__.return_value = mock_clip_instance
        
        # Create a dummy file to pass existence check
        with open("dummy_video.mp4", "w") as f:
            f.write("dummy")
            
        try:
            output = extract_audio("dummy_video.mp4", "output.mp3")
            
            # Verify calls
            mock_clip_cls.assert_called_with("dummy_video.mp4")
            mock_clip_instance.audio.write_audiofile.assert_called_with("output.mp3", logger=None)
            self.assertEqual(output, "output.mp3")
        finally:
            if os.path.exists("dummy_video.mp4"):
                os.remove("dummy_video.mp4")

    @patch('audio_processor.subprocess.run')
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_separate_vocals(self, mock_makedirs, mock_exists, mock_run):
        # Setup mocks
        # We need os.path.exists to return True for input file, and then True for output file check
        # This is tricky with side_effect, so let's just mock it to always True for simplicity in this unit test
        mock_exists.return_value = True
        
        output = separate_vocals("input.mp3", "temp_out")
        
        # Verify subprocess call
        expected_cmd = [
            "demucs", "-n", "htdemucs", "--two-stems=vocals", "-o", "temp_out", "input.mp3"
        ]
        mock_run.assert_called_with(expected_cmd, check=True)
        
        # Verify output path construction
        # input.mp3 -> temp_out/htdemucs/input/no_vocals.wav
        self.assertTrue(output.endswith("no_vocals.wav"))
        self.assertIn("htdemucs", output)

if __name__ == '__main__':
    unittest.main()
