import argparse
import os
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from downloader import download_video, parse_srt
from audio_processor import extract_audio, separate_vocals
from lyrics_engine import fetch_lyrics, generate_parody, count_syllables
from renderer import render_video

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Parody Karaoke Video Generator")
    parser.add_argument("url", help="YouTube URL of the karaoke video")
    parser.add_argument("--topic", help="Topic for parody lyrics", default="coding")
    parser.add_argument("--output", help="Output filename", default="parody_karaoke.mp4")
    parser.add_argument("--skip-download", help="Skip download if files exist", action="store_true")
    parser.add_argument("--parody-file", help="Path to a text file containing parody lyrics (one line per subtitle block)")
    parser.add_argument("--original-file", help="Path to a text file containing original lyrics (for generation context)")
    args = parser.parse_args()

    console.print(f"[bold green]Starting Parodyoke[/bold green]")
    console.print(f"URL: {args.url}")
    console.print(f"Topic: {args.topic}")

    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        # 1. Download
        task_dl = progress.add_task(description="Downloading video...", total=None)
        try:
            if args.skip_download and os.path.exists(os.path.join(temp_dir, "video.mp4")): # Simplified check
                 # In a real app, we'd need to know the exact filename. 
                 # For now, let's assume the user knows what they are doing or we re-download.
                 # Actually, let's just run the download_video function, it should be fast if files exist?
                 # yt-dlp checks existence.
                 pass
            
            video_path, srt_path = download_video(args.url, temp_dir)
            if not video_path:
                console.print("[red]Failed to download video.[/red]")
                return
            console.print(f"[green]Downloaded:[/green] {video_path}")
            if srt_path:
                console.print(f"[green]Subtitles:[/green] {srt_path}")
            else:
                console.print("[yellow]No subtitles found. Lyrics timing might be missing.[/yellow]")
        except Exception as e:
            console.print(f"[red]Download error:[/red] {e}")
            return
        progress.remove_task(task_dl)

        # 2. Audio Processing
        task_audio = progress.add_task(description="Processing audio...", total=None)
        try:
            audio_path = extract_audio(video_path)
            console.print(f"[green]Extracted audio:[/green] {audio_path}")
            
            # Check for Demucs
            try:
                instrumental_path = separate_vocals(audio_path, temp_dir)
                console.print(f"[green]Instrumental track:[/green] {instrumental_path}")
            except Exception as e:
                console.print(f"[yellow]Vocal separation failed (Demucs missing?):[/yellow] {e}")
                console.print("Using original audio as fallback.")
                instrumental_path = audio_path
        except Exception as e:
            console.print(f"[red]Audio processing error:[/red] {e}")
            return
        progress.remove_task(task_audio)

        # 3. Lyrics
        task_lyrics = progress.add_task(description="Preparing lyrics...", total=None)
        try:
            lyrics_data = []
            if srt_path:
                parsed_subs = parse_srt(srt_path)
                
                parody_lines = []
                
                # Case A: User provided parody lyrics file
                if args.parody_file:
                    if os.path.exists(args.parody_file):
                        console.print(f"[green]Using manual parody lyrics from:[/green] {args.parody_file}")
                        with open(args.parody_file, 'r', encoding='utf-8') as f:
                            parody_lines = [line.strip() for line in f if line.strip()]
                    else:
                        console.print(f"[red]Parody file not found:[/red] {args.parody_file}")
                        return

                # Case B: Generate parody lyrics
                else:
                    original_lines = []
                    # Use provided original lyrics file for context if available
                    if args.original_file and os.path.exists(args.original_file):
                        console.print(f"[green]Using manual original lyrics for generation context:[/green] {args.original_file}")
                        with open(args.original_file, 'r', encoding='utf-8') as f:
                            original_lines = [line.strip() for line in f if line.strip()]
                    else:
                        # Fallback to SRT text
                        original_lines = [text for _, _, text in parsed_subs]
                    
                    console.print("[blue]Generating parody lyrics with AI...[/blue]")
                    parody_lines = generate_parody(original_lines, args.topic)

                # Align
                # Warning if counts mismatch
                if len(parody_lines) != len(parsed_subs):
                    console.print(f"[yellow]Warning: Line count mismatch. SRT has {len(parsed_subs)} blocks, Lyrics have {len(parody_lines)} lines.[/yellow]")
                
                for i, (start, end, _) in enumerate(parsed_subs):
                    if i < len(parody_lines):
                        lyrics_data.append((start, end, parody_lines[i]))
            else:
                console.print("[red]No subtitles available. Cannot sync lyrics.[/red]")
                pass
        except Exception as e:
            console.print(f"[red]Lyrics error:[/red] {e}")
            return
        progress.remove_task(task_lyrics)

        # 4. Render
        task_render = progress.add_task(description="Rendering video...", total=None)
        try:
            if not lyrics_data:
                console.print("[yellow]No lyrics data to render. Creating instrumental video only.[/yellow]")
            
            render_video(video_path, instrumental_path, lyrics_data, args.output)
            console.print(f"[bold green]Done! Saved to {args.output}[/bold green]")
        except Exception as e:
            console.print(f"[red]Rendering error:[/red] {e}")
            if "convert" in str(e) or "ImageMagick" in str(e):
                console.print("[bold red]ImageMagick is likely missing. Please install it to render text.[/bold red]")
        progress.remove_task(task_render)

if __name__ == "__main__":
    main()
