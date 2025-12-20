"""
Silly sound plugin - goofy and comedic sounds
Platform-aware: MP3 for desktop, OGG for browser
"""
import pygame
import os
import sys
from game.sound_plugins.base_sound_plugin import BaseSoundPlugin
from game.logger import get_logger

logger = get_logger(__name__)


class SillySoundPlugin(BaseSoundPlugin):
    """Silly/comedic sound pack"""
    
    def __init__(self):
        super().__init__()
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            logger.info("Audio mixer initialized in SillySoundPlugin")
        
        # Detect platform and choose appropriate format
        self.is_browser = sys.platform == "emscripten"
        self.audio_dir = "assets/audio/ogg" if self.is_browser else "assets/audio/mp3"
        self.audio_ext = ".ogg" if self.is_browser else ".mp3"
        logger.info(f"Platform: {'browser' if self.is_browser else 'desktop'}, using {self.audio_ext} files from {self.audio_dir}")
        
        self.sounds = {}
        self._load_sounds()
    
    def _load_sounds(self):
        """Load silly sounds (format based on platform)"""
        sound_files = {
            'conquest': f'{self.audio_dir}/silly_conquest{self.audio_ext}',
            'explosion': f'{self.audio_dir}/silly_explosion{self.audio_ext}',
            'launch': f'{self.audio_dir}/silly_launch{self.audio_ext}',
        }
        
        for key, filepath in sound_files.items():
            if os.path.exists(filepath):
                try:
                    self.sounds[key] = pygame.mixer.Sound(filepath)
                    logger.debug(f"Loaded sound: {filepath}")
                except Exception as e:
                    logger.warning(f"Could not load {filepath}: {e}")
                    self.sounds[key] = None
            else:
                logger.warning(f"Sound file not found: {filepath}")
                self.sounds[key] = None
    
    def attack_succeeded(self):
        """Play cartoon victory sound"""
        if 'conquest' in self.sounds and self.sounds['conquest']:
            try:
                self.sounds['conquest'].play()
                logger.debug("Playing conquest sound")
            except Exception as e:
                logger.error(f"Could not play conquest sound: {e}")
    
    def attack_failed(self):
        """Play bonk sound"""
        if 'explosion' in self.sounds and self.sounds['explosion']:
            try:
                self.sounds['explosion'].play()
                logger.debug("Playing explosion sound")
            except Exception as e:
                logger.error(f"Could not play explosion sound: {e}")
    
    def fleet_launched(self):
        """Play boing sound"""
        if 'launch' in self.sounds and self.sounds['launch']:
            try:
                self.sounds['launch'].play()
                logger.debug("Playing launch sound")
            except Exception as e:
                logger.error(f"Could not play launch sound: {e}")
    
    def game_victory(self):
        """No special victory sound yet"""
        pass
    
    def game_defeat(self):
        """No special defeat sound yet"""
        pass
