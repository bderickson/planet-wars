#!/usr/bin/env python3
"""
Trim MP3 audio files to a specified duration and convert to OGG.

Usage:
    python trim_audio.py <input_file> <duration_seconds> [output_base_name]
    
Examples:
    python trim_audio.py full_song.mp3 5
    python trim_audio.py beethoven.mp3 4 beethoven-symphony-no5_trimmed_4s
    
This will create:
    - mp3/<output_base_name>.mp3 (trimmed MP3)
    - ogg/<output_base_name>.ogg (trimmed OGG for browser)
"""

import sys
import os
from pydub import AudioSegment

def trim_and_convert_audio(input_file, duration_seconds, output_base_name=None):
    """
    Trim an audio file to the specified duration and save as both MP3 and OGG.
    
    Args:
        input_file: Path to input MP3 file
        duration_seconds: Duration in seconds to trim to
        output_base_name: Base name for output files (without extension)
                         If None, derives from input filename
    """
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        return False
    
    # Ensure output directories exist
    os.makedirs('mp3', exist_ok=True)
    os.makedirs('ogg', exist_ok=True)
    
    # Generate output base name if not provided
    if output_base_name is None:
        # Remove path and extension from input file
        base = os.path.basename(input_file)
        output_base_name = os.path.splitext(base)[0] + f"_trimmed_{int(duration_seconds)}s"
    
    try:
        print(f"Loading {input_file}...")
        audio = AudioSegment.from_mp3(input_file)
        
        # Trim to specified duration (pydub uses milliseconds)
        duration_ms = int(duration_seconds * 1000)
        print(f"Trimming to {duration_seconds} seconds...")
        trimmed = audio[:duration_ms]
        
        # Save as MP3
        mp3_output = f"mp3/{output_base_name}.mp3"
        trimmed.export(mp3_output, format="mp3")
        print(f"  ✓ Trimmed MP3 saved: {mp3_output}")
        
        # Save as OGG (browser-compatible)
        ogg_output = f"ogg/{output_base_name}.ogg"
        trimmed.export(ogg_output, format="ogg")
        print(f"  ✓ Converted OGG saved: {ogg_output}")
        
        print(f"\n✓ Successfully trimmed to {duration_seconds} seconds")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python trim_audio.py <input_file> <duration_seconds> [output_base_name]")
        print()
        print("Examples:")
        print("  python trim_audio.py full_song.mp3 5")
        print("  python trim_audio.py beethoven.mp3 4 beethoven-symphony-no5_trimmed_4s")
        print()
        print("Requires: pip install pydub")
        print("          brew install ffmpeg  # or: sudo apt-get install ffmpeg")
        sys.exit(1)
    
    input_file = sys.argv[1]
    duration = float(sys.argv[2])
    output_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = trim_and_convert_audio(input_file, duration, output_name)
    sys.exit(0 if success else 1)

