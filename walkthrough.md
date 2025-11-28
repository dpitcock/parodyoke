# Parody Karaoke Video Generator Walkthrough

## Overview
This tool allows you to generate parody karaoke videos from YouTube links. It downloads the video, separates the vocals to create an instrumental track, generates parody lyrics using OpenAI (or a placeholder), and renders a final video with the new lyrics.

## Prerequisites
1.  **Python 3.10+**
2.  **FFmpeg**: Must be installed and in your PATH.
3.  **ImageMagick**: Required for text rendering.
    -   **Mac**: `brew install imagemagick`
    -   **Linux**: `sudo apt install imagemagick`
    -   **Windows**: Download installer. Ensure "Install legacy utilities (convert)" is checked or configure MoviePy to find the binary.
4.  **API Keys** (Optional but recommended):
    -   `OPENAI_API_KEY`: For generating parody lyrics.
    -   `GENIUS_ACCESS_TOKEN`: For fetching original lyrics if subtitles are missing.

## Setup
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_openai_key
    GENIUS_ACCESS_TOKEN=your_genius_token
    ```

    ```

## Finding Compatible Videos
This tool currently relies on **YouTube Subtitles (CC)** to know *when* to display each line of lyrics.
1.  **Search YouTube** for your song (e.g., "Bohemian Rhapsody").
2.  Click the **Filters** button at the top of the search results.
3.  Under **Features**, select **Subtitles/CC**.
4.  Choose a video. **Official Music Videos** are usually the best bet as they often contain accurate, timed subtitles.
    *   *Note: Many "Karaoke Version" videos have lyrics burned into the video but do NOT have a subtitle file. These will not work yet.*

## Usage
Run the tool via the CLI:

```bash
python main.py <YOUTUBE_URL> --topic "your topic"
```

### Example
```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --topic "debugging code"
```
```

### Manual Lyrics Input
You can bypass the AI generation or provide your own source text using local files. This is useful for saving API costs or refining the lyrics.

**Arguments:**
-   `--parody-file`: Path to a text file containing your custom parody lyrics.
-   `--original-file`: Path to a text file containing original lyrics (provides better context for the AI than raw subtitles).

**File Format:**
-   Plain text file (`.txt`).
-   One line of text per subtitle block.
-   *Tip: Run the tool once without these args to see how many lines/blocks are detected, then match that count in your file.*

**Example:**
```bash
python main.py "https://www.youtube.com/watch?v=..." --parody-file my_parody.txt
```

### Customizing Metadata & Filenames
You can control the output filename and metadata using the following arguments. If you don't provide a title, the AI will generate one for you.

**Arguments:**
-   `--author`: The name of the parody author (defaults to "AI").
-   `--parody-title`: The title of your parody song.

**Automatic Renaming:**
The tool will automatically clean the original video title (removing "Official Video", etc.) and format the final filename as:
`{{author}} - {{parody-title}} of {{orig_artist}} - {{orig-title}}.mp4`

**Example:**
```bash
python main.py "https://www.youtube.com/watch?v=..." --topic "coffee" --author "JavaJim" --parody-title "Caffeine Addiction"
# Output: JavaJim - Caffeine Addiction of Artist - Song.mp4
```
## How it Works
1.  **Download**: `yt-dlp` fetches the video and SRT subtitles.
2.  **Audio**: `demucs` separates the vocals from the music.
3.  **Lyrics**: The tool analyzes the original lyrics (from SRT) and generates a parody matching the rhythm.
4.  **Render**: `moviepy` combines the instrumental audio, the original video (in PiP), and the new lyrics overlays.

## Troubleshooting
-   **ImageMagick Error**: If you see an error about `convert` or `ImageMagick`, ensure it is installed. MoviePy relies on it for `TextClip`.
-   **Demucs Error**: The first run of Demucs might take time to download models. Ensure you have a stable internet connection.
-   **No Subtitles**: If the YouTube video doesn't have subtitles, the tool cannot currently sync lyrics. Try finding a video with CC/Subtitles enabled.
