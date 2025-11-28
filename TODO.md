# Project TODOs

## Core Features (Completed)
- [x] YouTube Video Downloader
- [x] Audio Extraction & Vocal Separation (Demucs)
- [x] Lyrics Fetching (Genius)
- [x] AI Parody Generation (OpenAI)
- [x] Manual Lyrics Input Support
- [x] Video Rendering with PiP and Text Overlays
- [x] CLI Interface

## Future Enhancements / Backlog
- [ ] **Video OCR (Computer Vision)**: Use OpenCV/Tesseract to read hardcoded lyrics from video frames when SRT is missing. This is crucial for most karaoke videos.
- [ ] **Karaoke Highlighting**: Animate text color to match the singing timing (requires word-level timestamps).
- [ ] **GUI**: Create a simple frontend (e.g., Streamlit or Gradio) for non-CLI users.
- [ ] **Cleanup**: Automatically delete temporary files after successful rendering.
- [ ] **Multi-language Support**: Better support for non-English songs and lyrics.
- [ ] **Custom Fonts/Styles**: Allow users to configure font, color, and position of lyrics via CLI args.
- [ ] **Preview Mode**: Generate a short snippet (e.g., 30s) to test synchronization before full render.
