# Parody Karaoke Video Generator

A Python tool to create parody karaoke videos.

## Features
-   Downloads YouTube videos and subtitles.
-   Removes vocals to create instrumental tracks (using Demucs).
-   Generates parody lyrics (using OpenAI).
-   Renders final video with synchronized lyrics and PiP original.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py <URL> --topic "topic"
```

See `walkthrough.md` for details.

## Disclaimer

**This project is for educational and personal use only.**

This tool processes copyrighted material (YouTube videos, audio tracks). Users are responsible for ensuring they have the right to use the content they download and process.

-   **Do not distribute** the output videos if they contain copyrighted audio or video without permission.
-   **Consult your local copyright laws** regarding fair use, parody, and private copying.
-   The authors of this tool are not responsible for any misuse.

