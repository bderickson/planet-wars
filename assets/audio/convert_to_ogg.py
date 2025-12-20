#!/usr/bin/env python3
"""
Convert MP3 audio files to OGG Vorbis format for browser compatibility.

MP3 files don't work well with Pygame in the browser (Pygbag), but OGG files do.
This script converts all MP3 files in the mp3/ directory to OGG format in the ogg/ directory.

Requirements: pydub, ffmpeg

Install:
    pip install pydub
    brew install ffmpeg  # macOS
    # or: sudo apt-get install ffmpeg  # Linux
"""

import os
from pydub import AudioSegment

def convert_mp3_to_ogg(mp3_filename):
    """Convert an MP3 file from mp3/ to OGG format in ogg/"""
    mp3_path = os.path.join('mp3', mp3_filename)
    
    if not os.path.exists(mp3_path):
        print(f"File not found: {mp3_path}")
        return False
    
    # Generate OGG filename and path
    ogg_filename = mp3_filename.replace('.mp3', '.ogg')
    ogg_path = os.path.join('ogg', ogg_filename)
    
    try:
        print(f"Converting {mp3_filename} to OGG...")
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(ogg_path, format="ogg")
        print(f"  ✓ Created ogg/{ogg_filename}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to convert {mp3_filename}: {e}")
        return False

def main():
    # Ensure directories exist
    os.makedirs('mp3', exist_ok=True)
    os.makedirs('ogg', exist_ok=True)
    
    # Get all MP3 files in the mp3/ directory
    if not os.path.exists('mp3'):
        print("Error: mp3/ directory not found")
        return
    
    mp3_files = [f for f in os.listdir('mp3') if f.endswith('.mp3')]
    
    if not mp3_files:
        print("No MP3 files found in mp3/ directory")
        return
    
    print("Converting MP3 files to OGG for browser compatibility...")
    print("=" * 60)
    
    success_count = 0
    for filename in sorted(mp3_files):
        if convert_mp3_to_ogg(filename):
            success_count += 1
    
    print("=" * 60)
    print(f"Converted {success_count}/{len(mp3_files)} files successfully")
    print("\nNote: You can keep the MP3 files for desktop or delete them if you only need browser support.")

if __name__ == "__main__":
    main()

