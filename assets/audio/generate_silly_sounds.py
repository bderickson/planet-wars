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
    """Generate a VERY silly cartoon-style victory jingle with whoops and squeaks"""
    sample_rate = 22050
    duration = 1.2
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    # Super silly ascending melody with exaggerated vibrato and slides
    notes = [
        (330, 0.0, 0.15),    # E (low silly start)
        (392, 0.15, 0.3),    # G (slide up)
        (494, 0.3, 0.45),    # B 
        (587, 0.45, 0.6),    # D (higher!)
        (784, 0.6, 1.2),     # G (very high, held with warble)
    ]
    
    for freq, start, end in notes:
        for i in range(num_samples):
            t = i / sample_rate
            if start <= t < end:
                # EXTREME cartoonish vibrato and pitch wobble
                vibrato = 1.0 + 0.15 * math.sin(2 * math.pi * 12 * t)  # More wobble!
                
                # Add pitch slide between notes
                progress = (t - start) / (end - start)
                if progress < 0.3:  # Quick slide up at start of each note
                    slide = 0.8 + 0.2 * (progress / 0.3)
                else:
                    slide = 1.0
                
                freq_with_effects = freq * vibrato * slide
                
                # Bouncy envelope with "squeak" character
                envelope = (1.0 - (progress ** 0.3)) * (0.9 + 0.1 * math.sin(30 * t))
                
                # Add harmonics for squeaky character
                fundamental = math.sin(2 * math.pi * freq_with_effects * t)
                harmonic2 = 0.3 * math.sin(2 * math.pi * freq_with_effects * 2 * t)
                harmonic3 = 0.15 * math.sin(2 * math.pi * freq_with_effects * 3 * t)
                
                arr[i] += int(envelope * 18000 * (fundamental + harmonic2 + harmonic3))
    
    # Add silly "trill" at the end
    for i in range(int(sample_rate * 0.8), num_samples):
        t = i / sample_rate
        trill_freq = 1000 + 200 * math.sin(2 * math.pi * 40 * t)
        envelope = math.exp(-8 * (t - 0.8))
        arr[i] += int(envelope * 8000 * math.sin(2 * math.pi * trill_freq * t))
    
    stereo_arr = np.column_stack((arr, arr))
    return pygame.sndarray.make_sound(stereo_arr)

def generate_bonk():
    """Generate an exaggerated cartoon BONK sound with comedic timing"""
    sample_rate = 22050
    duration = 0.35
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    # Classic "BONK" - two-stage hit with pitch drop
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        
        # Initial high impact, then "wobble" drop
        if t < 0.05:
            # Sharp high BONK
            freq = 800 - (400 * (t / 0.05))
            envelope = 1.0
        else:
            # Wobbly aftermath with "dizzy stars" effect
            wobble = 20 * math.sin(2 * math.pi * 8 * t)
            freq = 150 + wobble
            envelope = math.exp(-12 * (t - 0.05))
        
        # Add metallic "clang" overtones
        tone = math.sin(2 * math.pi * freq * t)
        overtone1 = 0.4 * math.sin(2 * math.pi * freq * 2.3 * t)  # Inharmonic!
        overtone2 = 0.2 * math.sin(2 * math.pi * freq * 3.7 * t)
        
        # Add percussive noise for impact
        noise_amount = math.exp(-40 * t)
        noise = (np.random.randint(-3000, 3000) * noise_amount) if i % 3 == 0 else 0
        
        combined = envelope * (tone + overtone1 + overtone2) * 15000 + noise * 0.4
        arr[i] = int(np.clip(combined, -32767, 32767))
    
    stereo_arr = np.column_stack((arr, arr))
    return pygame.sndarray.make_sound(stereo_arr)

def generate_boing():
    """Generate an exaggerated rubber band / spring BOING sound"""
    sample_rate = 22050
    duration = 0.6
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    # Mega-spring effect - wild oscillating frequency
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        
        # EXTREME spring oscillation with multiple frequencies
        # Creates that classic "boiyoiyoing" sound
        oscillation1 = 250 * math.sin(2 * math.pi * 12 * t) * math.exp(-3 * t)
        oscillation2 = 100 * math.sin(2 * math.pi * 25 * t) * math.exp(-5 * t)
        oscillation3 = 50 * math.sin(2 * math.pi * 40 * t) * math.exp(-8 * t)
        
        freq = 180 + oscillation1 + oscillation2 + oscillation3
        
        # Bouncy decay with slight "flutter"
        flutter = 1.0 + 0.05 * math.sin(2 * math.pi * 30 * t)
        envelope = math.exp(-2.5 * t) * flutter
        
        # Add harmonics for more character
        fundamental = math.sin(2 * math.pi * freq * t)
        harmonic2 = 0.4 * math.sin(2 * math.pi * freq * 1.5 * t)  # Not quite octave for silly effect
        harmonic3 = 0.2 * math.sin(2 * math.pi * freq * 2.2 * t)
        
        combined = fundamental + harmonic2 + harmonic3
        arr[i] = int(envelope * 14000 * combined)
    
    # Add a little "twang" at the end
    for i in range(int(sample_rate * 0.4), num_samples):
        t = i / sample_rate
        twang_t = t - 0.4
        twang_freq = 600 * math.exp(-10 * twang_t)
        twang_envelope = math.exp(-15 * twang_t)
        arr[i] += int(twang_envelope * 5000 * math.sin(2 * math.pi * twang_freq * t))
    
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

