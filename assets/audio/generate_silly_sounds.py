#!/usr/bin/env python3
"""
Generate silly/cartoon sound effects for the Silly sound plugin
Run this once to create the MP3 files
"""
import numpy as np
import pygame
import math
from pydub import AudioSegment
from pydub.generators import Sine
import io

# Initialize pygame mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

def generate_cartoon_victory():
    """Generate a silly cartoon-style victory jingle"""
    sample_rate = 22050
    duration = 0.8
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    # Silly ascending melody with vibrato
    notes = [
        (392, 0.0, 0.15),    # G
        (440, 0.15, 0.3),    # A
        (494, 0.3, 0.45),    # B
        (523, 0.45, 0.8),    # C (held)
    ]
    
    for freq, start, end in notes:
        for i in range(num_samples):
            t = i / sample_rate
            if start <= t < end:
                # Add cartoonish vibrato
                vibrato = 1.0 + 0.05 * math.sin(2 * math.pi * 8 * t)
                freq_with_vibrato = freq * vibrato
                
                # Bouncy envelope
                progress = (t - start) / (end - start)
                envelope = 1.0 - (progress ** 0.5)
                
                arr[i] += int(envelope * 15000 * math.sin(2 * math.pi * freq_with_vibrato * t))
    
    stereo_arr = np.column_stack((arr, arr))
    return pygame.sndarray.make_sound(stereo_arr)

def generate_bonk():
    """Generate a cartoon bonk/hit sound"""
    sample_rate = 22050
    duration = 0.2
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    # Short percussive hit with pitch drop
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        
        # Rapidly descending frequency (bonk!)
        freq = 400 - (350 * progress)
        
        # Sharp attack, quick decay
        envelope = math.exp(-15 * t)
        
        # Add noise for impact
        noise = np.random.randint(-5000, 5000) if i % 2 == 0 else 0
        tone = 20000 * math.sin(2 * math.pi * freq * t)
        
        arr[i] = int(envelope * (tone * 0.7 + noise * 0.3))
    
    stereo_arr = np.column_stack((arr, arr))
    return pygame.sndarray.make_sound(stereo_arr)

def generate_boing():
    """Generate a spring/boing sound"""
    sample_rate = 22050
    duration = 0.4
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    # Spring effect - oscillating frequency
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        
        # Base frequency with dampened oscillation
        oscillation = 150 * math.sin(2 * math.pi * 15 * t) * math.exp(-4 * t)
        freq = 200 + oscillation
        
        # Decay envelope
        envelope = math.exp(-3 * t)
        
        arr[i] = int(envelope * 12000 * math.sin(2 * math.pi * freq * t))
    
    stereo_arr = np.column_stack((arr, arr))
    return pygame.sndarray.make_sound(stereo_arr)

def save_pygame_sound_as_mp3_and_ogg(sound, base_name):
    """Convert pygame Sound to both MP3 and OGG formats"""
    # Get the raw audio data from pygame sound
    sound_array = pygame.sndarray.array(sound)
    
    # Convert to bytes
    byte_data = sound_array.tobytes()
    
    # Create AudioSegment from raw data
    audio = AudioSegment(
        data=byte_data,
        sample_width=2,  # 16-bit = 2 bytes
        frame_rate=22050,
        channels=2
    )
    
    # Export as MP3
    mp3_filename = f"mp3/{base_name}.mp3"
    audio.export(mp3_filename, format="mp3", bitrate="128k")
    print(f"  ✓ Saved {mp3_filename}")
    
    # Export as OGG (browser-compatible)
    ogg_filename = f"ogg/{base_name}.ogg"
    audio.export(ogg_filename, format="ogg")
    print(f"  ✓ Saved {ogg_filename}")

if __name__ == "__main__":
    print("🎵 Generating Silly Sound Effects for Planet Wars")
    print("=" * 60)
    print()
    
    # Generate conquest sound
    print("Generating cartoon victory sound...")
    conquest = generate_cartoon_victory()
    save_pygame_sound_as_mp3_and_ogg(conquest, "silly_conquest")
    
    # Generate explosion sound
    print("\nGenerating bonk sound...")
    explosion = generate_bonk()
    save_pygame_sound_as_mp3_and_ogg(explosion, "silly_explosion")
    
    # Generate launch sound
    print("\nGenerating boing sound...")
    launch = generate_boing()
    save_pygame_sound_as_mp3_and_ogg(launch, "silly_launch")
    
    print()
    print("=" * 60)
    print("✓ All silly sounds generated successfully!")
    print()
    print("Files created in mp3/ and ogg/ directories:")
    print("  - silly_conquest (MP3 + OGG)")
    print("  - silly_explosion (MP3 + OGG)")
    print("  - silly_launch (MP3 + OGG)")

