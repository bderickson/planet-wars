# Audio Trimming Instructions

## Prerequisites

```bash
pip install pydub
brew install ffmpeg  # macOS
# or: sudo apt-get install ffmpeg  # Linux
```

## Usage

The `trim_audio.py` script trims audio files and converts them to both MP3 and OGG formats:

```bash
python trim_audio.py <input_file> <duration_seconds> [output_base_name]
```

### Examples

**Basic usage (auto-generates output name):**
```bash
python trim_audio.py rachmaninoff.mp3 7
```
Creates:
- `mp3/rachmaninoff_trimmed_7s.mp3`
- `ogg/rachmaninoff_trimmed_7s.ogg`

**With custom output name:**
```bash
python trim_audio.py beethoven.mp3 4 beethoven-symphony-no5_trimmed_4s
```
Creates:
- `mp3/beethoven-symphony-no5_trimmed_4s.mp3`
- `ogg/beethoven-symphony-no5_trimmed_4s.ogg`

## Output Format

- **MP3**: Kept for reference and desktop use
- **OGG**: Used by the game for browser compatibility (Pygame in browser doesn't support MP3)

## Workflow

1. Add your source audio file to the `assets/audio/` directory
2. Run the trim script to create trimmed versions in both formats
3. The game automatically loads OGG files from `assets/audio/ogg/`
4. MP3 files in `assets/audio/mp3/` are for reference/archival

## Notes

- Browser (Pygbag) requires OGG format - MP3 files cause errors
- Both formats are generated automatically for convenience
- Original/untrimmed files can be kept outside the mp3/ogg directories
