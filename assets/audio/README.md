# Audio Assets Guide

This directory contains all audio files for Planet Wars, organized for both desktop and browser compatibility.

## Directory Structure

```
assets/audio/
├── mp3/          # MP3 files (desktop, reference)
├── ogg/          # OGG files (browser-compatible, used by game)
├── README.md     # This file
├── TRIM_INSTRUCTIONS.md  # How to trim audio files
├── convert_to_ogg.py     # Convert MP3 → OGG
├── trim_audio.py         # Trim and convert audio
├── generate_default_sounds.py  # Generate default sound pack
└── generate_silly_sounds.py    # Generate silly sound pack
```

## Browser Compatibility

**🎯 Platform-aware audio loading!**

The game automatically detects the platform and loads the appropriate format:
- 🖥️ **Desktop** (`sys.platform != "emscripten"`): Loads MP3 files from `mp3/`
- 🌐 **Browser** (`sys.platform == "emscripten"`): Loads OGG files from `ogg/`

### Why Two Formats?

- ✅ **OGG Vorbis**: Required for browser (Pygbag) - Pygame in browser cannot load MP3
- ✅ **MP3**: Faster loading on desktop, smaller file sizes in some cases
- ❌ **MP3 in browser**: Causes "Surface doesn't have a colorkey" error

## Sound Packs

### Default (Space/Sci-Fi)
- `default_conquest.ogg` - Energy beam for planet conquest
- `default_explosion.ogg` - Space explosion for failed attacks
- `default_launch.ogg` - Warp drive for fleet launches
- `default_victory.ogg` - Triumphant fanfare for victories

### Classical (Classical Music)
- `rachmaninoff-prelude-c-sharp-minor_trimmed_7s.ogg` - Conquest sound
- `beethoven-symphony-no5_trimmed_4s.ogg` - Attack failed sound

### Silly (Comedy/Cartoon)
- `silly_conquest.ogg` - Cartoon victory sound
- `silly_explosion.ogg` - Bonk sound for attacks  
- `silly_launch.ogg` - Boing sound for launches

## Working with Audio Files

### Converting MP3 to OGG

```bash
python convert_to_ogg.py
```
Converts all MP3 files in `mp3/` to OGG format in `ogg/`.

### Trimming Audio Files

```bash
python trim_audio.py <input_file> <duration_seconds> [output_name]
```
Creates both MP3 and OGG versions in their respective directories.

See `TRIM_INSTRUCTIONS.md` for details.

### Generating Sound Effects

**Default sounds:**
```bash
python generate_default_sounds.py
```

**Silly sounds:**
```bash
python generate_silly_sounds.py
```

Both scripts create MP3 and OGG versions automatically.

## For Developers

When adding new audio to the game:

1. **Create/obtain the audio** (any format)
2. **Trim if needed** using `trim_audio.py`
3. **Place in correct directories:**
   - MP3 files → `mp3/`
   - OGG files → `ogg/`
4. **Update the sound plugin** to reference `assets/audio/ogg/<filename>.ogg`
5. **Test locally and in browser**
6. **Commit both MP3 and OGG files**

## Requirements

```bash
pip install pydub
brew install ffmpeg  # macOS
# or: sudo apt-get install ffmpeg  # Linux
```

## Technical Notes

- **Platform detection**: All sound plugins check `sys.platform == "emscripten"` to determine format
- **Desktop**: Loads MP3 files from `assets/audio/mp3/` for optimal performance
- **Browser**: Loads OGG files from `assets/audio/ogg/` for compatibility
- Sample rate: 22050 Hz (standard for game audio)
- Format: Stereo, 16-bit
- The platform detection is automatic - no configuration needed!
