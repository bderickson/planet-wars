"""
Configuration management - saves/loads player preferences
"""
import json
import os
import sys
from game.logger import get_logger

logger = get_logger(__name__)


class Config:
    """Manages game configuration and persistence"""
    
    def __init__(self, config_file="files/config.json"):
        self.config_file = config_file
        self.player_name = "Player"  # Default
        self.is_browser = sys.platform == "emscripten"
        logger.debug(f"Config initializing (browser: {self.is_browser})")
        
        # Ensure files directory exists (desktop only)
        if not self.is_browser:
            os.makedirs("files", exist_ok=True)
        
        self.load()
    
    def load(self):
        """Load configuration from file (or localStorage in browser)"""
        try:
            if self.is_browser:
                # In browser, use localStorage
                logger.debug("Loading config from localStorage")
                self._load_from_localstorage()
            else:
                # Desktop: use file
                logger.debug(f"Loading config from {self.config_file}")
                if os.path.exists(self.config_file):
                    with open(self.config_file, 'r') as f:
                        data = json.load(f)
                        self.player_name = data.get("player_name", "Player")
                        logger.info(f"Config loaded: player_name={self.player_name}")
        except Exception as e:
            # If anything fails, use defaults
            logger.warning(f"Config load failed (using defaults): {e}")
            pass
    
    def _load_from_localstorage(self):
        """Load from browser localStorage"""
        try:
            # Use JavaScript to access localStorage
            import platform
            logger.debug("Attempting to load from localStorage")
            if hasattr(platform, 'window'):
                storage = platform.window.localStorage
                data_str = storage.getItem('planet_wars_config')
                logger.debug(f"localStorage data: {data_str}")
                if data_str:
                    data = json.loads(data_str)
                    self.player_name = data.get("player_name", "Player")
                    logger.info(f"Loaded player_name from localStorage: {self.player_name}")
                else:
                    logger.info("No config found in localStorage, using default")
            else:
                logger.warning("platform.window not available")
        except Exception as e:
            logger.error(f"localStorage load failed: {e}", exc_info=True)
    
    def save(self):
        """Save configuration to file (or localStorage in browser)"""
        try:
            logger.debug(f"Saving config (browser: {self.is_browser}, player_name: {self.player_name})")
            if self.is_browser:
                self._save_to_localstorage()
            else:
                with open(self.config_file, 'w') as f:
                    json.dump({
                        "player_name": self.player_name
                    }, f, indent=2)
                logger.info(f"Config saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Config save failed: {e}", exc_info=True)
    
    def _save_to_localstorage(self):
        """Save to browser localStorage"""
        try:
            import platform
            logger.debug("Attempting to save to localStorage")
            if hasattr(platform, 'window'):
                storage = platform.window.localStorage
                data_str = json.dumps({"player_name": self.player_name})
                storage.setItem('planet_wars_config', data_str)
                logger.info(f"Saved player_name to localStorage: {self.player_name}")
                
                # Verify the save worked
                verify = storage.getItem('planet_wars_config')
                logger.debug(f"Verification read: {verify}")
            else:
                logger.warning("platform.window not available for save")
        except Exception as e:
            logger.error(f"localStorage save failed: {e}", exc_info=True)


