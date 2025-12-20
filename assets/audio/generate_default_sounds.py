#!/usr/bin/env python3
"""
Generate default sound effects for Planet Wars

This script generates the default space-themed sound effects and saves them as MP3 files.
Run this once to create the sound files, then the game can load them directly.
"""
import numpy as np
import math
import pygame
import sys


def generate_energy_beam():
    """Generate a sci-fi energy beam/laser conquest sound"""
    sample_rate = 22050
    duration = 1.2
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.float32)
    
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        
        # Energy charging up then sustained beam
        if progress < 0.15:  # Charge up
            charge_progress = progress / 0.15
            freq = 200 + (400 * charge_progress)
            envelope = charge_progress
        else:  # Sustained beam with slight modulation
            freq = 600 + 100 * math.sin(2 * math.pi * 8 * t)
            envelope = 0.9 * (1.0 - ((progress - 0.15) / 0.85) ** 2)
        
        # Add harmonics for electronic texture
        base_wave = math.sin(2 * math.pi * freq * t)
        harmonic1 = 0.3 * math.sin(2 * math.pi * freq * 1.5 * t)
        harmonic2 = 0.2 * math.sin(2 * math.pi * freq * 2.5 * t)
        
        # Add slight noise for texture
        noise = (np.random.random() - 0.5) * 0.1
        
        arr[i] = envelope * 18000 * (base_wave + harmonic1 + harmonic2 + noise)
    
    arr = np.clip(arr, -32767, 32767).astype(np.int16)
    stereo_arr = np.column_stack((arr, arr))
    return stereo_arr


def generate_space_explosion():
    """Generate a sci-fi space explosion sound"""
    sample_rate = 22050
    duration = 0.8
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        
        # Initial impact with descending frequency
        impact_freq = 300 - (250 * progress)
        impact = 12000 * math.sin(2 * math.pi * impact_freq * t)
        
        # Explosion rumble (low frequency)
        rumble_freq = 60 + 40 * math.sin(2 * math.pi * 5 * t)
        rumble = 8000 * math.sin(2 * math.pi * rumble_freq * t)
        
        # White noise decay
        noise = np.random.randint(-15000, 15000)
        
        # Sharp attack, exponential decay
        envelope = math.exp(-4 * t)
        
        # Mix all components
        arr[i] = int(envelope * (impact * 0.4 + rumble * 0.3 + noise * 0.3))
    
    stereo_arr = np.column_stack((arr, arr))
    return stereo_arr


def generate_warp_launch():
    """Generate a futuristic warp drive launch sound"""
    sample_rate = 22050
    duration = 0.6
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.int16)
    
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        
        # Rapidly ascending frequency (warp acceleration)
        freq = 150 + (800 * progress ** 2)
        
        # Add doppler-like effect
        doppler = 1.0 + 0.5 * progress
        
        # Build envelope - crescendo
        envelope = min(1.0, progress * 3) * (1.0 - progress * 0.3)
        
        # Create the warp sound with harmonics
        warp = math.sin(2 * math.pi * freq * doppler * t)
        warp += 0.4 * math.sin(2 * math.pi * freq * 1.5 * doppler * t)
        
        arr[i] = int(envelope * 14000 * warp)
    
    stereo_arr = np.column_stack((arr, arr))
    return stereo_arr


def generate_victory_fanfare():
    """Generate a triumphant space victory fanfare"""
    sample_rate = 22050
    duration = 2.5
    
    num_samples = int(sample_rate * duration)
    arr = np.zeros(num_samples, dtype=np.float32)
    
    # Epic ascending fanfare melody (space hero theme)
    # Using a triumphant progression: C -> E -> G -> C (major triad)
    notes = [
        (261.63, 0.0, 0.35),    # C (confident start)
        (329.63, 0.35, 0.7),    # E (rising)
        (392.00, 0.7, 1.05),    # G (building)
        (523.25, 1.05, 1.7),    # High C (triumph!)
        (659.25, 1.7, 2.5),     # High E (sustained victory)
    ]
    
    for freq, start, end in notes:
        for i in range(num_samples):
            t = i / sample_rate
            if start <= t < end:
                note_progress = (t - start) / (end - start)
                
                # Heroic envelope with sustain
                if note_progress < 0.1:
                    envelope = note_progress / 0.1  # Quick attack
                elif note_progress < 0.7:
                    envelope = 1.0  # Sustain
                else:
                    envelope = 1.0 - ((note_progress - 0.7) / 0.3) * 0.3  # Gentle decay
                
                # Add electronic/synth harmonics for sci-fi feel
                base = math.sin(2 * math.pi * freq * t)
                harmonic1 = 0.4 * math.sin(2 * math.pi * freq * 2 * t)
                harmonic2 = 0.2 * math.sin(2 * math.pi * freq * 3 * t)
                
                # Add slight vibrato on sustained notes
                if note_progress > 0.3:
                    vibrato = 1.0 + 0.02 * math.sin(2 * math.pi * 5 * t)
                else:
                    vibrato = 1.0
                
                arr[i] += envelope * 16000 * vibrato * (base + harmonic1 + harmonic2)
    
    # Add some sparkle/shimmer effect in the background
    for i in range(num_samples):
        t = i / sample_rate
        if t > 1.0:  # Start shimmer effect after the melody builds
            shimmer_freq = 1500 + 500 * math.sin(2 * math.pi * 8 * t)
            shimmer_envelope = 0.15 * math.sin(math.pi * (t - 1.0) / 1.5)
            arr[i] += shimmer_envelope * 8000 * math.sin(2 * math.pi * shimmer_freq * t)
    
    arr = np.clip(arr, -32767, 32767).astype(np.int16)
    stereo_arr = np.column_stack((arr, arr))
    return stereo_arr


