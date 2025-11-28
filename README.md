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
