"""
Classical sound plugin - all classical music pieces
Platform-aware: MP3 for desktop, OGG for browser
"""
import pygame
import os
import sys
from game.sound_plugins.base_sound_plugin import BaseSoundPlugin
from game.logger import get_logger

logger = get_logger(__name__)


class ClassicalSoundPlugin(BaseSoundPlugin):
    """Classical music sound pack"""
    
    def __init__(self):
        super().__init__()
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                logger.info("Audio mixer initialized in ClassicalSoundPlugin")
            except pygame.error as e:
                logger.warning(f"Audio mixer init failed in ClassicalSoundPlugin: {e}")
        
        # Detect platform and choose appropriate format
        self.is_browser = sys.platform == "emscripten"
        self.audio_dir = "assets/audio/ogg" if self.is_browser else "assets/audio/mp3"
        self.audio_ext = ".ogg" if self.is_browser else ".mp3"
        logger.info(f"Platform: {'browser' if self.is_browser else 'desktop'}, using {self.audio_ext} files from {self.audio_dir}")
        
        self.sounds = {}
        self._load_sounds()
    
    def _load_sounds(self):
        """Load classical sounds from trimmed audio files (format based on platform)"""
        try:
            # Load Rachmaninoff conquest sound (trimmed to 7 seconds)
            conquest_path = f'{self.audio_dir}/rachmaninoff-prelude-c-sharp-minor_trimmed_7s{self.audio_ext}'
            if os.path.exists(conquest_path):
                self.sounds['conquest'] = pygame.mixer.Sound(conquest_path)
                logger.debug(f"Loaded sound: {conquest_path}")
            else:
                logger.warning(f"Sound file not found: {conquest_path}")
                self.sounds['conquest'] = None
            
            # Load Beethoven's Symphony No. 5 for failed attacks (trimmed to 4 seconds)
            beethoven_path = f'{self.audio_dir}/beethoven-symphony-no5_trimmed_4s{self.audio_ext}'
            if os.path.exists(beethoven_path):
                self.sounds['explosion'] = pygame.mixer.Sound(beethoven_path)
                logger.debug(f"Loaded sound: {beethoven_path}")
            else:
                logger.warning(f"Sound file not found: {beethoven_path}")
                self.sounds['explosion'] = None
            
        except Exception as e:
            logger.error(f"Error loading classical sounds: {e}", exc_info=True)
            self.sounds = {}
    
    def attack_succeeded(self):
        """Play Rachmaninoff's Prelude (entire trimmed file)"""
        if 'conquest' in self.sounds and self.sounds['conquest']:
            try:
                self.sounds['conquest'].play()
                logger.debug("Playing conquest sound")
            except Exception as e:
                logger.error(f"Could not play conquest sound: {e}")
    
    def attack_failed(self):
        """Play Beethoven's Symphony No. 5 opening (first 3.5 seconds of trimmed file)"""
        if 'explosion' in self.sounds and self.sounds['explosion']:
            try:
                # Play only first 3.5 seconds of the 4-second trimmed file
                self.sounds['explosion'].play(maxtime=3500, fade_ms=50)
                logger.debug("Playing explosion sound")
            except Exception as e:
                logger.error(f"Could not play explosion sound: {e}")
    
    def fleet_launched(self):
        """No special launch sound for classical"""
        pass
    
    def game_victory(self):
        """No special victory sound yet"""
        pass
    
    def game_defeat(self):
        """No special defeat sound yet"""
        pass


