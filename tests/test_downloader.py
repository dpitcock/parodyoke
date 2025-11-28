import sys
import os
import unittest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from downloader import parse_srt, _time_to_seconds

class TestDownloader(unittest.TestCase):
    def test_time_to_seconds(self):
        self.assertAlmostEqual(_time_to_seconds("00:00:01,500"), 1.5)
        self.assertAlmostEqual(_time_to_seconds("01:01:01,000"), 3661.0)

    def test_parse_srt(self):
        srt_content = """1
00:00:01,000 --> 00:00:04,000
Line 1 text

2
00:00:04,500 --> 00:00:06,000
Line 2 text
with newline
"""
        with open("temp_test.srt", "w") as f:
            f.write(srt_content)

        try:
            parsed = parse_srt("temp_test.srt")
            self.assertEqual(len(parsed), 2)
            self.assertEqual(parsed[0], (1.0, 4.0, "Line 1 text"))
            self.assertEqual(parsed[1], (4.5, 6.0, "Line 2 text with newline"))
        finally:
            if os.path.exists("temp_test.srt"):
                os.remove("temp_test.srt")

if __name__ == '__main__':
    unittest.main()
