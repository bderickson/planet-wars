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
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                logger.info("Audio mixer initialized in SillySoundPlugin")
            except pygame.error as e:
                logger.warning(f"Audio mixer init failed in SillySoundPlugin: {e}")
        
        # Detect platform and choose appropriate format
        self.is_browser = sys.platform == "emscripten"
        self.audio_dir = "assets/audio/ogg" if self.is_browser else "assets/audio/mp3"
        self.audio_ext = ".ogg" if self.is_browser else ".mp3"
        logger.info(f"Platform: {'browser' if self.is_browser else 'desktop'}, using {self.audio_ext} files from {self.audio_dir}")
        
        self.sounds = {}
        self._load_sounds()
    
    def _load_sounds(self):
        """
        Load silly sounds with fallback support.
        Tries MP3 first (iOS Safari), falls back to OGG (other browsers).
        """
        sound_names = ['conquest', 'explosion', 'launch', 'victory']
        
        for sound_key in sound_names:
            sound_loaded = False
            
            # Try MP3 first (works on iOS Safari)
            mp3_path = f'assets/audio/mp3/silly_{sound_key}.mp3'
            if os.path.exists(mp3_path):
                try:
                    self.sounds[sound_key] = pygame.mixer.Sound(mp3_path)
                    logger.debug(f"Loaded MP3 sound: {mp3_path}")
                    sound_loaded = True
                except Exception as e:
                    logger.debug(f"MP3 load failed for {mp3_path}: {e}, trying OGG...")
            
            # Fallback to OGG if MP3 failed or doesn't exist
            if not sound_loaded:
                ogg_path = f'assets/audio/ogg/silly_{sound_key}.ogg'
                if os.path.exists(ogg_path):
                    try:
                        self.sounds[sound_key] = pygame.mixer.Sound(ogg_path)
                        logger.debug(f"Loaded OGG sound (fallback): {ogg_path}")
                        sound_loaded = True
                    except Exception as e:
                        logger.warning(f"OGG load also failed for {ogg_path}: {e}")
            
            # If both formats failed, set to None
            if not sound_loaded:
                logger.warning(f"Could not load sound '{sound_key}' in any format")
                self.sounds[sound_key] = None
    
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