def save_as_wav_then_convert(audio_array, filename, sample_rate=22050):
    """Save audio array as WAV, then convert to MP3 using pydub"""
    import os
    
    # First save as WAV using pygame
    wav_filename = filename.replace('.mp3', '.wav')
    
    try:
        # Initialize pygame mixer
        pygame.mixer.init(frequency=sample_rate, size=-16, channels=2, buffer=512)
        
        # Create sound from array
        sound = pygame.sndarray.make_sound(audio_array)
        
        # pygame doesn't have a direct save method, so we'll use pydub
        # to create the WAV from the raw audio data
        try:
            from pydub import AudioSegment
            import array
            
            # Convert numpy array to bytes
            audio_bytes = audio_array.tobytes()
            
            # Create AudioSegment from raw data
            audio = AudioSegment(
                audio_bytes,
                frame_rate=sample_rate,
                sample_width=2,  # 16-bit
                channels=2  # Stereo
            )
            
            # Export as MP3
            audio.export(filename, format='mp3', bitrate='128k')
            print(f"  ✓ Saved as MP3: {filename}")
            return True
            
        except Exception as e:
            print(f"  ⚠️  pydub/ffmpeg not available, saving as WAV: {e}")
            
            # Fall back to WAV using wave module
            import wave
            
            with wave.open(wav_filename, 'w') as wav_file:
                wav_file.setnchannels(2)  # Stereo
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_array.tobytes())
            
            print(f"  ✓ Saved as WAV: {wav_filename}")
            return True
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    finally:
        try:
            pygame.mixer.quit()
        except:
            pass


def main():
    """Generate all default sounds in both MP3 and OGG formats"""
    print("🎵 Generating Default Sound Effects for Planet Wars")
    print("=" * 60)
    
    sounds = [
        ('default_conquest', generate_energy_beam, 'Energy Beam (Conquest)'),
        ('default_explosion', generate_space_explosion, 'Space Explosion (Attack Failed)'),
        ('default_launch', generate_warp_launch, 'Warp Launch (Fleet Launch)'),
        ('default_victory', generate_victory_fanfare, 'Victory Fanfare'),
    ]
    
    success_count = 0
    for base_name, generator_func, description in sounds:
        print(f"\nGenerating: {description}")
        
        try:
            # Generate audio
            audio_array = generator_func()
            
            # Save as MP3 in mp3/ directory
            mp3_filename = f"mp3/{base_name}.mp3"
            if save_as_wav_then_convert(audio_array, mp3_filename):
                print(f"  ✓ MP3 saved: {mp3_filename}")
                
                # Convert to OGG for browser compatibility
                try:
                    from pydub import AudioSegment
                    ogg_filename = f"ogg/{base_name}.ogg"
                    audio = AudioSegment.from_mp3(mp3_filename)
                    audio.export(ogg_filename, format='ogg')
                    print(f"  ✓ OGG saved: {ogg_filename}")
                    success_count += 1
                except Exception as e:
                    print(f"  ✗ Failed to convert to OGG: {e}")
            else:
                print(f"  ✗ Failed to save MP3")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully generated {success_count}/{len(sounds)} sounds")
    
    if success_count == len(sounds):
        print("\n🎉 All sounds generated successfully!")
        print("\nNext steps:")
        print("  1. The game will now load OGG files (browser-compatible)")
        print("  2. MP3 files are kept for reference/desktop use")
        print("  3. Faster startup time!")
    else:
        print(f"\n⚠️  Some sounds failed to generate")
        print("Make sure you have pydub and ffmpeg installed")
        sys.exit(1)


if __name__ == "__main__":
    main()

